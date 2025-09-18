# Advanced FTP Brute Force Tool 🔐

A Python tool for **FTP password testing** in controlled environments.  
This project is **intended only for educational purposes, penetration testing on authorized systems, and lab experiments**.  
**Never use this tool against systems you do not own or have explicit permission to test. Unauthorized access is illegal.**

---

## Features

- Brute-force FTP login attempts with username and password combinations.
- Supports:
  - Single username
  - Username lists
  - Password wordlists
  - On-the-fly password generation
- Multi-threaded for faster testing.
- Handles common FTP errors and connection resets.
- Colored output for easy readability using `colorama`.

---

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/advanced_ftp_bruteforce.git
cd advanced_ftp_bruteforce
Install required packages:
pip install -r requirements.txt

Dependencies:
Python 3.x
ftplib (built-in)
colorama

Usage:
python advanced_ftp_brute.py --host <FTP_HOST> [options]

Options:
Option	Description
--host	Target FTP server IP or hostname (required)
--port	FTP port (default: 21)
-t, --threads	Number of threads (default: 30)
-u, --user	Single username
-U, --userlist	File containing a list of usernames
-w, --wordlist	File containing a list of passwords
-g, --generate	Generate passwords on the fly
--min_length	Minimum password length (default: 1)
--max_length	Maximum password length (default: 4)
-c, --chars	Characters to use for password generation (default: letters + digits)


Safety & Legal Disclaimer ⚠️
Do NOT use this tool on any system you do not own or have explicit permission to test.

Only use in lab environments or authorized penetration tests.

Unauthorized use is illegal and may result in criminal charges.

This tool is intended for learning purposes: understanding password security, testing weak credentials, and improving defense mechanisms.

