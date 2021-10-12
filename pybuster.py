#!/usr/bin/python3

import os
import requests
# import argparse
# import colorama
import sys


def extensions(url, wordlist, extension):
    pass


def fixed_length(url, wordlist, size):
    pass


def main(url, wordlist, session):
    print(f'[+] Attacking target: {url}')
    index = 1
    with open(wordlist, 'r') as f:
        f = f.readlines()
        sum_lines = len(f)
        while True:
            try:
                for line in f:
                    line = line.replace('\n', '')
                    print(f"left: {index}/{sum_lines}   -> /{line}")
                    index += 1
                    try:
                        r = session.get(url + line, allow_redirects=True, verify=False, timeout=0.5)
                    except Exception:
                        r = session.get(url + line, allow_redirects=True, verify=False)

                    if r.status_code in range(400, 499):
                        if "Access Denied" in r.text or "Forbidden" in r.text:
                            print(f"[-] Found /{line}  directory but you don't have access to it")
                        else:
                            # print(line)
                            continue

                    elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                        urlc = url.count('/') + line.count('/')
                        print(f"[+] Found directory /{line} -> [{r.url} | {len(r.content)}]")

                        if urlc <= 4:
                            os.system(f"""terminator -T 'dir {line} '--new-tab -x 'python3 /home/$USER/pybuster/pybuster.py {url + line}/ {wordlist};echo "\n\033[1;33mPress ENTER to continue";read'""")
                            # Need to add status bar and a command that opens a new tab with a title of the dir found.
                        else:
                            continue
                    else:
                        continue

                print("[+] Done!!\nHappy Hacking")
                break

            except KeyboardInterrupt:
                done = input("\n[+] Keyboard interrupt detected, do you really want to quit? Y/n -> ")
                if done.lower() == 'y':
                    sys.exit()
                else:
                    continue


if __name__ == '__main__':
    # Need to add if the length of the page is the same and has 200 code then to leave it.
    # Need to add an option for fix length like: if the 404(200 code) page's length is 450 then do the command below:
    # if r.status_code in range(200, 299) and len(r.content > {user_fixed_size})

    # Need to add option for extensions -x php,html,sh.

    # Need to add full recursive(No restrict)

    # Need to add an option to follow recursive on 404 access denied or Forbidden. -F?

    # Need to add -n for no-tab(Not going recursive)

    # parser = argparse.ArgumentParser()
    # parser.parse_args()

    # url = "http://10.10.99.130/"
    # wordlist = "/home/soundtrack/Desktop/word.txt"

    if len(sys.argv) < 2:
        print("[-] usage pybuster.py <Target_IP> <Wordlist>")

    url = sys.argv[1]
    wordlist = sys.argv[2]

    s = requests.Session()

    main(url, wordlist, s)
