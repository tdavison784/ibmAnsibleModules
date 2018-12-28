#!/usr/bin/python

DOCUMENTAION='''
Class that mocks the real IBM IMCL CLI tool
This class will create two files:
    1. repository.config
    2. internal.config
The repository.config file is the file that we would normally point to to install IBM products.
This file will have a entries that are the products install names. Ie. com.ibm.websphere.ND.v90_9.0.9.20180906_1004
The internal.config is where the installed products will end up, so that we can query if they exist or not.    

author: Tom Davison @tntdavison784
'''


def get_home():
    """Function that gets users home dir and returns value"""
    import os
    home = os.path.expanduser("~")
    return home


def check_files():
    """Function that checks for two files:
    1. repositroy.config
    2. internal.config
    if these files do not exist, it will create them.
    Base file creation goes to users home folder: /home/user/.internal.config
    """

    import os

    try:
        home = get_home()
        files = ['.repository.config', '.internal.config']
        for file in files:
            if os.path.exists(home+"/"+file):
                print("Repository files already exist.")
                break
            else:
                with open(home+"/"+file, "w+") as f_obj:
                    f_obj.close()
        return home
    except IOError:
        print("Permission denied, cannot create file in %s directory.") % home


def install_pckg(dest, name):
    """Function that will do a mock install of a package.
    This will first query the internal.config to see if anything exists.
    It will place all packages into an array to be compared to packages to be installed.
    This function will also be used for testing updates as logic is same.
    """

    usrhome = get_home()

    src = usrhome+"/.repository.config"

    repo_pack = []
    with open(src, 'r') as f_obj:
        packages = f_obj.readlines()
        repo_pack.append(packages)
        for package in repo_pack:
            if name in package:
                with open(usrhome + "/.internal.config", "r") as f_obj:
                    inst_packages = f_obj.readlines()
                    f_obj.close()
                    if len(inst_packages) == 0:
                        with open(usrhome + "/.internal.config", "w") as f:
                            new_pckg = name
                            f.writelines(new_pckg)
                            f.close()
                            print("Package " + name + " was successfully installed to " + dest + ".")
                    else:
                        for inst_package in inst_packages:
                            if name in inst_package:
                                print("Package " + name +" is already installed.")
                                break
                            else:
                                print('Unrecognized package in .internal.config. Please check.')
            else:
                print("Package: " + name + " not found. Check .repository config to ensure correct spelling.")
                break


def remove_pckg(dest, name):
    """Function that will remove package or packages from the .internal.config"""

    usrhome = get_home()

    src = usrhome+"/.internal.config"

    with open(src, "r") as f_obj:
        inst_packages = f_obj.readlines()
        f_obj.close()
        for inst_pckg in inst_packages:
            if name in inst_pckg:
                inst_packages.remove(inst_pckg)
                with open(src, "w") as f:
                    f.writelines(inst_packages)
                    f.close()
                print("Package " + name + " has been removed from " + dest)
            else:
                print("Package: " + name + " is not installed. Nothing to remove.")


#remove_pckg("/opt/WebSphere/AppServer", "com.ibm.websphere.ND.v90_9.0.9.20180906_1004")
install_pckg("/opt/WebSphere/AppServer", "com.ibm.websphere.ND.v90.9.0.10.20181228_1010")


#check_files()