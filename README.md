# VyOS EVENG Lab Testing

This POC is for automatic build and test predefined labs for vyos.
At the moment, it only works with the EVE-NG Pro version, b/c the API is different from the CE version

## Quickstart

install python pramiko and scp

`pip install paramiko`

`pip install scp`

### set vars and environment specifics

you can set Ansible `vars` in `playbook.yml` or as arguments in the execution of main.py

`node_template_iso`: the vyos iso url

`node_template_version`: the vyos version used in eve-ng


Create a new User in Eve-NG. Name and password are `ansible`.
or set the user in the `playbook.yml` `vars`:

`eve_ng_user`

`eve_ng_password`

It is recommended to use a dedicated account for the Ansible Workflow. It is, maybe at the moment,
not possible to log in with the user in the Eve-NG GUI and use the same user with the ansible workflow.
With a different User, it is possible to look live in config process.

Edit the `poxy_command` option in the `ansible.cfg` and set the absolute path for the `inventory/id_rsa` file.
Paramiko can't use a relative path in this case.

### Start the Process

To set some settings and get the ansible logs after run, there is a wrapper for the ansible-playbook

    python main.py run -l LABNAME

to test a upgrade, set the iso path in the playbook `upgrade_iso` var and run:

    python main.py run -l LABNAME --upgrade

### Connect to Host in Lab

    python main.py ssh HOSTNAME

This is only possible if a `run` command fail and the lab is up.




## The Process

1. create a new template based on iso and version name, do nothing when a VyOS image with the same version is present
2. stop and delete an existing lab with the same name
3. create the lab from the lab folder
4. start the nodes
5. configure the nodes
6. run ping tests
7. run command tests
8. do a reboot
9. run command tests
10. if upgrade, upgrade all vyos
11. if upgrade, run point 6 and 7 again
12. generate *.rst documentation
13. stop all nodes and delete the lab

If something failed, you can open the lab in vyos the `lab management` and investigate the problem.

## TODO and Knows issues

TODO:
ISO URL from local filesystem
check reboot per default

ISSUES:
more than one running lab is not possible if every oobm host is called vyos-oobm




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
            PE2:
                tests:
                    ping:
                        - "172.29.255.1"
                        - "172.29.255.3"
                    commands:
                        - desc: "PING vyos-oobm with VRF"
                          command: "ping 10.100.0.1 vrf mgmt count 1"
                          wait_for: 
                            - result[0] contains '1 packets transmitted, 1 received'
                    stdout:
                        - name: bgp_evpn_net
                          command: "show bgp l2vpn evpn 10.3.1.10"
