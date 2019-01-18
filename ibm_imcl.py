#!/usr/bin/python

import os
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_imcl

short_description: Module that takes care of installing packages via imcl cli.

version_added: "2.1"

description:
    - Module that takes care of installing IBM products via imcl cli.
    - Module does a package lookup within the target cell to check for package existance.
    - Depending on the specified module state, the package check will determine the outcome of the run.
    - Module supports dry runs.

options:
    state:
        description:
            - Specified state of package.
        required: true
        choices:
          - present
          - absent
          - update
    src:
        description:
            - Path to IBM IM installation binaries. E.g /tmp/WASND8.5.5/
        required: false
    dest:
        description:
            - Installation Path where package will be installed. E.g /opt/IBM/WebSphere/AppServer
        required_if: state == 'present'
    path:
        description:
            - Path that leads to imcl tool for installing packages.
        required: true
    name:
        description:
            - Name of package to be installed, updated, or removed from any given cell.
        required: true
    shared_resource:
        description:
            - Path to sharedResources directory for Product install. E.g /opt/IBM/IMShared
        required_if: state == 'present' or 'update'


author:
    - Tom Davison (@tntdavison784)
'''

EXAMPLES = '''
- name: Install IBM ND version 8.5.5
  ibm_imcl:
    state: present
    src: /tmp/WASND8.5/
    dest: /opt/IBM/WebSphere/AppServer
    path: /opt/IBM/InstallationManager/eclipse/tools/imcl
    name: com.ibm.websphere.ND.v85_8.5.5012.20170627_1018
    shared_resource: /opt/IBM/IMShared
- name: Uninstall IBM ND version 8.5.5
  ibm_imcl:
    state: absent
    path: /opt/IBM/InstallationManager/eclipse/tools/imcl
    name: com.ibm.websphere.ND.v85_8.5.5012.20170627_1018
    shared_resource: /opt/IBM/IMShared
- name: Update WAS ND to FixPack 8.5.5.13
  ibm_imcl:
    state: update
    path: /opt/IBM/InstallationManager/eclipse/tools/imcl
    name: com.ibm.websphere.ND.v85_8.5.5013.20180112_1418
'''

RETURN = '''
update:
    description: Describes state of updating a package
    type: str
message:
    description: Successfully updated package: <package_name> into cell.
install:
    description: Describes state after installing a package
    type: str
message:
    description: Successfully installed package: <package_name> into cell.
absent:
    description: Describes state after uninstalling a package.
    type: str
message:
    description: Successfully removed package: <package_name> from cell.
'''


def install_package(module,path,src,shared_resource,dest,name,properties):
    """Function that takes care of installing new packages into the target environment."""

    if properties is None:
        package_install =  module.run_command(path + " -acceptLicense -repositories " + src +
                                          " -installationDirectory " + dest + " -log /tmp/IBM-Install.log " +
                                          "-sharedResourcesDirectory " + shared_resource + " install " + name,
                                          use_unsafe_shell=True)
    if properties is not None:
        package_install =  module.run_command(path + " -acceptLicense -repositories " + src +
                                          " -installationDirectory " + dest + " -log /tmp/IBM-Install.log " +
                                          "-sharedResourcesDirectory " + shared_resource + " install " + name +
                                          " -properties " + properties,
                                          use_unsafe_shell=True)
    if package_install[0] != 0:
        module.fail_json(
            msg="Failed to install package: %s. Please see log in /tmp for more details." % (name),
            changed=False,
            stderr=package_install[2]
        )

    module.exit_json(
        msg="Succesfully installed package: %s to location: %s. For installation details please see log in /tmp/. "
            % (name, dest),
        changed=True
    )


def update_package(module,path,src,shared_resource,name):
    """Function that updates packages for target environment."""

    package_update = module.run_command(path + " -acceptLicense -sharedResourcesDirectory " + shared_resource
                                        + " install " + name + " -repositories " + src +
                                        " -log /tmp/IBM-Install.log", use_unsafe_shell=True)
    if package_update[0] != 0:
        module.fail_json(
            msg="Failed to update package: %s. Please see log in /tmp/ for more details." % (name),
            changed=False,
            stderr=package_update[2]
        )
    module.exit_json(
        msg="Succesfully updated package: %s" % (name),
        changed=True
    )


def rollback_package(module,path,name):
    """Function to rollback to a previous package version."""

    rllbck_pckg = module.run_command(path+" rollback "+name,use_unsafe_shell=True)

    if rllbck_pckg[0] != 0:
        module.fail_json(
            msg="Failed to rollback package: %s because the package was not previously installed" %(name),
            changed=False,
            stderr=rllbck_pckg[2]
        )
    module.exit_json(
        msg="Successfully rolled back package: %s" %(name),
        changed=True
    )


def uninstall_package(module,path,name):
    """Functiont that will remove any given package from target environment."""

    remove_package = module.run_command(path + " uninstall " + name
                                        + "-log /tmp/IBM-Install.log", use_unsafe_shell=True)

    if remove_package[0] != 0:
        module.fail_json(
            msg="Failed to remove package: %s from cell. See log in /tmp/ for more details." % (name),
            changed=False,
            stderr=remove_package[2]
        )
    module.exit_json(
        msg="Succesfully removed package: %s from cell." % (name),
        changed=True
    )


def package_check(module,path,name):
    """Function that will be checking target cell for package existance.
    This portion will be doing package lookups to ensure that the package being installed
    either exists in the cell, or doesn't for all module.params['state']
    """

    check_package = module.run_command(path + " listInstalledPackages", use_unsafe_shell=True)

    if name in check_package[1]:
        return 1
    else:
        return 0


def main():
    """Function that does all the main logic for the module.
    This portion will be doing package lookups to ensure that the package being installed
    either exists in the cell, or doesn't for all module.params['state']
    """

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True, choices=['present', 'absent', 'update', 'rollback']),
            src=dict(type='str', required=True),
            dest=dict(type='str', required=False),
            path=dict(type='str', required=True),
            name=dict(type='str', required=False),
            shared_resource=dict(type='str', required=False),
            properties=dict(type='str', required=False, default=None)
        ),
        supports_check_mode = True,
        required_if=[
            ["state","present", ["dest", "shared_resource"],
             ["state","update", ["dest", "shared_resource"]]]]
    )

    state = module.params['state']
    src = module.params['src']
    dest = module.params['dest']
    path = module.params['path']
    name = module.params['name']
    shared_resource = module.params['shared_resource']
    properties = module.params['properties']
    pckg_check = package_check(module,path,name)


    if pckg_check != 1:
        if state == 'present' and not module.check_mode:
            install_package(module,path,src,shared_resource,dest,name,properties)
        if state == 'update' and not module.check_mode:
            update_package(module,path,src,shared_resource,name)
        if state == 'rollback':
            rollback_package(module,path,name)
        if module.check_mode:
            if state == 'present':
                module.exit_json(msg="Package: %s will be installed to location %s" % (name,dest),change=True)
            if state == 'update':
                module.exit_json(msg="Package: %s will be updated" % (name),changed=True)
            if state == 'absent':
                module.exit_json(msg="Package: %s is not present in cell. Nothing to remove." % (name),changed=False)
            if state == 'rollback':
                module.exit_json(msg="Package %s is not present in cell. Nothing to remove" % (name),changed=False)
    elif pckg_check != 0:
        if state == 'present':
            module.exit_json(msg="Package %s is already present." % (name),changed=False)
        if state == 'absent' and not module.check_mode:
            uninstall_package(module,path,name)
        if state == 'rollback' and not module.check_mode:
            rollback_package(module,path,name)
        if module.check_mode:
            if state == 'absent':
                module.exit_json(msg="Package %s will be removed." % (name),changed=True)
            if state == 'rollback':
                module.exit_json(msg="Package %s will be rolled back" %(name),changed=True)

if __name__ == '__main__':
    main()
