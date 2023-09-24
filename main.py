
#imports
import json
import flask

#import socketIO to use flask and scapy at the same time
from flask_socketio import SocketIO, send

#import scapy to receive and read DNS packets
import scapy.all as scapy

#import additional scapy objects
from scapy.all import DNS, DNSQR

class Domain:
    def __init__(self,url,isMalicious) -> None:
        self.url = url
        self.isMalicious = isMalicious
    
    def serialize():
        return {"Domain": {'url':self.url,
                           'isMalicious':self.isMalicious}}
    
def findByURL(urlList,searchUrl):
        for url in urlList:
            if url.url == searchUrl:
                #todo: replace this
                print("found it")
                return url



domainList = []
#start flask
SERVER = flask.Flask(__name__)
#start socketIO
socketIO = SocketIO(SERVER)

#create the routes
@SERVER.route('/')
def index():
    #send data in the json format to the view to be read and displayed by javascript
    return flask.render_template("index.html",urlList=domainList)

#when the user clicks on the delete button, have them redirect to this link so 
@SERVER.route('/change/<url>')
def change_url(url):
    domain = findByURL(domainList,url)

    #verify that the domain found on the list is not null
    if domain is None:
        #if domain is null redirect to an error page
        return flask.render_template("error.html", message="Unable to find domain in list")
    else:
        #todo: finish implementing json serialization
        domainList[domainList.index(domain)].isMalicious = not domainList[domainList.index(domain)].isMalicious
        return flask.redirect('/')


    
#runs every time scapy finds a domain
def extract_domain_name(pkt):
    if DNS in pkt and pkt[DNS].qr == 0:  # if the captured packet is a DNS query, the qr bit=0
        qname = pkt[DNSQR].qname.decode()  # Extract the query name (domain) and decode it from bytes to a string
        print(f"DNS Query for: {qname}")
                
        #make sure the domain has not already been checked
        if findByURL(domainList,qname) is None:
            #TODO: implement AI model filtering
            domainList.append(Domain(qname,False))
        else:
            #if the domain has already been checked use the boolean stored in domainList to know if it should
            # be blocked or not
            domain = findByURL(domainList,qname)
            if domain.isMalicious:
                #todo: find a way to drop packets here

            



#run the app
if __name__ == '__main__':
    SERVER.debug = True
    socketIO.start_background_task(scapy.sniff,prn=extract_domain_name)
    socketIO.run(SERVER)
    # Sniff DNS packets on the network interface (e.g., 'eth0') and call extract_domain_name for each packet
    sniff(filter="udp and port 53", prn=extract_domain_name)

    



