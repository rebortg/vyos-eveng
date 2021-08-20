# VyOS EVENG Lab Testing

This POC is for automatic build and test predefined labs for vyos.
At the moment, it only work with the EVE-NG Pro version, b/c the API is different from the CE version

## Quickstart

install collection:

`ansible-galaxy collection install vyos.vyos`

### set vars and environment specifics

you must set Ansible `vars` in `playbook.yml`


`node_template_iso`: the vyos iso url

`node_template_version`: the vyos version used in eve-ng


Create a new User in Eve-NG. Name and password are `ansible`.
or set the user in the `playbook.yml` `vars`:

`eve_ng_user`

`eve_ng_password`

It is recommend to use a dedicated account for the Ansible Workflow.

Edit the `poxy_command` option in the `ansible.cfg` and set the absolute path for the `inventory/id_rsa` file.
Paramiko can't use relative path in this case.

### Start the Process

    ansible-playbook -i labinventory.py  -e lab=AnsibleExample playbook.yml

The lab name must the same as the lab name in the `lab` folder. For example `AnsibleExample`.


## The Process

1. create a new template based on iso and version name, do nothing when a VyOS image with the same version is present
2. stop and delete an existing lab with the same name
3. create the lab from the lab folder
4. start the nodes
5. configure the nodes
6. run ping tests
7. run command tests
8. generate *.rst documentation
9. stop all nodes and delete the lab

If something failed, you can open the lab in the `lab management` and investigate the problem.


## content of the Lab Directory

### LABNAME.rst.j2

The RST file for rendering the output

### LABNAME.unl.j2

The Lab file to import to eve-ng

VyOS-OOBM must have the node id 1

    <node id="1" name="VyOS-OOBM" type="qemu" template="vyos" image="{{ node_template_name }}".....

The Startup-Config is base64 decoded.

    <configs>
      <config id="1">c2V0IGludGVyZmFjZX......Bzc2gtcnNh</config>
      <config id="2">c2V0IHN5c3RlbSBob3......GUNoLXJzYQ==</config>
    </configs>

The config of VyOS-OOBM is different from the other nodes:

    set interfaces ethernet eth0 address 'dhcp'
    set interfaces ethernet eth1 address '10.100.0.1/24'
    set service dhcp-server listen-address '10.100.0.1'
    set service dhcp-server hostfile-update
    set service dhcp-server shared-network-name MGMT subnet 10.100.0.0/24 default-router '10.100.0.1'
    set service dhcp-server shared-network-name MGMT subnet 10.100.0.0/24 range 0 start '10.100.0.10'
    set service dhcp-server shared-network-name MGMT subnet 10.100.0.0/24 range 0 stop '10.100.0.250'
    set service ssh
    set system host-name vyos-oobm
    set system login user vyos authentication public-keys default key AAAAB3NzaC1yc2EAAAADAQABAAABgQDaCjzejtf56qx40toZqPRLcpg0fWJxpvR5cS9oqh+3+rRURKVrGIbgCmeucBC+kQnyvAqugCtEIZKDyk/kl9Z8eLoCjjkr4pguxo9PKWsDiMBdit1DY6m2Mr0BotbhhaNmIvRkA8/5apI6/RrNlo78Pj1doiu64+cqUjzvh5BuBUCbIaseE+4pg2Fs28d+NM20J4eOplHYnsVz7Aipj0UzT/HaIo8alPyZHOKuPOcOXZGJEwjayszQoQbKwIpBxCJM2m5zQyWkirX8QvmnIie57TSQ7J9zNB4NhLpUV27QYBBixMZOOwDJQpnISfjOd/tFpM5fn0vOIp02oQAHpK1hwQBFLVjAI50z8K96zTIwEPeCwIosTBer4HTUY073zpCVEsvnsT5c5Y0UVJLT+235S1XbuBr5zMvAAN9CpLb+WqNlDpvI/rAIVQTFjZOXr0x9rEVGRmTT19GGzjp2rXu9SIrnJ0d0X5ycyIp1dvoBngb4GWSkZaGUsYEDFk/kONs=
    set system login user vyos authentication public-keys default type ssh-rsa


a minimal config of the nodes:

    The hostname is important and used in ansible 

    set system host-name rtr01
    set interfaces ethernet eth0 address 'dhcp'
    set service ssh
    set system login user vyos authentication public-keys default key AAAAB3NzaC1yc2EAAAADAQABAAABgQDaCjzejtf56qx40toZqPRLcpg0fWJxpvR5cS9oqh+3+rRURKVrGIbgCmeucBC+kQnyvAqugCtEIZKDyk/kl9Z8eLoCjjkr4pguxo9PKWsDiMBdit1DY6m2Mr0BotbhhaNmIvRkA8/5apI6/RrNlo78Pj1doiu64+cqUjzvh5BuBUCbIaseE+4pg2Fs28d+NM20J4eOplHYnsVz7Aipj0UzT/HaIo8alPyZHOKuPOcOXZGJEwjayszQoQbKwIpBxCJM2m5zQyWkirX8QvmnIie57TSQ7J9zNB4NhLpUV27QYBBixMZOOwDJQpnISfjOd/tFpM5fn0vOIp02oQAHpK1hwQBFLVjAI50z8K96zTIwEPeCwIosTBer4HTUY073zpCVEsvnsT5c5Y0UVJLT+235S1XbuBr5zMvAAN9CpLb+WqNlDpvI/rAIVQTFjZOXr0x9rEVGRmTT19GGzjp2rXu9SIrnJ0d0X5ycyIp1dvoBngb4GWSkZaGUsYEDFk/kONs=
    set system login user vyos authentication public-keys default type ssh-rsa

TODO: create base64 decoded config via ansible from inventory/rtr.conf.j2 and vyos-oobm.conf.j2

### lab_config.yml

Ansible tasks to configure the lab after all nodes are started and are running with the startup-config

### inventory.yml

This is the lab inventory files, a script parse it and add the hosts to the ansible inventroy.
Also test commands will provide here:

for example:

    hosts:
        vyos:
            rtr01:
                tests:
                    ping:
                    - "10.1.1.2"
                    commands:
                    - desc: "Test if IP is set to interface"
                        command: "ip -4 addr show dev eth1 | grep inet | tr -s ' ' | cut -d' ' -f3 | head -n 1"
                        stdout: "10.1.1.1/24"


            rtr02:
                tests:
                    ping:
                    - "10.1.1.1"
                    commands:
                    - desc: "Test if IP is set to interface"
                        command: "ip -4 addr show dev eth1 | grep inet | tr -s ' ' | cut -d' ' -f3 | head -n 1"
                        stdout: "10.1.1.2/24"
