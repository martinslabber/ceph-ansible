import ansible.errors as errors
from ansible.plugins.lookup import LookupBase
import socket

# Inspired by:
# https://stackoverflow.com/questions/32324120/arbitrary-host-name-resolution-in-ansible

# The builtin lookup dig
# (http://docs.ansible.com/ansible/latest/playbooks_lookups.html#the-dns-lookup-dig)
# no not fulfil my requirements and it require an additional package installed.


class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, variables=None, **kwargs):
        ip_addresses = []
        for hostname in terms:
            if not isinstance(hostname, basestring):
                raise errors.AnsibleError("ip lookup expects a string "
                                          "(hostname)")
            ip_addresses.append(self.resolve_ip_address(hostname))
        return ip_addresses

    def resolve_ip_address(self, hostname):
        """Resolve a hostname to IP address or return IP address if that was
        given.

        If IPv4 CIDR notation was used the hostname is resolved and the mask
        is preserved.  PTR lookups are not performed.
        """
        if '/' in hostname:
            # This is not URL safe, it's not intended to be.
            hostname, mask = hostname.split('/', 1)
        else:
            mask = None
        address = socket.gethostbyname(hostname)
        if mask:
            address += "/{}".format(mask)
        return address
