
#imports
import json
import flask

#import socketIO to use flask and scapy at the same time
from flask_socketio import SocketIO, send

#import scapy to receive and read DNS packets
import scapy.all as scapy

from model import Prediction

#import additional scapy objects
from scapy.all import DNS, DNSQR, sniff

class Domain:
    def __init__(self,url,isMalicious) -> None:
        self.url = url
        self.isMalicious = isMalicious
    
    
def findByURL(urlList,searchUrl):
        for url in urlList:
            if url.url == searchUrl:
                return url

#initiate a list that will store all the domains checked by scapy on it
domainList = []

#start flask for the dashboard
SERVER = flask.Flask(__name__)

#start socketIO for using scapy and flask at the same time
socketIO = SocketIO(SERVER)

#create the routes

#set the root route
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
        domainList[domainList.index(domain)].isMalicious = not domainList[domainList.index(domain)].isMalicious
        return flask.redirect('/')


    
#runs every time scapy finds a domain
def extract_domain_name(pkt):
    if DNS in pkt and pkt[DNS].qr == 0:  # if the captured packet is a DNS query, the qr bit=0
        qname = pkt[DNSQR].qname.decode()  # Extract the query name (domain) and decode it from bytes to a string
        
                
        #make sure the domain has not already been checked
        if findByURL(domainList,qname) is None:
            prediction = our_model.classify_website(str(qname))
            domainList.append(Domain(qname,not prediction))
        else:
            #if the domain has already been checked use the boolean stored in domainList to know if it should
            # be blocked or not
            domain = findByURL(domainList,qname)
            if domain.isMalicious:
                #todo: implement blocking
                print("bad domain")

            



#run the app
if __name__ == '__main__':
    our_model = Prediction()
    SERVER.debug = True
    # Sniff DNS packets on the network interface (e.g., 'eth0') and call extract_domain_name for each packet
    socketIO.start_background_task(scapy.sniff,prn=extract_domain_name)

    #run the server to support the dashboard
    socketIO.run(SERVER)



