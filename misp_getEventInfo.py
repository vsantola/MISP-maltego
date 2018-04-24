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

if __name__ == '__main__':
        misp = init()
        mt = MaltegoTransform()
        event_id = sys.argv[1]
        try:
            event = misp.get_event(event_id)
            eid = event['Event']['id']
            einfo = event['Event']['info']
            eorgc = event['Event']['Orgc']['name']
            me = MaltegoEntity('maltego.MISPEvent', eid)
            me.addAdditionalFields('EventLink', 'EventLink', False, BASE_URL + '/events/view/' + eid )
            me.addAdditionalFields('Org', 'Org', False, eorgc)
            me.addAdditionalFields('notes#', 'notes', False, eorgc + ": " + str(einfo))
            mt.addEntityToMessage(me)
        except Exception as e:
	       mt.addUIMessage("[ERROR]  " + str(e))
        mt.returnOutput()
