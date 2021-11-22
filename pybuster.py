#!/usr/bin/python3

"""
Created by: Yerom Hemo
Point: I was sick from gobuster and dirb not going recursive as soon as they find a hit so I created this program
I will try to make it faster in the future.
"""

import urllib3
import requests
# import colorama
from threading import Thread
import sys


def new_thread(url, wlt, se):
    urllib3.disable_warnings()
    with open(wlt, 'r') as wl:
        while True:
            for w in wl.readlines():
                w = w.replace('\n', '')

                try:
                    req = se.get(url + w, allow_redirects=True, verify=False, timeout=0.5)
                except Exception:
                    req = se.get(url + w, allow_redirects=True, verify=False)

                if req.status_code in range(400, 499):
                    if "Access" in req.text or "Forbidden" in req.text:
                        print(f"\n[-] Found {url.split('/')[3]}/{w}  directory but you don't have access to it\n")
                    else:
                        # print(line)
                        continue

                elif req.status_code in range(200, 299) or req.status_code in range(300, 399):
                    urlc = url.count('/') + w.count('/')
                    print(f"\n[+] Found directory {url.split('/')[3]}/{w} -> [{req.url} | {len(req.content)}]\n")

                    if urlc <= 4:
                        t = Thread(target=new_thread, args=(url + w + '/', wlt, se))
                        t.daemon = True
                        t.start()
                    else:
                        continue
                else:
                    continue
            break


def extensions(url, wordlist, ses, extension):
    urllib3.disable_warnings()
    print(f'[+] Attacking target: {url}')
    index = 1
    with open(wordlist, 'r') as f:
        f = f.readlines()
        sum_lines = len(f)

        while True:
            try:
                for line in f:
                    line = line.replace('\n', '')
                    sys.stdout.write('\r' + f"Prograss: {index}/{sum_lines}")
                    index += 1
                    for ext in extension:
                        print(f'{line}.{ext}')
                        try:
                            r = ses.get(url + line + f'.{ext}', allow_redirects=True, verify=False, timeout=0.5)
                        except Exception as e:
                            print(e)
                            r = ses.get(url + line + f'.{ext}', allow_redirects=True, verify=False)

                        if r.status_code in range(400, 499):
                            if f'.{ext}' in r.url and "Access" in r.text or "Forbidden" in r.text:
                                print(f"\n[-] Found /{line}.{ext} file but you don't have access to it\n")
                            elif "Access" in r.text or "Forbidden" in r.text:
                                print(f"\n[-] Found /{line} directory but you don't have access to it\n")
                            else:
                                continue

                        elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                            url_counter = url.count('/') + line.count('/')
                            if f'.{ext}' in r.url:
                                print(f"\n[+] Found file /{line}.{ext} -> [{r.url}.{ext} | {len(r.content)}]\n")
                            else:
                                print(f"\n[+] Found directory /{line} -> [{r.url} | {len(r.content)}]\n")

                                if url_counter <= 4:
                                    t = Thread(target=new_thread, args=(url + line + '/', session, wordlist))
                                    t.daemon = True
                                    t.start()
                                else:
                                    continue
                        else:
                            continue

                    print("[+] Done!!\nHappy Hacking")
                    break

            except KeyboardInterrupt:
                done = input("\n[+] Keyboard interrupt detected, do you really want to quit? Y/n -> ")
                if done.lower() == 'y':
                    break
                else:
                    continue


def fixed_length(url, wordlist, se, size):
    urllib3.disable_warnings()
    with open(wordlist, 'r') as wl:
        while True:
            try:
                for w in wl.readlines():
                    w = w.replace('\n', '')

                    try:
                        req = se.get(url + w, allow_redirects=True, verify=False, timeout=0.5)
                    except Exception:
                        req = se.get(url + w, allow_redirects=True, verify=False)

                    if req.status_code in range(400, 499):
                        if "Access" in req.text or "Forbidden" in req.text:
                            print(f"\n[-] Found /{w}  directory but you don't have access to it\n")
                        else:
                            # print(line)
                            continue

                    elif req.status_code in range(200, 299) or req.status_code in range(300, 399) \
                            and len(req.content) > size:
                        url_counter = url.count('/') + w.count('/')
                        print(f"\n[+] Found directory /{w} -> [url: {req.url} |status_code: {req.status_code} \
                        | content_length: {len(req.content)}]\n")

                        if url_counter <= 4:
                            pass
                            # t = Thread(target=new_thread, args=(url + w + '/', s, wordlist))
                            # t.daemon = True
                            # t.start()
                        else:
                            continue
                    else:
                        continue
            except KeyboardInterrupt:
                done = input("\n[+] Keyboard interrupt detected, do you really want to quit? Y/n -> ")
                if done.lower() == 'y':
                    break
                else:
                    continue


def main(url, wordlist, session):
    urllib3.disable_warnings()
    print(f'[+] Attacking target: {url}')
    index = 1
    with open(wordlist, 'r') as f:
        f = f.readlines()
        sum_lines = len(f)

        while True:
            try:
                for line in f:
                    line = line.replace('\n', '')
                    sys.stdout.write('\r' + f"Prograss: {index}/{sum_lines}")
                    index += 1
                    try:
                        r = session.get(url + line, allow_redirects=True, verify=False, timeout=0.5)
                    except Exception as e:
                        print(e)
                        r = session.get(url + line, allow_redirects=True, verify=False)

                    if r.status_code in range(400, 499):
                        if "Access" in r.text or "Forbidden" in r.text:
                            print(f"\n[-] Found /{line}  directory but you don't have access to it\n")
                        else:
                            continue

                    elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                        url_counter = url.count('/') + line.count('/')
                        print(f"\n[+] Found directory /{line} -> [{r.url} | {len(r.content)}]\n")

                        if url_counter <= 4:
                            t = Thread(target=new_thread, args=(url + line + '/', wordlist, session))
                            t.daemon = True
                            t.start()

                        else:
                            continue
                    else:
                        continue

                print("[+] Done!!\nHappy Hacking")
                break

            except KeyboardInterrupt:
                done = input("\n[+] Keyboard interrupt detected, do you really want to quit? Y/n -> ")
                if done.lower() == 'y':
                    break
                else:
                    continue


def full_recursive(url, wordlist, session):
    urllib3.disable_warnings()
    print(f'[+] Attacking target: {url}')
    index = 1
    with open(wordlist, 'r') as f:
        f = f.readlines()
        sum_lines = len(f)

        while True:
            try:
                for line in f:
                    line = line.replace('\n', '')
                    sys.stdout.write('\r' + f"Prograss: {index}/{sum_lines} -> /{line}")
                    index += 1
                    try:
                        r = session.get(url + line, allow_redirects=True, verify=False, timeout=0.5)
                    except Exception as e:
                        print(e)
                        r = session.get(url + line, allow_redirects=True, verify=False)

                    if r.status_code in range(400, 499):
                        if "Access" in r.text or "Forbidden" in r.text:
                            print(f"\n[-] Found /{line}  directory but you don't have access to it\n")
                            t = Thread(target=new_thread, args=(url + line + '/', session, wordlist))
                            t.daemon = True
                            t.start()
                        else:
                            continue

                    elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                        print(f"\n[+] Found directory /{line} -> [{r.url} | {len(r.content)}]\n")
                        t = Thread(target=new_thread, args=(url + line + '/', session, wordlist))
                        t.daemon = True
                        t.start()
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


def follow_404(url, wordlist, session):
    urllib3.disable_warnings()
    print(f'[+] Attacking target: {url}')
    index = 1
    with open(wordlist, 'r') as f:
        f = f.readlines()
        sum_lines = len(f)

        while True:
            try:
                for line in f:
                    line = line.replace('\n', '')
                    sys.stdout.write('\r' + f"Prograss: {index}/{sum_lines} -> /{line}")
                    index += 1
                    try:
                        r = session.get(url + line, allow_redirects=True, verify=False, timeout=0.5)
                    except Exception as e:
                        print(e)
                        r = session.get(url + line, allow_redirects=True, verify=False)

                    if r.status_code in range(400, 499):
                        if "Access" in r.text or "Forbidden" in r.text:
                            print(f"\n[-] Found /{line}  directory but you don't have access to it")
                            t = Thread(target=new_thread, args=(url + line + '/', session, wordlist))
                            t.daemon = True
                            t.start()
                        else:
                            continue

                    elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                        url_counter = url.count('/') + line.count('/')
                        print(f"\n[+] Found directory /{line} -> [{r.url} | {len(r.content)}]")

                        if url_counter <= 4:
                            t = Thread(target=new_thread, args=(url + line + '/', session, wordlist))
                            t.daemon = True
                            t.start()
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
    # When I open the menu I need to open a new terminal for it like my other project.
    try:
        session = requests.Session()
        url = sys.argv[1]
        wordlist = sys.argv[2]
        auto_save = "off"
    except IndexError:
        print("Usage: pybuster.py http[s]://domain.com/ wordlist_path\nIt will then open a menu for you.")
        exit()
    # Menu 
    while True:
        try:
            menu = input(f"""
URL: {url}
wordlist: {wordlist}
AutoSave: {auto_save}

0)  exit                         # Will exit the program.
1)  Normal Scan                  # Will scan recursive only once.
2)  Full Recursive Scan          # Will go inside every directory it finds.
3)  Follow 404 Scan              # Will follow the 404 to find files or dirs.
4)  Fixed length Scan            # Will ignore page with the fixed length.
99) Auto Save Output             # Will auto save your work to a file.
> """)

            if menu == '0':
                print("Exiting....")
                exit()
            
            elif menu == '1':
                main(url, wordlist, session)
            
            elif menu == '2':
                pass
            
            elif menu == '3':
                pass
            
            elif menu == '4':
                fixed_length_number = input("Enter the fixed number > ")
                fixed_length(url, wordlist, session, fixed_length_number)

            if menu == '99':
                if auto_save == 'On':
                    auto_save = 'Off'
                else:
                    auto_save = "On"

        except KeyboardInterrupt:
            a = input("Are you sure you want to exit the main program? Y/n > ")
            if a.lower() == "y":
                print("\nExiting...")
                break
            else:
                continue
                
"""
in the setup.py add a line that add to the .bashrc and the .zshrc an alias
alias pybuster="python3.9 /opt/pybuster.py"
need to change the location of the script to opt
"""