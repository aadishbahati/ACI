from labScript import *
from apicPython import createTenant
from apicPython import addSecurityDomain
from apicPython import createPrivateNetwork
from apicPython import createBridgeDomain


class Lab2CreateTenant(LabScript):
    """
    Discover switches and spines
    """
    def __init__(self):
        self.description = 'Create a Tenant with security domain, private network and bridge domains'
        self.tenant_required = True
        self.security_domains = []
        self.private_network = None
        self.bridge_domains = []
        super(Lab2CreateTenant, self).__init__()

    def run_yaml_mode(self):
        super(Lab2CreateTenant, self).run_yaml_mode()
        self.security_domains = self.args['security_domains']
        self.private_network = self.args['private_network']
        self.bridge_domains = self.args['bridge_domains']

    def wizard_mode_input_args(self):
        self.security_domains = [name['key_args'] for name in add_mos('Add a Security Domain', addSecurityDomain.input_key_args)]
        self.private_network = createPrivateNetwork.input_key_args()
        bridge_domains = add_mos('Add a Bridge Domain', createBridgeDomain.input_key_args)
        for bridge_domain in bridge_domains:
            args = {'name': bridge_domain['key_args'][0],
                    'subnet_ip': bridge_domain['key_args'][1]}
            self.bridge_domains.append(args)

    def main_function(self):
        fv_tenant = self.check_if_tenant_exist(return_boolean=True)
        if not fv_tenant:
            self.mo = self.modir.lookupByDn('uni')
            fv_tenant = createTenant.create_tenant(self.mo, self.tenant)
        for security_domain in self.security_domains:
            addSecurityDomain.add_security_domain(fv_tenant, security_domain)
        createPrivateNetwork.create_private_network(fv_tenant, self.private_network)
        for bridge_domain in self.bridge_domains:
            createBridgeDomain.createBridgeDomain(fv_tenant, bridge_domain['name'], bridge_domain['subnet_ip'], self.private_network)

if __name__ == '__main__':
    mo = Lab2CreateTenant()