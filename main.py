import os
import argparse
import uuid
from jinja2 import Template


'''
--run --urun
-l --lab NAME
--iso URL
--isoname NAME (default from iso)

must if -u is present
--uiso URL
--uisoname  NAME (default from iso)


set in ansible.cfg or with -e in ansible-playbook
- default_log_path
- paramiki proxy command

'''

labs =[]
for entry in os.listdir('labs'):
    if os.path.isdir(f'labs/{entry}'):
        labs.append(entry)


parser = argparse.ArgumentParser(description='Ansible wrapper')
subparsers = parser.add_subparsers(dest="command")
# run commands

parser_run = subparsers.add_parser("run", help="Run ansible playbook")
parser_run.add_argument("--lab", "-l", choices=labs, type=str, help="Labname", required=True)
parser_run.add_argument("--iso", type=str, help="ISO URL")
parser_run.add_argument("--isoname", type=str, help="Versionname")
parser_run.add_argument("--uiso", type=str, help="ISO Upgrade URL")
parser_run.add_argument("--uisoname", type=str, help="Upgrade Versionname")
parser_run.add_argument("--upgrade", "-u", action="store_true", help="do an upgrade")

# ssh commands
parser_ssh = subparsers.add_parser("ssh", help="connect to a running ssh host")
#parser_ssh.add_argument("--lab", "-l", type=str, help="Labname")
parser_ssh.add_argument("host", type=str, help="ISO URL")

args = parser.parse_args()

paramiko_proxy_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i {os.getcwd()}/inventory/id_rsa -W %h:%p vyos@vyos-oobm"

if args.command == "run":
    tf = open('ansible.cfg.j2')
    template = Template(tf.read())
    # override new ansible file
    wf = open('ansible.cfg','w+')
    log_path = f"./logs/{args.lab}.log"
    wf.write(template.render(log_path=log_path, proxy_command=paramiko_proxy_command))
    wf.close()

    #remove old logfile before ansible run
    try:
        os.remove(f"logs/{args.lab}.log")
    except:
        pass

    # TODO think over git workflow
    try:
        os.system(f"rm -rf vyos-documentation")
    except:
        pass
    os.system("git clone --branch equuleus git@github.com:vyos/vyos-documentation.git")

    iso = ""
    if args.iso and args.isoname:
        iso = f"-e node_template_iso={args.iso} -e node_template_version={args.isoname} "
    
    upgrade = ""
    if args.upgrade:
        upgrade = "-e upgrade=True "
    
    uiso = ""
    if args.uiso and args.uisoname:
        iso = f"-e upgrade_iso={args.uiso} -e upgrade_iso_version={args.uisoname} "

    command_string = f'ansible-playbook -i labinventory.py -e lab={args.lab} {iso} {upgrade} playbook.yml'
    exit_code = os.WEXITSTATUS(os.system(command_string))

    # delete upgrade temp files
    for entry in os.listdir():
        try:
            uuid.UUID(str(entry))
            os.remove(entry)
        except:
            pass


    if exit_code != 0:
        print(f"Lab {args.lab} failed, please check output and log ({log_path})")
        exit()

if args.command == "ssh":
    os.system(f'ssh -o ProxyCommand="{paramiko_proxy_command}" vyos@{args.host}')



#os.system("ansible-playbook -i labinventory.py -e lab=L3VPN_EVPN  playbook.yml")