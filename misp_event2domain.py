#############################################
# MISP API Domain to Event
# 
# Author: Emmanuel Bouillon
# Email:  emmanuel.bouillon.sec@gmail.com
# Date: 24/11/2015
#############################################
import sys
from misp_util import *
from pymisp import PyMISP

type2attribute = {'domain':('domain','hostname'), 'hostname':('hostname'), 'url':('url'), 'hash':('md5','sha1','sha256') , 'ip':('ip-src','ip-dst'), 'email':('email-src','email-dst'), 'email-subject': ('email-subject')}
argType2enType = {'domain':'maltego.Domain', 'hostname':'maltego.Domain', 'url':'maltego.Phrase', 'hash':'maltego.Hash', 'ip':'maltego.IPv4Address', 'email':'maltego.EmailAddress', 'email-subject': 'maltego.Phrase'}
filename_pipe_hash_type = ('filename|md5', 'filename|sha1', 'filename|sha256', 'malware-sample')

if __name__ == '__main__':
        event_id = sys.argv[1]
        argType = sys.argv[0].split('.')[0].split('2')[1] # misp_event2argType.py
        misp = init()
        mt = MaltegoTransform()
        try:
            event = misp.get_event(event_id)
            for attribute in event['Event']["Attribute"]:
                value = attribute["value"]
                aType = attribute["type"]
                if aType in type2attribute[argType]:
                    if aType in filename_pipe_hash_type:
                        h = value.split('|')[1].strip()
                        me = MaltegoEntity(argType2enType[argType], h)
                    else:
                        me = MaltegoEntity(argType2enType[argType], value)

                    mt.addEntityToMessage(me)

            # support new MISP event Object
            for obj in event['Event']['Object']:
                for attribute in obj['Attribute']:
                    value = attribute["value"]
                    aType = attribute["type"]
                    if aType in type2attribute[argType]:
                        if aType in filename_pipe_hash_type:
                            h = value.split('|')[1].strip()
                            me = MaltegoEntity(argType2enType[argType], h)
                        else:
                            me = MaltegoEntity(argType2enType[argType], value)

                        mt.addEntityToMessage(me)

        except Exception as e:
	       mt.addUIMessage("[ERROR]  " + str(e))
        mt.returnOutput()
