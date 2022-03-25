# TODO 

## randomize vyos-oobm hostname
there can't be more than one running lab due the same name

### steps:
- add a random hash or fix hash to the name
- move creating of startup-config to ansible template file
	- create base64 decoded config via ansible from inventory/rtr.conf.j2 and vyos-oobm.conf.j2
	- more than one version of rtr.conf (vrf yes/no)

## image handling
- ISO URL from local filesystem
- Upgrade ISO from local filesystem
- Download upgrade ISO --> delegate_to eve-ng not ansible host
	- iso tmp dir?
	- iso from filesystem

## playbook

eveng url, user and password as argument in main.py

## lab docu

document the lab structure


## gen *.rst

exclude the log

## git process

vyos-documentation as submodule
generate a PR at the end