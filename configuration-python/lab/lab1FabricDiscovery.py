from labScript import *
from apicPython import addFabricNode


class Lab1FabricDiscovery(LabScript):
    """
    Discover switches and spines
    """
    def __init__(self):
        self.description = 'Discovery all the switches and spines'
        self.fabric_nodes = []
        super(Lab1FabricDiscovery, self).__init__()

    def run_yaml_mode(self):
        super(Lab1FabricDiscovery, self).run_yaml_mode()
        self.fabric_nodes = self.args['fabric_nodes']

    def wizard_mode_input_args(self):
        fabric_nodes = add_mos('Add a Fabric Node', addFabricNode.input_key_args)
        for fabric_node in fabric_nodes:
            args = {'serial_number': fabric_node['key_args'][0],
                    'node_id': fabric_node['key_args'][1],
                    'node_name': fabric_node['key_args'][2]}
            self.fabric_nodes.append(args)

    def main_function(self):
        parent_mo = self.check_if_mo_exist('uni/controller/nodeidentpol', description='Fabric Node')
        for fabricNode in self.fabric_nodes:
            addFabricNode.add_fabric_node(parent_mo, fabricNode['serial_number'], fabricNode['node_id'], fabricNode['node_name'])

if __name__ == '__main__':
    mo = Lab1FabricDiscovery()