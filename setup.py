def main():
    print("Stating the installation process...")
    import os
    print("Installing requirements...")
    test_for_pip = os.popen("pip3")
    if "Usage" in test_for_pip.read():
        print("Yes")
    else:
        print("Installing pip3")
        os.system("sudo apt install python3-pip -y")
    os.system("pip3 install colorama requests urllib3")
    print("Done:\n \
    pybuster usage: pybuster http[s]://domain.com/ wordlist_path\nIt will then open a menu for you.")


if __name__ == '__main__':
    main()
