import os
import argparse
import uuid
from jinja2 import Template


# collect lab choices
labs =[]
for entry in os.listdir('labs'):
    if os.path.isdir(f'labs/{entry}'):
        labs.append(entry)


parser = argparse.ArgumentParser(description='Ansible wrapper')
subparsers = parser.add_subparsers(dest="command")
# run commands

parser_run = subparsers.add_parser("run", help="Run ansible playbook")
parser_run.add_argument("--lab", "-l", choices=labs, type=str, help="Labname", required=True)
parser_run.add_argument("--iso_path", type=str, help="ISO URL")
parser_run.add_argument("--iso_version", type=str, help="Versionname")
parser_run.add_argument("--upgrade_iso_path", type=str, help="ISO Upgrade URL")
parser_run.add_argument("--upgrade_iso_version", type=str, help="Upgrade Versionname")
parser_run.add_argument("--upgrade", "-u", action="store_true", help="do an upgrade")
parser_run.add_argument("--branch", "-b", type=str, help="the lab and documentation branchname", required=True,     choices=['master', 'equuleus'])

# ssh commands
parser_ssh = subparsers.add_parser("ssh", help="connect to a running ssh host")
#parser_ssh.add_argument("--lab", "-l", type=str, help="Labname")
parser_ssh.add_argument("host", type=str, help="ISO URL")

args = parser.parse_args()

paramiko_proxy_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i {os.getcwd()}/inventory/id_rsa -W %h:%p vyos@vyos-oobm"

if args.command == "run":
    print("")
    template_f = open('ansible.cfg.j2')
    template = Template(template_f.read())
    # override new ansible file
    write_f = open('ansible.cfg','w+')
    log_path = f"./logs/{args.lab}.log"
    write_f.write(template.render(log_path=log_path, proxy_command=paramiko_proxy_command))
    write_f.close()

    #remove old logfile before ansible run
    try:
        os.remove(f"logs/{args.lab}.log")
    except:
        pass

    iso = ""
    upgrade = ""

    if args.iso_path or args.iso_version:
        if args.iso_path and args.iso_version:
            # define Ansible envvars
            iso = f"-e node_template_iso={args.iso_path} -e node_template_version={args.iso_version}"
        else:
            print("--iso_path and --iso_version must definded")
            exit(255)

    
    if args.upgrade_iso_path or args.upgrade_iso_version:
        if args.upgrade_iso_path and args.upgrade_iso_version:
            # define Ansible envvars
            upgrade = f"-e upgrade=True -e upgrade_iso={args.upgrade_iso_path} -e upgrade_iso_version={args.upgrade_iso_version}"
        else:
            print("--upgrade, --upgrade_iso_path and --upgrade_iso_version must definded")
            exit(255)


    # TODO think over git workflow
    try:
        os.system(f"rm -rf vyos-documentation")
    except:
        pass
    os.system(f"git clone --branch {args.branch} git@github.com:vyos/vyos-documentation.git")
    os.system(f"git submodule set-branch --branch {args.branch} -- labs")
    os.system(f"git submodule update --remote -- labs")

    command_string = f'ansible-playbook -i labinventory.py -e lab={args.lab} {iso} {upgrade} playbook.yml'
    exit_code = os.WEXITSTATUS(os.system(command_string))

    # delete upgrade temp files which where written from andible/paramiko upload module
    for entry in os.listdir():
        try:
            uuid.UUID(str(entry))
            os.remove(entry)
        except:
            pass


    if exit_code != 0:
        print(f"Lab {args.lab} failed, please check output and log ({log_path})")
        exit(exit_code)

if args.command == "ssh":
    os.system(f'ssh -o ProxyCommand="{paramiko_proxy_command}" -o StrictHostKeyChecking=no vyos@{args.host}')