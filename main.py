import os
import pathlib
import argparse
import uuid
from jinja2 import Template
from git import Repo
import random
import string


#generate random host suffix 6 chars


def ssh_host(host):
    ''' SSH into a lab host'''
    #os.system(f'ssh -o ProxyCommand="{paramiko_proxy_command}" -o StrictHostKeyChecking=no vyos@{host}')
    # with random host suffix it will not work anymore
    raise NotImplementedError


def run_lab(args):
    result = []
    for lab in args.lab:
        # generate vyos-oobm hostname and paramiko proxy command and prepare defaultinventory.yml
        random_host_suffix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        oobmhostname = f"oobm-{random_host_suffix}"
        paramiko_proxy_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i {os.getcwd()}/inventory/id_rsa -W %h:%p vyos@{oobmhostname}"
        template_inventory = open('defaultinventory.yml.j2')
        template_inventory = Template(template_inventory.read())
        with open('defaultinventory.yml','w+') as f:
            f.write(template_inventory.render(oobm_hostname=oobmhostname, proxy_command=paramiko_proxy_command))
    
        # open ansible.cfg template
        template_f = open('ansible.cfg.j2')
        template = Template(template_f.read())
        # override new ansible file
        with open('ansible.cfg','w+') as f:
            log_path = f"./logs/{args.branch}/{lab}.log"
            f.write(template.render(log_path=log_path, proxy_command=paramiko_proxy_command))

        # create logdir and remove old logfile before ansible run
        pathlib.Path(f"logs/{args.branch}/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"logs/{args.branch}/{lab}.log").unlink(missing_ok=True)

        iso = f"-e node_template_iso={args.iso_path} -e node_template_version={args.iso_version}"
        upgrade = ""
        verbose = ""
        if args.upgrade_iso_path and args.upgrade_iso_version and args.upgrade:
            upgrade = f"-e upgrade=True -e upgrade_iso={args.upgrade_iso_path} -e upgrade_iso_version={args.upgrade_iso_version}"
        
        if args.verbose:
            verbose = "-vvv"
        
        command_string = f'ansible-playbook -i labinventory.py -e oobm_hostname={oobmhostname} -e lab={lab} -e branch={args.branch} {iso} {upgrade} playbook.yml {verbose}'
        exit_code_lab = os.WEXITSTATUS(os.system(command_string))
        
        result.append((lab,log_path, exit_code_lab))
        # cleanup not needed anymore
        #if exit_code_lab != 0:
        #    # clean lab only if it was not successful
        #    command_string_cleanup = f'ansible-playbook -i labinventory.py -e oobm_hostname={oobmhostname} -e lab={lab} -e branch={args.branch} playbook-cleanup.yml {verbose}'
        #    os.system(command_string_cleanup)
    
    return result


def main():
    # collect branches choices
    branches =[]
    for entry in os.listdir('labs'):
        if os.path.isdir(f'labs/{entry}'):
            branches.append(entry)
    
    parser = argparse.ArgumentParser(description='Ansible wrapper')
    subparsers = parser.add_subparsers(dest="command")
    # run commands
    parser_run = subparsers.add_parser("run", help="Run ansible playbook")
    parser_run.add_argument("--lab", "-l", type=str, help="Labname")
    parser_run.add_argument("--alllabs", "-a", help="run all Labs", action="store_true")
    parser_run.add_argument("--iso_path", type=str, help="ISO URL", required=True)
    parser_run.add_argument("--iso_version", type=str, help="Versionname", required=True)
    parser_run.add_argument("--upgrade_iso_path", type=str, help="ISO Upgrade URL")
    parser_run.add_argument("--upgrade_iso_version", type=str, help="Upgrade Versionname")
    parser_run.add_argument("--upgrade", "-u", action="store_true", help="do an upgrade")
    parser_run.add_argument("--branch", "-b", type=str, help="the lab and documentation branchname", required=True, choices=branches)
    parser_run.add_argument("--verbose", "-v", action="store_true", help="Ansible verbose output")

    # ssh commands
    parser_ssh = subparsers.add_parser("ssh", help="connect to a running ssh host")
    parser_ssh.add_argument("host", type=str, help="name of host in the affected lab")

    args = parser.parse_args()

    # run
    if args.command == "run":
    # check if all needed args are defined
        if args.upgrade_iso_path or args.upgrade_iso_version or args.upgrade:
            if not (args.upgrade_iso_path and args.upgrade_iso_version and args.upgrade):
                parser.error("--upgrade/-u, --upgrade_iso_path and --upgrade_iso_version must definded")
        
        if args.lab and args.alllabs:
            parser.error("--lab/-l and --alllabs are mutually exclusive")
        
        if not (args.lab or args.alllabs):
            parser.error("--lab/-l or --alllabs must be defined")
        
        branch_labs = []
        for entry in os.listdir(f'labs/{args.branch}'):
            if os.path.isdir(f'labs/{args.branch}/{entry}'):
                branch_labs.append(entry)
        
        if args.lab:
            if not args.lab in branch_labs:
                parser.error(f"lab {args.lab} not found in branch {args.branch}")
        
        if args.alllabs:
            args.lab = branch_labs
        else:
            args.lab = [args.lab]

        try:
            repo = Repo('vyos-documentation')
        except:
            pathlib.Path('vyos-documentation').unlink(missing_ok=True)
            repo = Repo.clone_from('git@github.com:vyos/vyos-documentation.git', 'vyos-documentation')

        repo.git.checkout(args.branch)
        repo.git.pull()
        run_result = run_lab(args)
        success = False
        for lab,log_path, exit_code in run_result:            
            print(f"{lab} finished with exit code {exit_code}")
            if exit_code == 0:
                success = True

        if success:
            repo.git.checkout('-b', f'{args.branch}_autotest_{args.iso_version}')
            repo.git.add('docs/*')
            repo.git.commit('-m', f'Update autotest labs with {args.iso_version}')

        
        # delete upgrade temp files which where written from andible/paramiko upload module
        # these files are all 
        for entry in os.listdir():
            try:
                # this failed if entry is not a uuid
                uuid.UUID(str(entry))
                pathlib.Path(entry).unlink(missing_ok=True)
            except:
                pass
        

    # ssh
    if args.command == "ssh":
        ssh_host(args.host)


if __name__ == "__main__":
    main()