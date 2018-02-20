#! /usr/bin/python

from peeringdb import PeeringDB
import sys, re

OrgList = [ 'Equinix', 'LINX', 'DE-CIX', 'Netnod', 'CoreSite', 'NIX.CZ', 'France-IX', 'LONAP', 'AMS-IX', 'Peering.cz', 'STHIX', 'NL-ix', 'SIX', 'FL-IX', 'BBIX', 'JPNAP', 'MegaIX', 'IX Australia', 'HKIX', 'PLIX', 'Thinx', 'KINX', 'ESPANIX', 'TorIX', 'VIX', 'IX.br', 'CyrusOne', 'NWAX', 'QIX', 'Digital Realty', 'BCIX', 'SLIX' ]

if __name__ == '__main__' :
    as_num = sys.argv[1]
    pdb = PeeringDB()

    # query ASN by parameter
    net_info_dict = pdb.all('net', asn=as_num)
    
    company_name = net_info_dict[0]["name"]
    company_website = net_info_dict[0]["website"]

    print '='*60
    print "AS number:\t" + as_num
    print "CompanyName:\t" + company_name
    print "WebSite:\t" + company_website
    print '='*60
    
    # query AS peerings details by parameter
    netixlan_info_dict = pdb.all('netixlan', asn=as_num)

    ix_info_dict = []
    warn_msg = ""
    total_speed = 0

#    print "\nPeerings"
    for peering in netixlan_info_dict:
        ixid = peering['ix_id']
        speed = peering['speed']
        name = peering['name']

        for ix in ix_info_dict:
            if ix['ixid'] == ixid:
                ix['speed'] += speed
                break
        else:
            ix_info_dict.append( {'ixid' : ixid, 'speed' : speed, 'name' : name} )

        total_speed += speed

#        print '-'*60
#        print "PeeringIXID:\t" + str(ixid)
#        print "PeeringName:\t" + name
#        print "PeeringSpeed:\t" + str(speed)
#    print '='*60

    org_info_dict = []

    print "\nList of IXs"
    for ix in ix_info_dict:
        print '-'*60
        print "IX ID:\t\t" + str(ix['ixid'])
        print "PopName:\t" + ix['name']
        print "Speed:\t\t" + str(ix['speed'])

        for org in org_info_dict:
            if re.match(org['name'], ix['name']):
                org['speed'] += ix['speed']
                break
        else:
            for pattern in OrgList:
                if re.match(pattern, ix['name']):
                    org_info_dict.append( {'speed' : ix['speed'], 'name' : pattern} )
                    break
            else:
                warn_msg += 'CAUTION: IX name ' + ix['name'] + ' is not found in OrgList.\n'

    print '='*60

    print "\nList of IX Orgs"
    print '='*60
    for org in org_info_dict:
        if len(org['name']) >= 8:
            print "Org:\t" + org['name'] + "\tSpeed:\t" + str(org['speed'])
        else: 
            print "Org:\t" + org['name'] + "\t\tSpeed:\t" + str(org['speed'])
    print '='*60

    print "\nGlobal Total Speed of AS " + as_num + ', ' + company_name
    print '='*60
    print "TotalSpeed:\t" + str(total_speed)
    print '='*60
    print warn_msg
