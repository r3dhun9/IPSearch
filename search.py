import sys
import subprocess
import signal

title = """

    ________  _____                      __
   /  _/ __ \/ ___/___  ____ ___________/ /_
   / // /_/ /\__ \/ _ \/ __ `/ ___/ ___/ __ \\
 _/ // ____/___/ /  __/ /_/ / /  / /__/ / / /
/___/_/    /____/\___/\__,_/_/   \___/_/ /_/


An automatic ip searching tool by Redhung aka r3dhun9.
Contact: redhung@hung.red
"""

ip_list = []

def handler(signal, frame):
    print("\n[+] IP Search done.")
    if len(ip_list) != 0:
        with open("output.txt", "wb") as fd:
            new_list = "\n".join(ip_list)
            fd.write(new_list)
        print("[+] Please check output.txt.")
    else:
        print("[-] No IP alive.")
    sys.exit()

def search_24(ip):
    signal.signal(signal.SIGINT, handler)
    for i in range(1, 256):
        c_ip = ip.split('.')
        c_ip = c_ip[0] + '.' + c_ip[1] + '.' + c_ip[2] + '.' + str(i)
        cmd = "ping -c 1 -t 1 " + c_ip
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        buf = p.stdout.read()
        if buf.find("from") != -1:
            print("[!] Found the alive target: " + c_ip)
            ip_list.append(c_ip)

def search_16(ip):
    signal.signal(signal.SIGINT, handler)
    for i in range(1, 256):
        for j in range(1, 256):
            c_ip = ip.split('.')
            c_ip = c_ip[0] + '.' + c_ip[1] + '.' + str(i) + '.' + str(j)
            cmd = "ping -c 1 -t 1 " + c_ip
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            buf = p.stdout.read()
            if buf.find("from") != -1:
                print("[!] Found the alive target: " + c_ip)
                ip_list.append(c_ip)

def search_8(ip):
    signal.signal(signal.SIGINT, handler)
    for i in range(1, 256):
        for j in range(1, 256):
            for k in range(1, 256):
                c_ip = ip.split('.')
                c_ip = c_ip[0] + '.' + str(i) + '.' + str(j) + '.' + str(k)
                cmd = "ping -c 1 -t 1 " + c_ip
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                buf = p.stdout.read()
                if buf.find("from") != -1:
                    print("[!] Found the alive target: " + c_ip)
                    ip_list.append(c_ip)

def main():
    print(title)
    if len(sys.argv) != 3:
        print("[!] Usage: python search.py <ip> <netmask>")
        print("[!] E.g. python search.py 192.168.0.0 255.255.255.0")
        sys.exit()
    ip = sys.argv[1]
    netmask = sys.argv[2]
    print("[+] Start searching ...")
    print("[+] You may press Ctrl+C to interrupt the process and get the current result.")
    if netmask == "255.255.255.0":
        search_24(ip)
    elif netmask == "255.255.0.0":
        search_16(ip)
    elif netmask == "255.0.0.0":
        search_8(ip)
    else:
        print("[-] Error: Netmask out of range.")
        sys.exit()
    print("[+] IP Search done.")
    if len(ip_list) != 0:
        with open("output.txt", "wb") as fd:
            new_list = "\n".join(ip_list)
            fd.write(new_list)
        print("[+] Please check output.txt.")
    else:
        print("[-] No IP alive.")

if __name__ == '__main__':
    main()
