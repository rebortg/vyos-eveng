# VyOS Eve-NG Labs

In this location, the Labs are stored for [[ https://github.com/rebortg/vyos-eveng ]].

## content of the Lab Directory

### LABNAME.rst.j2

The RST file for rendering the output

### LABNAME.unl.j2

The Lab file for import to eve-ng

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
    set service dhcp-server shared-network-name MGMT subnet 10.100.0.0/24 range 0 start '10.100.0.10'
    set service dhcp-server shared-network-name MGMT subnet 10.100.0.0/24 range 0 stop '10.100.0.250'
    set service ssh
    set system host-name vyos-oobm
    set system login user vyos authentication public-keys default key AAAAB3NzaC1yc2EAAAADAQABAAABgQDaCjzejtf56qx40toZqPRLcpg0fWJxpvR5cS9oqh+3+rRURKVrGIbgCmeucBC+kQnyvAqugCtEIZKDyk/kl9Z8eLoCjjkr4pguxo9PKWsDiMBdit1DY6m2Mr0BotbhhaNmIvRkA8/5apI6/RrNlo78Pj1doiu64+cqUjzvh5BuBUCbIaseE+4pg2Fs28d+NM20J4eOplHYnsVz7Aipj0UzT/HaIo8alPyZHOKuPOcOXZGJEwjayszQoQbKwIpBxCJM2m5zQyWkirX8QvmnIie57TSQ7J9zNB4NhLpUV27QYBBixMZOOwDJQpnISfjOd/tFpM5fn0vOIp02oQAHpK1hwQBFLVjAI50z8K96zTIwEPeCwIosTBer4HTUY073zpCVEsvnsT5c5Y0UVJLT+235S1XbuBr5zMvAAN9CpLb+WqNlDpvI/rAIVQTFjZOXr0x9rEVGRmTT19GGzjp2rXu9SIrnJ0d0X5ycyIp1dvoBngb4GWSkZaGUsYEDFk/kONs=
    set system login user vyos authentication public-keys default type ssh-rsa


a minimal config of the nodes:

    The hostname is important and will be used in ansible 

    set system host-name rtr01
    set interfaces ethernet eth0 address 'dhcp'
    set service ssh
    set system login user vyos authentication public-keys default key AAAAB3NzaC1yc2EAAAADAQABAAABgQDaCjzejtf56qx40toZqPRLcpg0fWJxpvR5cS9oqh+3+rRURKVrGIbgCmeucBC+kQnyvAqugCtEIZKDyk/kl9Z8eLoCjjkr4pguxo9PKWsDiMBdit1DY6m2Mr0BotbhhaNmIvRkA8/5apI6/RrNlo78Pj1doiu64+cqUjzvh5BuBUCbIaseE+4pg2Fs28d+NM20J4eOplHYnsVz7Aipj0UzT/HaIo8alPyZHOKuPOcOXZGJEwjayszQoQbKwIpBxCJM2m5zQyWkirX8QvmnIie57TSQ7J9zNB4NhLpUV27QYBBixMZOOwDJQpnISfjOd/tFpM5fn0vOIp02oQAHpK1hwQBFLVjAI50z8K96zTIwEPeCwIosTBer4HTUY073zpCVEsvnsT5c5Y0UVJLT+235S1XbuBr5zMvAAN9CpLb+WqNlDpvI/rAIVQTFjZOXr0x9rEVGRmTT19GGzjp2rXu9SIrnJ0d0X5ycyIp1dvoBngb4GWSkZaGUsYEDFk/kONs=
    set system login user vyos authentication public-keys default type ssh-rsa

### lab_config.yml

Ansible tasks to configure the lab after all nodes are started and are running with the startup-config

### inventory.yml

This is the lab inventory file. An inventory script will parse it and add the hosts to the ansible inventroy.
Also test commands will provide here:

The Playbook wide vars define
- start_stop_nodes: a list of nodes, see unl file, which are stopped and started via the eveng API.
  This is mostly used for VPCs that cannot be handle via the OOBM network.

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
    vars:
      start_stop_nodes:
        - 5
