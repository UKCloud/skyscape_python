__author__ = 'prossi'
from lxml import objectify

from skyscape.skyscape_vcloud_methods import Vcloud_Method


class lazy_property(object):
    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value


class VSE:
    def __init__(self, vseobject, connection):
        self.__dict__ = dict(vseobject.attrib)
        self.connection = connection

    @lazy_property
    def vse_data(self):
        return objectify.fromstring(self.connection.get_link(self.href))

    @lazy_property
    def firewall(self):
        rules = self.vse_data.Configuration.EdgeGatewayServiceConfiguration.FirewallService.FirewallRule
        holder = []
        for rule in rules:
            holder.append(rule)
        return holder

    def list_firewall_rules(self):
        for rule in self.firewall:
            print "Id: {0}".format(rule.Id)
            print "IsEnabled: {0}".format(rule.IsEnabled)
            print "MatchOnTranslate: {0}".format(rule.MatchOnTranslate)
            print "Description: {0}".format(rule.Description)
            print "Policy: {0}".format(rule.Policy)
            print "Protocols:"
            if hasattr(rule.Protocols, 'Any'):
                print " - ANY: {0}".format(rule.Protocols.Any)
            if hasattr(rule.Protocols, 'Icmp'):
                print " - Icmp: {0}".format(rule.Protocols.Icmp)
            print "Port: {0}".format(rule.Port)
            print "DestinationPortRange: {0}".format(rule.DestinationPortRange)
            print "DestinationIp: {0}".format(rule.DestinationIp)
            print "SourcePort: {0}".format(rule.SourcePort)
            print "SourcePortRange: {0}".format(rule.SourcePortRange)
            print "SourceIp: {0}".format(rule.SourceIp)
            print "EnableLogging: {0}".format(rule.EnableLogging)
            print ""

    @lazy_property
    def nat(self):
        return self.vse_data.Configuration.EdgeGatewayServiceConfiguration.NatService.NatRule

    @lazy_property
    def loadbalancer(self):
        return self.vse_data.Configuration.EdgeGatewayServiceConfiguration.LoadBalancerService.VirtualServer

    @lazy_property
    def dhcp(self):
        return self.vse_data.Configuration.EdgeGatewayServiceConfiguration.GatewayDhcpService.Pool

    @lazy_property
    def links(self):
        holder = []
        for link in self.vse_data.Link:
            new_method = Vcloud_Method(link, self.connection)
            if new_method.description != "":
                holder.append(new_method)
        return holder

    def list_links(self):
        i = 0
        for a in self.links:
            outputstring = "ID {0}: {1} - {2} - {3}".format(i, a.rel, a.description, a.href)
            i += 1
            print outputstring
