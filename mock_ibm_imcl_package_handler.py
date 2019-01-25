#!/usr/bin/python3

import sys

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
                break
            else:
                with open(home+"/"+file, "w+") as f_obj:
                    f_obj.close()
                    print("Created two hidden files under %s directory."%(home))
        return home
    except IOError:
        print("Permission denied, cannot create file in %s directory."%(home))


def get_avail_pckg():
    """
    Function to get all available packages. This function
    will query ~/.repository.config and return all values
    found from the file.
    """

    src = get_home()+"/.repository.config"

    with open(src, "r") as f_obj:
        pckgs_avail = f_obj.readlines()
        return pckgs_avail
    f_obj.close()


def get_inst_pckg():
    """
    Function to get list of packages installed. Function
    will query ~/.internal.config and return a list of
    installed packages.
    """

    src = get_home()+"/.internal.config"
    with open(src, "r") as f_obj:
        inst_pckgs = f_obj.readlines()
        return inst_pckgs
    f_obj.close()


def inst_pckg(name, dest):
    """
    Function that will install packages if its not already present
    """

    src = get_home()+"/.internal.config"
    exsting_pckgs = get_inst_pckg()
    
    if len(exsting_pckgs) < 1:
        with open(src, "w") as f_obj:
            f_obj.writelines(name)
            f_obj.close()
            print("Succesfully installed package: %s to %s."%(name,dest)) 
    else:
        for pckg in exsting_pckgs:
            if name in pckg:
                print("Package: %s is already  installed."%(name)) 
                break


def rmv_pckg(name, dest):
    """
    Function that will remove a package from .internal.config if it exists
    in file.
    """

    src = get_home()+"/.internal.config"
    inst_pckgs = get_inst_pckg()

    if len(inst_pckgs) < 1:
        print("No packages are installed. Nothing to remove.")
        sys.exit(0)        
    else:
        for pckg in inst_pckgs:
            if name in pckg:
                inst_pckgs.remove(pckg)
                with open(src, "w") as f_obj:
                    f_obj.writelines(inst_pckgs)
                    f_obj.close()
                    print("Successfully removed package: %s from %s."%(name,dest)) 


def main():
    """Function to do all main logic.
    This will call in the above sub functions to preform specific tasks
    """

    from sys import argv

    check_files()

    state = argv[1]
    package = argv[2]
    dest = argv[3]
 


    if state == 'present':
        inst_pckg(package, dest)
    if state == 'update':
        inst_pckg(package, dest)
    if state == 'absent':
        rmv_pckg(package, dest)
    

if __name__  == '__main__':
    main()

#remove_pckg("/opt/WebSphere/AppServer", "com.ibm.websphere.ND.v90_9.0.9.20180906_1004")
#install_pckg("/opt/WebSphere/AppServer", "com.ibm.websphere.ND.v90.9.0.10.20181228_1010")
#check_files()
