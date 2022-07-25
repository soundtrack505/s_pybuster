#!/usr/bin/python3

from urllib3 import disable_warnings
import requests
# from colorama import Fore, Back, Style
from threading import Thread
import os
import sys


def new_thread(url, wlt, se):
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
                    exten = extension.split(',')

                    for ext in exten:
                        # print(f'{line}.{ext}')
                        if ext == "":
                            ext = ext
                        else:
                            ext = "." + ext
                        try:
                            r = ses.get(url + line + ext, allow_redirects=True, verify=False, timeout=0.5)
                            # print(r.url)
                        except Exception as e:
                            print(e)
                            r = ses.get(url + line + ext, allow_redirects=True, verify=False)

                        if r.status_code in range(400, 499):
                            if f'.{ext}' in r.url and "Access" in r.text or "Forbidden" in r.text:
                                print(f"\n[-] Found /{line}{ext} file but you don't have access to it\n")
                            elif "Access" in r.text or "Forbidden" in r.text:
                                print(f"\n[-] Found /{line} directory but you don't have access to it\n")
                            else:
                                continue

                        elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                            url_counter = url.count('/') + line.count('/')
                            if f'.{ext}' in r.url:
                                print(f"\n[+] Found file /{line}{ext} -> [URL: {r.url} | \
Content_Length: {len(r.content)} | Status_code: {r.status_code}]\n")
                            else:
                                print(f"\n[+] Found directory /{line} -> [URL: {r.url} | Content_Length:\
 {len(r.content)} | Status_code: {r.status_code}]\n")

                                if url_counter <= 4:
                                    t = Thread(target=new_thread, args=(url + line + '/', ses, wordlist))
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
                        print(f"\n[+] Found directory /{w} -> [url: {req.url} | content_length: {len(req.content)} |\
 status_code: {req.status_code}]\n")

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
    url_list = []
    print(f'[+] Attacking target: {url}')
    index = 1
    with open(wordlist, 'r') as f:
        f = f.readlines()
        sum_lines = len(f)

        while True:
            try:
                for line in f:
                    line = line.replace('\n', '')
                    sys.stdout.write('\r' + f"Progress: {index}/{sum_lines}")
                    index += 1
                    try:
                        r = session.get(url + line, allow_redirects=True, verify=False, timeout=0.5)
                        if url + line in url_list:
                            continue
                    except Exception as e:
                        print(e)
                        r = session.get(url + line, allow_redirects=True, verify=False)
                        if url + line in url_list:
                            continue

                    if r.status_code in range(400, 499):
                        if "Access" in r.text or "Forbidden" in r.text:
                            print(f"\n[-] Found /{line} directory but you don't have access to it\n")
                            print(f"URL: {r.url} | Status_code: {r.status_code}")
                            url_list.append(url + line)
                        else:
                            continue

                    elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                        url_counter = url.count('/') + line.count('/')
                        print(f"\n[+] Found directory /{line} -> [URL: {r.url} | Content_Length: {len(r.content)} \
| Status_code: {r.status_code}]\n")
                        url_list.append(url + line)
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
                        print(f"\n[+] Found directory /{line} -> [URL: {r.url} | Content_Length: {len(r.content)} \
| Status_code: {r.status_code}]\n")
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


def follow_403(url, wordlist, session):
    
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


def docs():
    print("""
Normal Scan:
    Will scan the URL given and will go recursive only once.
    This scan is good if you don't want to crash the website.
    For example, if you scan http://localhost/ and you find admin/ dir, then the code will try to find every thing
    inside admin/ directory.
    
Full recursive Scan:
    Will scan the URL given and will go recursively for every directory it finds.
    For example, if you scan http://localhost/ and you find admin/ dir, then the code will try to find everything inside
    all the folders it finds: admin/ -> admin/dashboard/ -> admin/dashboard/index etc.
    
Follow 403 Scan:
    When you get 403 error code you can still find files that are in this folder.
    For example, if you scan http://localhost/ and you find admin/ dir but you get 403 error,
    then the code will try to find the files with extension you gave it to search.


Fixed length Scan:
    Website sometimes uses a redirect page which will give you status code of 200 but there is actually nothing in there
    so to avoid that you can set a fixed length and if the code catches that it will ignore it.

Extension Scan:
    If you want to find files with specific extensions, you can add them for the scan and it will try to find them.

""")
    input("Press enter to continue...")


if __name__ == '__main__':
    disable_warnings()
    session = requests.Session()
    auto_save = "off"
    try:
        url = sys.argv[1]
        wordlist = sys.argv[2]
    except IndexError:
        print("Usage: pybuster.py http[s]://domain.com/ wordlist_path\nIt will then open a menu for you.")
        exit()

    amount_of_lines = os.popen("wc " + wordlist).read().split(" ")[1]
    # Menu
    while True:
        os.system("clear")
        try:
            menu = input(f"""
URL: {url}
wordlist: {wordlist}  |  amount of lines: {amount_of_lines}
AutoSave: {auto_save}

Type help to see what every thing does.

0)  exit                         # Will exit the program.
1)  Normal Scan                  # Will scan recursive only once.
2)  Full Recursive Scan          # Will go inside every directory it finds.
3)  Follow 403 Scan              # Will follow the 403 to find files or dirs.
4)  Fixed length Scan            # Will ignore page with the fixed length.
5)  Extension Scan               # Will add an extensions to your wordlist.
99) Auto Save Output             # Will auto save your work to a file.
⋊> """)

            if menu.lower() == "help":
                docs()

            if menu == '0':
                print("Exiting....")
                exit()
            
            elif menu == '1':
                main(url, wordlist, session)
            
            elif menu == '2':
                full_recursive(url, wordlist, session)
            
            elif menu == '3':
                follow_403(url, wordlist, session)
            
            elif menu == '4':
                fixed_length_number = input("Enter the fixed number > ")
                fixed_length(url, wordlist, session, fixed_length_number)

            elif menu == '5':
                print("Use , to separate the words:               # Don't use spaces!!!\nExample: php,txt,html,aspx...")
                extension_input = input("Enter the extensions > ")
                if " " in extension_input:
                    print("Space was detected.")
                else:
                    extension_input += "," + ""
                    extensions(url, wordlist, session, extension_input)

            elif menu == '99':
                if auto_save == 'On':
                    auto_save = 'Off'
                else:
                    auto_save = "On"

        except KeyboardInterrupt:
            a = input("\nAre you sure you want to exit the main program? Y/n > ")
            if a.lower() == "y" or a == "":
                print("\nExiting...")
                sys.exit(0)
            else:
                continue

"""
## Need to copy new_thread and create it for the fixed length one.
## Do a multiple selection like: if the user will input 1,4 do a for loop and open a thread for every one of those 
   selections. (Need to check how to display it.)
"""
