#!/usr/bin/python

import os
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_node

short_description: Module that controls the state of IBM Node Agent.

version_added: "2.1"

description:
    - Module that controls the state of IBM Node Agent.
    - Module is idempotent.
    - Module depends on having the pre-req IBM products installed.

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
- name: Start Node Agent
  ibm_node:
    state: start
    path: /opt/WebSphere/AppServer
    profile: AppSrv01
- name: Stop Node Agent
  ibm_node:
    state: stop
    path: /opt/WebSphere/AppServer
    profile: AppSrv01
'''

RETURN = '''
result:
    description: Descibes changed state or failed state
    type: str
message:
    description: Succesfully put node agent into a state for profile

'''

def stop_node(module):
    """Function that will stop IBM Node agent.
    Function is idempotent and will only stop if running.
    To determine running state, we will check for the default .pid
    location to determine state. Below are the return results:
    """
    try:
        if module.params['state'] == 'stop':
            stop_node_cmd = "{0}/profiles/{1}/bin/stopNode.sh".format(module.params['path'],module.params['profile'])
            stop_node = module.run_commmand(stop_node_cmd)

            if stop_node[0] != 0:
                module.fail_json(
                    msg="Failed to stop node agent. See stderr for details",
                    changed=False,
                    stderr=stop_node[2]
                )
            module.exit_json(
                msg="Successfully stopped node agent",
                changed=True
            )

    except OSError:
            module.exit_json(
                msg="Path does not exist.",
                changed=False
                params=module.params['path']
            )

def start_node(module):
    """Function that will start Node Agent if stopped.
    Function is idempotent and will only start if stopped.
    To determine running state we will check for the default .pid
    location to determine state.
    """

    try:
        if module.params['state'] == 'start':
            start_node_cmd = "{0}/profiles/{1}/bin/startNode.sh".format(module.params['path'],module.params['profile'])
            start_node = module.run_command(start_node_cmd)

            if start_node[0] != 0:
                module.fail_json(
                    msg="Failed to start node agent. See stderr for details",
                    changed=False,
                    stderr=start_node[2]
                )
            module.exit_json(
                msg="Sucesffuly started node agent."
                changed=True
            )
    except OSError:
        module.exit_json(
            msg="Path does not exist",
            changed=False,
            params=module.params['path']
        )

def main():
    """Main Function of the module.
    Function will import other modules into main body to run the main logic"""

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True),
            path=dict(type='str', required=True),
            profile=dict(type='str', required=True)
        ),
        supports_check_mode = True
    )

    state = module.params['state']
    path = module.params['path']
    profile = module.params['profile']

    if state == 'stop' and not module.check_mode:
        stop_node(module)

    if state == 'start' and not module.check_mode:
        start_node(module)

    if module.check_mode:
        if state == 'stop':
            if os.path.exists("%s/profiles/%s/logs/nodeagent/nodeagent.pid"):
                module.exit_json(
                    msg="Sending Nodeagent into {0} state".format(state),
                    changed=True
                )
            else:
                module.exit_json(
                    msg="NodeAgent is already in {0} state".format(state),
                    changed=False
                )

        if state == 'start':
            if not os.path.exists("%s/profiles/%s/logs/nodeagent/nodeagent.pid"):
                module.exit_json(
                    msg="Sending node agent into {0} state.".format(state),
                    changed=True
                )
            else:
                module.exit_json(
                    msg="NodeAgent is already in %s state.".format(state),
                    changed=False
                )

if __name__ == '__main__':
    main()
