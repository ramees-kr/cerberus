from scapy.all import DNS, DNSQR, sniff

def extract_domain_name(pkt):
    if DNS in pkt and pkt[DNS].qr == 0:  # if the captured packet is a DNS query, the qr=0
        qname = pkt[DNSQR].qname.decode()  # Extract the query name (domain) and decode it from bytes to a string
        print(f"DNS Query for: {qname}")

# Sniff DNS packets on the network interface (e.g., 'eth0') and call extract_domain_name for each packet
sniff(filter="udp and port 53", prn=extract_domain_name)

#sniff(filter="udp and port 53 and dst host YOUR_SERVER_IP", prn=extract_domain_name)