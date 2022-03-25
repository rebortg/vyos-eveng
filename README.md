# VyOS EVENG Lab Testing

This Environment is for automatic build and test predefined labs for vyos.
At the moment, it only works with the EVE-NG Pro version, b/c the API is different from the CE version

## Quickstart

install python requirements

`pip install -r requirements.txt`

Create a new User in Eve-NG. Username and password are both `ansible`.
or set the credentials in the `playbook.yml` `vars`:

`eve_ng_user`
`eve_ng_password`

It is recommended to use a dedicated account for the Ansible Workflow. It is, at the moment,
not possible to login with the user in the Eve-NG GUI and use the same user with the ansible workflow.
With a different User, it is possible to look live in the playbook process.

### Run the Process

see [[RUN.md]]

### Connect to Host in Lab

    python main.py ssh HOSTNAME

This is only possible if a `run` command failed and the lab is up.


## The Process

1. create a new template, based on iso and version name, do nothing when a VyOS image with the same version name is present
2. delete an existing lab with the same name, if all hosts are down in the lab
3. create the lab from the labs folder
4. start the nodes
5. configure the nodes
6. run ping tests
7. run command tests
8. collect command output
9. do a reboot
10. run command tests
11. if upgrade, upgrade all vyos
12. if upgrade, run point 6 and 7 again
13. generate *.rst documentation
14. stop all nodes and delete the lab

If something failed, you can open the lab in the eve-ng `lab management` section and investigate the problem.