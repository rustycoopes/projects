'''
Created on Oct 15, 2013

@author: rusty
'''
from russpandora import RussPandora
import httplib
import logging

SOAP_TEMPLATEOLD = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
<ns1:AddURIToQueue xmlns:ns1="urn:schemas-upnp-org:service:AVTransport:1">
              <InstanceID>0</InstanceID>
              <EnqueuedURI>x-file-cifs://Rainbow-Media/QRecordings/jukebox/%s.mp3</EnqueuedURI>
              <EnqueuedURIMetaData></EnqueuedURIMetaData>
              <DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued>
              <EnqueueAsNext>1</EnqueueAsNext>
        </ns1:AddURIToQueue>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

'<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>{uri}</CurrentURI><CurrentURIMetaData>{meta}</CurrentURIMetaData></u:SetAVTransportURI>'


SOAP_TEMPLATE = """ <?xml version="1.0" encoding="UTF-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>pndrradio:%s</CurrentURI><CurrentURIMetaData></CurrentURIMetaData></u:SetAVTransportURI>'</s:Body></s:Envelope>"""
SOAPACTION_PLAY = "urn:schemas-upnp-org:service:AVTransport:1#Play"

SOAP_TEMPLATE_PLAY = """<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Body><ns1:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></ns1:Play></SOAP-ENV:Body></SOAP-ENV:Envelope>"""
class SonosPandora(object):
    '''
    classdocs
    '''
    

    rpandora = None

    def __init__(self):
        '''
        Constructor
        '''
    def playStation(self, stationNameLike): 
        if self.rpandora is None:
            self.rpandora = RussPandora()
            
        stationId = self.rpandora.getIdForStation(stationNameLike)
        
        if stationId > 0:           
                  
            SoapMessage = SOAP_TEMPLATE%(str(stationId))
            logging.info(SoapMessage)
            webservice = httplib.HTTP("192.168.2.14:1400")
            webservice.putrequest("POST", "/MediaRenderer/AVTransport/Control")
            webservice.putheader("Host", "192.168.2.14:1400")
            webservice.putheader("User-Agent", "Linux UPnP/1.0 Sonos/24.0-69180 (MDCR_iMac9,1)")
            webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
            webservice.putheader("Content-length", "%d" % len(SoapMessage))
            webservice.putheader("CONNECTION", "Close")
            webservice.putheader("SOAPACTION", "urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI")
            webservice.endheaders()
            webservice.send(SoapMessage)
            
            SoapMessage = SOAP_TEMPLATE_PLAY
            logging.info(SoapMessage)
            webservice = httplib.HTTP("192.168.2.14:1400")
            webservice.putrequest("POST", "/MediaRenderer/AVTransport/Control")
            webservice.putheader("Host", "192.168.2.14:1400")
            webservice.putheader("User-Agent", "Russ Pandora Script")
            webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
            webservice.putheader("Content-length", "%d" % len(SoapMessage))
            webservice.putheader("SOAPACTION", SOAPACTION_PLAY)
            webservice.endheaders()
            webservice.send(SoapMessage)
            print 'sent'
            
            
            
if __name__ == "__main__":
  
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='sonos-jukebox-server.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)    
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)    
    sonos = SonosPandora()
    sonos.playStation('Rod')
    



