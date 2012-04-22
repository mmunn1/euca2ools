# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2012, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from requestbuilder import Arg, Filter
from . import EucalyptusRequest

class DescribeAddresses(EucalyptusRequest):
    APIVersion = '2011-01-01'
    Description = 'Show information about elastic IP addresses'
    Args = [Arg('address', nargs='*', route_to=None,
                help='''limit results to one or more elastic IP addresses or
                        allocation IDs''')]
    Filters = [Filter('domain', choices=['standard', 'vpc'],
                      help='whether the address is a standard or VPC address'),
               Filter('instance-id',
                      help='instance the address is associated with'),
               Filter('public-ip', help='the elastic IP address'),
               Filter('allocation-id', help='allocation ID (VPC only)'),
               Filter('association-id', help='association ID (VPC only)')]
    ListMarkers = ['addressesSet']
    ItemMarkers = ['item']

    def main(self):
        alloc_ids = set(addr for addr in self.args.get('address', [])
                        if addr.startswith('eipalloc-'))
        public_ips = set(self.args.get('address', [])) - alloc_ids
        self.params = {}
        if alloc_ids:
            self.params['AllocationId'] = list(alloc_ids)
        if public_ips:
            self.params['PublicIp'] = list(public_ips)
        return self.send()

    def print_result(self, result):
        print result
        for addr in result.get('addressesSet', []):
            print self.tabify(['ADDRESS', addr.get('publicIp'),
                               addr.get('instanceId'),
                               addr.get('domain', 'standard'),
                               addr.get('allocationId'),
                               addr.get('associationId')])
