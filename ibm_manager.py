#!/usr/bin/python
import subprocess as sp
from ansible.module_utils.basic import *


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ibm_manager

short_description: Module that controls the state of an IBM Deployment Manager

version_added: "2.0"

description:
    - Module that controls the state of IBM Node Deployment Manager.
    - Module is idempotent.
    - Module depends on having the pre-req IBM products installed.
    - Module is aimed at running in a WebSphere ND installation run time.

options:
    state:
        description:
            - Describes the state in which to send IBM Node Agent.
        required: true
        choices:
          - start
          - stop
    path:
        description:
            - Path of IBM Install root. E.g /opt/WebSphere/AppServer.
        required: true
    profile:
        description:
            - Name of IBM Profile that the node agent belongs to.
        required: true


author:
    - Tom Davison (@tntdavison784)
'''

EXAMPLES = '''
- name: Stop Deployment Manager
  ibm_node:
    state: start
    path: /opt/WebSphere/AppServer
    profile: Dmgr01
- name: Stop Node Agent
  ibm_node:
    state: stop
    path: /opt/WebSphere/AppServer
    profile: DmgrProfile
'''

RETURN = '''
result:
    description: Descibes changed state or failed state
    type: str
message:
    description: Succesfully sent Deployment Manager into state

'''


def stop_manager(module, path, profile):
    """Function to send IBM Deployment Manager into a stopped state.
    This function is idempotent, meaning it will only stop the dmgr profile
    if it is up and running. Function will do a filesystem check for a .pid file
    in the WAS_ROOT/profiles/logs/dmgr/ directory. If a .pid file exists, it is assumed
    that the deployment manager is running.
    """

    if  os.path.exists("%s/profiles/%s/logs/dmgr/dmgr.pid"):
        stop_dmgr  = module.run_command(path+'/profiles/'+profile+'/bin/stopManager.sh', use_unsafe_shell=True)
        if stop_dmgr[0] != 0:
            module.fail_json(
                msg='Failed to send Deployment Manager into %s for profile %s' % (state, profile),
                changed=False,
                stderr=start_dmgr[2]
            )
        module.exit_json(
            msg='Succesfully sent Deployment Manager into % state for profile %s' % (state, profile),
            changed=True
        )
    else:
        module.exit_json(
            msg='>>>>>>>> Deployment Manager is not running <<<<<<<<'
        )

def start_manager(moduele, path, profile):
    """Function that will send IBM Deployment Manager into a started state.
    This function is idempotent. Meaning that it will only start the deploymment manager if it is not running.
    Function does a filesystem check to see if a .pid file exists. If file exits, module will return a OK run call.
    """

    if not os.path.exists("%s/profiles/%s/logs/dmgr/dmgr.pid"):
        module.run_command(path+'/profiles/'+profile+'/bin/startManager.sh', use_unsafe_shell=True)
        if start_dmgr[0] != 0:
            module.fail_json(
                msg='Failed to send Deployment Manager %s for profile %s' % (state),
                changed=False,
                stderr=start_dmgr[2]
            )
        module.exit_json(
            msg='Succesfully sent Deployment Manager into % state for profile %s' % (state),
            changed=True
        )
    else:
        module.exit_json(
            msg='>>>>>>>> Deployment Manager is already running <<<<<<<<'
        )



def main():
	"""Main Module logic.
        Imports sub functions to determine state status.
        """

	module_args = dict(
		state = dict(type='str', required=True, choices=['start', 'stop']),
		profile_root = dict(type='str', required=True)
	)

	module = AnsibleModule(
		argument_spec = module_args,
                supports_check_mode = True
	)

	state = module.params['state']
	profile_root = module.params['profile_root']


	if state == 'start' and not module.check_mode:
            start_manager(module, path, profile)

        if state == 'stop' and not module.check_mode:
            stop_manager(module, path, profile)

        elif module.check_module:
            if state == 'stop':
                if  os.path.exists("%s/profile/%s/logs/dmgr/dmgr.pid"):
                    module.exit_json(
                        msg='Sending Deployment Manager into %s' % (state),
                        changed=True
                    )
                else:
                    if not os.path.exists("%s/profiles/%s/logs/dmgr/dmgr.pid"):
                        module.exit_json(
                                msg='Deployment Manager already in a %s state ' %(state),
                                changed=False
                                )
            if state == 'start':
                if  os.path.exists("%s/profiles/%s/logs/dmgr/dmgr.pid"):
                    module.exit_json(
                            msg='Deployment Manager already in a %s state ' %(state),
                            changed=False
                    )
                else:
                    module.exit_json(
                            msg='Sending Deployment Manager into a %s state ' % (state),
                            changed=True
                    )


if __name__ == "__main__":
	main()

