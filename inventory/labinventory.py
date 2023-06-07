from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError
import yaml
import sys

DOCUMENTATION = ""

class InventoryModule(BaseInventoryPlugin):
    NAME = 'labinventory'
    allow_extras = True
    defaultinventory = {}
    lab = ''
    labinventory = {}

    def verify_file(self, path):
        with open("defaultinventory.yml", 'r') as stream:
            try:
                self.defaultinventory = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return False
        
        for arg in sys.argv:
            if "lab=" in arg:
                self.lab = arg.split('=')[1]
        
        if self.lab == '':
            return False
        
                
        with open(f"labs/{self.lab}/inventory.yml", 'r') as stream:
            try:
                self.labinventory = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return False
        
        return True

    def parse(self, inventory, loader, path, cache):
        super(InventoryModule, self).parse(inventory, loader, path)

        # fill default inventory
        for defaulthostsgroup in self.defaultinventory['hosts']:
            self.inventory.add_group(defaulthostsgroup)
            for defaulthost in self.defaultinventory['hosts'][defaulthostsgroup]:
                self.inventory.add_host(host=defaulthost, group=defaulthostsgroup)
                for var in self.defaultinventory['hosts'][defaulthostsgroup][defaulthost]:
                    self.inventory.set_variable(defaulthost, var, self.defaultinventory['hosts'][defaulthostsgroup][defaulthost][var])

        # fill lab inventory vyos hosts
        self.inventory.add_group('vyos')
        for labhost in self.labinventory['hosts']['vyos']:
            self.inventory.add_host(host=labhost, group='vyos')
            for var in self.defaultinventory['vyos_vars']:
                self.inventory.set_variable(labhost, var, self.defaultinventory['vyos_vars'][var])

            self.inventory.set_variable(labhost, 'lab_vars', self.labinventory['hosts']['vyos'][labhost])
        
        # fill other lab inventory hosts
        for group in self.labinventory['hosts']:
            if group == "vyos":
                continue
            self.inventory.add_group(group)
            for labhost in self.labinventory['hosts'][group]:
                self.inventory.add_host(host=labhost, group=group)
                for var in self.labinventory['hosts'][group][labhost]:
                    self.inventory.set_variable(labhost, var, self.labinventory['hosts'][group][labhost][var])
            
        
        try:
            # quick insert TODO: build more stable
            self.inventory.set_variable('eveng', 'start_stop_nodes', self.labinventory['vars']['start_stop_nodes'])
        except:
            pass

