def main():
    print("Stating the installation process...")
    import os
    print("Copying pybuster.py to /opt/.pybuster.py")
    os.system("sudo cp pybuster.py /opt/.pybuster.py")
    print("Installing requirements...")
    test_for_pip = os.popen("pip3")
    if "Usage" in test_for_pip.read():
        print("Yes")
    else:
        print("Installing pip3")
        os.system("sudo apt install python3-pip -y")
    os.system("pip3 install colorama requests urllib3")
    os.system("""echo 'alias pybuster="python3 /opt/.pybuster.py"' >> ~/.zshrc"'""")
    os.system("""echo 'alias pybuster="python3 /opt/.pybuster.py"' >> ~/.bashrc"'""")
    print("WHOOP WHOOP we are done\n \
    pybuster usage: pybuster http[s]://domain.com/ wordlist_path\nIt will then open a menu for you.")


if __name__ == '__main__':
    main()
