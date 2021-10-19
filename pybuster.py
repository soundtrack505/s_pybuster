#!/usr/bin/python3
import time

from tqdm import tqdm
import urllib3
import requests
from random import choice
import argparse
# import colorama
from threading import Thread
import sys


def extensions(url, wordlist, extension):
    urllib3.disable_warnings()
    pass


def fixed_length(url, wordlist, se, size):
    urllib3.disable_warnings()
    with open(wordlist, 'r') as wl:
        while True:
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
                        and len(req.content > {size}):
                    url_counter = url.count('/') + w.count('/')
                    print(f"\n[+] Found directory /{w} -> [{req.url} | {len(req.content)}]\n")

                    if url_counter <= 4:
                        pass
                        # t = Thread(target=new_thread, args=(url + w + '/', s, wordlist))
                        # t.daemon = True
                        # t.start()
                    else:
                        continue
                else:
                    continue
            break


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
                        t = Thread(target=new_thread, args=(url + w + '/', s, wlt))
                        t.daemon = True
                        t.start()
                    else:
                        continue
                else:
                    continue
            break


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
                        else:
                            continue

                    elif r.status_code in range(200, 299) or r.status_code in range(300, 399):
                        url_counter = url.count('/') + line.count('/')
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
                    sys.exit()
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
    s = requests.Session()

    parser = argparse.ArgumentParser(description="PyBuster")
    # parser.parse_args()

    parser.add_argument('url', type=str, help='Target URL')
    parser.add_argument('wordlist', type=str, help='Wordlist path')
    parser.add_argument('-x', action='store_true', help='Add extensions for the files: php,html,cgi,aspx...')
    parser.add_argument('-F', action='store_true', help='This will search dirs in 404 pages')
    parser.add_argument('-f', action='store_true', help='This will go full recursive on the target')

    # parser.add_argument('-u', '--url', help='Target URL')
    # parser.add_argument('-w', '--wordlist', help='Wordlist to attack with')

    args = parser.parse_args()

    if args.url and args.wordlist:
        main(args.url, args.wordlist, s)
    else:
        print(parser.print_help())

