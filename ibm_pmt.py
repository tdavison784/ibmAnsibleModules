#!/usr/bin/python

import os
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ibm_pmt

short_description: Module that handles profile creation and deletion.

version_added: "3.5"

description:
    - Module that handles IBM WebSphere profile creation.
    - Module is idempotent.
    - Module will create IBM WebSphere ND profiles.
    - Profiles include Deployment manager, and custom profiles.
    - The following parameters are only needed if security is true, admin_user, admin_password

options:
    admin_user:
        description:
            - Name of the admin account that controls the IBM WebSphere cell
        required: false
        required_if: security is true
    admin_password:
        description:
            - Password to be used with admin account
        required: false
        required_if: security is true
    dmgr_host:
        description:
            - HostName or IP Address of server where deployment manager resides
        required: false
    path:
        description:
            - Path of IBM Install root. E.g /opt/IBM/WebSphere/AppServer.
        required: true
    profile:
        description:
            - The name of the profile that will be created
        required: true
    profile_path:
        description:
            - Path of newly created profile. E.g /opt/IBM/WebSphere/AppServer/profiles/Custom01
        required: true
    profile_type:
        description:
            - Type of profile to be created.
        required: true
        choices:
            - managment
            - custom

author:
    - Tom Davison (@tntdavison784)
'''


EXAMPLES = '''
- name: create dmgr profile with security enabled
  ibm_pmt:
    state: present
    admin_user: MyAdmin
    admin_password: MyPassword
    path: /opt/IBM/WebSphere/AppServer
    profile: DeploymenManager
    profile_path: /opt/IBM/WebSphere/AppServer/profiles/DeploymentManager
    security: True
    profile_type: management
- name: create custom profile
  ibm_pmt:
    state: present
    admin_user: MyAdmin
    admin_password: MyPassword
    path: /opt/IBM/WebSphere/AppServer
    profile_path: /opt/IBM/WebSphere/AppServer/profiles/Custom01
    profile: Custom01
    profile_type: custom
'''
    

def make_managerProfile(module, admin_user, admin_password, cell_name, 
        path, profile_path, security):
    """
    Function that creates an Deployment manager profile
    for IBM WebSphere ND installations.
    """

    if cell_name is not None:
        create_dmgr_account = "%s/bin/manageprofiles.sh -create -templatePath \
            %s/profileTemplates/management/ -adminUserName %s -adminPassword %s\
             - cellName %s -enableAdminSecurity %s -profileRoot %s \
              -personalCertValidityPeriod 15 \
              -serverType DEPLOYMENT_MANAGER -signingCertValidityPeriod 20 \
               -profileName %" % (path, path, admin_user, admin_password,
                       cell_name, security, profile_path, profile)


    if cell_name is None:
        create_dmgr_account = "%s/bin/manageprofiles.sh -create -templatePath \
            %s/profileTemplates/management/ -adminUserName %s -adminPassword %s\
             -enableAdminSecurity %s -profileRoot %s -personalCertValidityPeriod 15 \
              -serverType DEPLOYMENT_MANAGER -signingCertValidityPeriod 20 \
               -profileName %" % (path, path, admin_user, admin_password,
                       security, profile_path, profile)

        mngr_acct_create = module.run_command(create_dmgr_account, use_unsafe_shell=True)

        if mngr_acct_create[0] != 0:
            module.fail_json(
                    msg=">>>>>>>> Failed to create account: %s \
                            . Review errors and try again <<<<<<<<" % (profile),
                    changed=False,
                    stderr=mngr_acct_create[2]
            )
        module.exit_json(
            msg=">>>>>>>> Succesfully created account %s <<<<<<<<" % (profile),
            changed=True
        )


def make_customProfile(module, admin_user, admin_password, dmgr_host,
        profile, profile_path):
    """
    Function that creates a custom profile for a IBM Websphere ND Cell
    """

    create_custom_profile = "%s/bin/manaeprofiles.sh - create \
             -templatePath %s/profileTemplates/managed/ \
              -dmgrAdminUserName %s -dmgrAdminPassword %s \
               -profileRoot %s -profileName %s -dmgrHost %s"
               % (path, path, admin_user, admin_password,
                       profile_root, profile, dmgr_host)

    cstm_account_create = module.run_command(create_custom_profile, use_unsafe_shell=True)
    if cstm_account_create[0] != 0:
        module.fail_json(
                msg=">>>>>>>> Failed to create account %s <<<<<<<<" %(profile),
                changed=False,
                stderr=cstm_account_create[2]
        )
    module.exit_json(
            msg=">>>>>>>> Successfully created account %s <<<<<<<<" %(profile),
            changed=True
    )


def check_accountExistance(module, path, profile):
    """
    Function that checks to see if specified profile
    exists in current IBM WebSphere cell.
    """

    check_profile_cmd = "%s/bin/manageprofiles.sh -listProfiles" % (path)
    profile_check = module.run_command(check_profile_cmd, use_unsafe_shell=True)

    if profile in profile_check[1]:
        module.exit_json(">>>>>>>> Profile %s already exists in cell <<<<<<<<" 
                %(profile),
        changed=False)


def main():

    module = AnsibleModule(
            argument_spec=dict(
                admin_user=dict(type='str', required=False),
                admin_password=dict(type='str', required=False),
                cell_name=dict(type='str', required=False, defaults=None),
                dmgr_host=dict(type='str', required=False),
                profile=dict(type='str', required=True),
                profile_path=dict(type='str', required=True),
                profile_type=dict(type='str', required=True, choices=['management', 'custom']),
                security=dict(type='bol', required=True),
                state=dict(type='str', required=True choices=['absent', 'augment', '
                    backup', 'present' 'restore'])
            ),
            support_check_mode = True,
            required_if=[
                ["security",True, ["admin_user", "admin_password"],
                ["security",True, ["profile_type", "management"]]]
    )

    admin_user = module.params['admin_user']
    admin_password = module.params['admin_password']
    cell_name = module.params['cell_name']
    dmgr_host = module.params['dmgr_host']
    profile = module.params['profile']
    profile_path = module.params['profile_path']
    profile_type = module.params['profile_type']
    security = module.params['security']
    state = module.params['state']


    if profile_type == 'management' and state == 'present':
        check_accountExistance(module, path, profile)
        make_managerProfile(module, admin_user, admin_password, cell_name, path, profile_path, security)
    if profile_type == 'custom' and state == 'present':
        check_accountExistance(module, path, profile)
        make_customProfile(module, admin_user, admin_password, dmgr_host, profile, profile_path)

    if module.check_mode:
        if profile_type == 'management' or 'custom':
            check_accountExistance(module, path, profile)
            module.exit_json(
                msg=">>>>>>>> Account %s will be created on run <<<<<<<<" %(profile),
                changed=True
            )


if __name__ == '__main__':
    main()
