# Copyright (C) 2017 Antoine Fourmy <antoine dot fourmy at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class DataFlow(object):
    
    def __init__(self, src_ip, dst_ip):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.throughput = 0
        self.src_mac = None
        self.dst_mac = None
        
    def __repr__(self):
        return '''Data flow:
        Source IP: {src_ip} Destination IP: {dst_ip}
        Source MAC: {src_mac} Destination MAC: {dst_mac}
        Throughput: {throughput}
        '''.format(
                   src_ip = self.src_ip,
                   dst_ip = self.dst_ip,
                   src_mac = self.src_mac,
                   dst_mac = self.dst_mac,
                   throughput = self.throughput
                   )
        
class IPAddress(object):

    # an IP address object is defined as an IP and a subnet ('IP/subnet')
    def __init__(self, ip_addr, subnet, interface=None):
        self.ip_addr = ip_addr
        self.subnet = subnet
        self.mask = tomask(self.subnet)
        self.network = compute_network(self.ip_addr, self.mask)
        # interface to which the IP address is attached
        self.interface = interface
        
    def __repr__(self):
        return '{ip}/{subnet}'.format(ip=self.ip_addr, subnet=self.subnet)
        
    def __lt__(self, other):
        return self.interface.name

BYTE = range(32, 0, -8)

def toip(ip):
    return sum(x << s - 8 for x, s in zip(map(int, ip.split('.')), BYTE))
    
def tostring(ip):
    return '.'.join(str((ip & (1 << i) - 1) >> (i - 8)) for i in BYTE)

def compute_network(ip, mask):
    return tostring(toip(ip) & toip(mask))

def tosubnet(ip):
    # convert a subnet mask to a subnet
    # ex: tosubnet('255.255.255.252') = 30
    return ''.join(map(bin, map(int, ip.split('.')))).count('1')
    
def wildcard(ip):
    # convert a subnet mask to a wildcard mask or the other way around
    # ex: towildcard('255.255.255.252') = '0.0.0.3'
    #     towildcard('0.0.0.3') = '255.255.255.252'
    return '.'.join(map(lambda i: str(255 - int(i)), ip.split('.')))

def tomask(subnet):
    # convert a subnet to a subnet mask
    # ex: tomask(30) = '255.255.255.252'
    return tostring(int('1'*subnet + '0'*(32 - subnet), 2))
    
def mac_incrementer(mac_address, nb):
    # increment a mac address by 'nb'
    return '{:012X}'.format(int(mac_address, 16) + nb)
    
def mac_comparer(mac1, mac2):
    # 06:00:00:00:00:01 > 05:AA:CC:00:00:11
    mac1, mac2 = ''.join(mac1.split(':')), ''.join(mac2.split(':'))
    return mac_incrementer(mac1, 0) > mac_incrementer(mac2, 0)
    
def ip_incrementer(ip_address, nb):
    # increment an ip address by 'nb'
    return tostring(toip(ip_address) + nb)