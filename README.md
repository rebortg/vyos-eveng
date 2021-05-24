# VyOS EVENG Lab Testing

This POC is for automatic build and test predefined lab for vyos.
At the moment it only work with EVE-NG Pro version, b/c the API is diffent from the CE version

## Quickstart

must set Ansible vars in `playbook.yml`

`node_template_iso`: the vyos iso url
`node_template_version` the vyos version used in eve-ng

eve-ng user and password are `ansible` as a default in the roles

start the process

    ansible-playbook -i labinventory.py  -e lab=AnsibleExample playbook.yml

The lab name must the same as the lab name in the `lab` folder. For example `AnsibleExample`.


## process

* create a new template based on iso and version name, do nothing when a the version is there
* stop and delete a existing lab with the same name
* create the lab from lab folder
* start the nodes
* configure the nodes
* run ping tests
* run command tests
* generate rst documentation
* stop all nodes and delete the lab

if something failed, you can open the lab in the `lab management` and investigate the problem.