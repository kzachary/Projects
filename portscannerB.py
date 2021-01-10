import socket
import termcolor

line = '-'*80

def scan(target, ports, status):
    for port in range(1,ports + 1):
        scan_port(target, port, status)

def scan_port(addr, port, status):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((addr, port))
        if status == 1:
            decBanner = banner_grab(s)
        print(termcolor.colored((line), 'blue'))
        print("[+] " + str(port) + " : open")
        if status == 1:
            print(decBanner)
        print(termcolor.colored((line), 'blue'))
        s.close()
    except socket.error as socketerror:
        pass
        #print("[-] " + str(port) + " : closed")

def banner_grab(sock):
    sock.send(b'WhoAreYou\r\n')
    try:
        banner = sock.recv(1024)
    except:
        return
    try:
        decBanner = banner.decode()
    except UnicodeDecodeError:
        try:
            decBanner = banner.decode('utf-16')
        except UnicodeDecodeError:
            try:
                decBanner = banner.decode('utf-32')
            except UnicodeDecodeError:
                decBanner = "Unable to decode"
    return decBanner

targets = input("Enter targets to scan split by comma: ")
while True:
    ports = int(input("How many ports to scan: "))
    if ports <= 65535:
        break
    else:
        print("Number must be 65535 or less")
status = 0
grabBan = input("Attempt to grab banners? y/n: ")
if grabBan == 'y' or grabBan == 'Y':
    status = 1
print(termcolor.colored(('\n' + targets), 'red'))
if ',' in targets:
    print(termcolor.colored(("[*] Scanning multiple targets"), 'red'))
    for ip_addr in targets.split(','):
        print(termcolor.colored(("\nScanning " + ip_addr + " :"), 'red'))
        scan(ip_addr.strip(' '), ports, status)
else:
    scan(targets, ports, status)


