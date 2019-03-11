#!/usr/bin/python

import os
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ibm_ihs

short_description: Module that controls the state of an IBM Deployment Manager

version_added: "3.0"

description:
    - Module that controls the state of IBM IHS Web Server.
    - Module control start and stop state for both adminctl and apachectl.
    - Support of dry run is provided with this module.

options:
    state:
        description:
            - Describes the state in which to send IBM IHS server.
        required: true
        choices:
          - start
          - stop
    path:
        description:
            - Path of IBM Install root. E.g /opt/IBM/WebSphere/HTTPServer
        required: true
    name:
        description:
            - Name of the IHS service to start, stop, or restart.
        required: true
        choices:
          - adminctl
          - apachectl
author:
    - Tom Davison (@tntdavison784)
'''


EXAMPLES = '''
- name: Stop apachectl service
  ibm_ihs:
    state: stop
    path: /opt/IBM/WebSphere/HTTPServer
    name: apachectl
- name: Stop adminctl service
  ibm_ihs:
    state: stop
    path: /opt/IBM/WebSphere/HTTPServer
    name: adminctl
- name: Restart ihs all services
  ibm_ihs:
    state: restart
    path: /opt/IBM/WebSphere/HTTPServer
    name: "{{ item.service }}"
  loop:
    - { service: adminctl }
    - { service: apachectl }
'''


RETURN = '''
result:
    description: Descibes changed state or failed state
    type: str
message:
    description: Succesfully sent ihs into desired state
'''


def start_service(module):
    """Function that will start either IHS service:
    adminctl or apachectl if it is not already started.
    If its started it will pass the module.exit status."""

    admin_pid = "{0}/logs/admin.pid".format(module.params['path'])
    httpd_pid = "{0}/logs/httpd.pid".format(module.params['path'])

    start_service_cmd = """{0}/bin/{1} {2}""".format(module.params['path'],
                                                     module.params['name'],
                                                     module.params['state'])
    if module.params['name'] == 'adminctl':
        if os.path.exists(admin_pid):
            module.exit_json(
                msg="Service {0} is already running.".format(module.params['name']),
                changed=False
            )
    if module.params['name'] == 'apachectl':
        if os.path.exists(httpd_pid):
            module.exit_json(
                msg="Service {0} is already running.".format(module.params['name']),
                changed=False
            )

    start_ihs_service = module.run_command(start_service_cmd)

    if start_ihs_service[0] != 0:
        module.fail_json(
            msg="Failed to start service {0}. See stdout/stderr for details.".format(module.params['name']),
            changed=False,
            stdout=start_ihs_service[1],
            stderr=start_ihs_service[2]
        )


def stop_service(module):
    """Function that stops given IHS service
    adminctl or apachectl if found not running.
    We are only doing an os.exists check for a .pid file
    association"""

    admin_pid = "{0}/logs/admin.pid".format(module.params['path'])
    httpd_pid = "{0}/logs/httpd.pid".format(module.params['path'])

    if module.params['name'] == 'adminctl':



def stop_apachectl(module, path, name, state):
    """
    Function that will stop ibm ihs apache service
    will only stop if found running
    """
    if not os.path.exists("%s/logs/admin.pid" % (path)):
        module.exit_json(
                msg="httpd service is not running",
                changed=False
        )

    cmd = "%s/bin/%s %s" %(path, name, state)
    stop_httpd = module.run_command(cmd, use_unsafe_shell=True)

    if stop_httpd[0] != 0:
        module.fail_json(
                msg="failed to send  %s service into %s state. see stderr for more details..." % (name, state),
                changed=False,
                stderr=stop_httpd[2]
        )
    module.exit_json(
            msg="Successfully sent  %s service into % state" % (name, state),
            changed=True
    )


def restart_service(module):
    """Function that will restart the given service provided to it."""

    restart_srvc_cmd = """{0}/bin/{1} {2}""".format(module.params['path'],
                                                    module.params['name'],
                                                    module.params['state'])
    restart_service = module.run_command(restart_srvc_cmd)

    if restart_service[0] != 0:
        module.fail_json(
            msg="Failed to restart service {0}. See stderr for details.".format(module.params['name']),
            changed=False
        )
    module.exit_json(
        msg="Sucessfully restarted {0}.".format(module.params['name']),
        changed=True
    )


def main():

    module = AnsibleModule(
            argument_spec=dict(
                state=dict(type='str',required=True, choices=['start','stop','restart']),
                name=dict(type='str',required=True, choices=['adminctl', 'apachectl']),
                path=dict(type='str',required=True, defaults='/opt/IBM/WebSphere/HTTPServer')
            ),
            supports_check_mode = True
    )

    state = module.params['state']
    name = module.params['name']
    path = module.params['path']


    if state == 'start' and not module.check_mode:
        if name == 'apachectl':
            start_apachectl(module, path, name ,state)
        if name == 'adminctl':
            start_adminctl(module, path, name, state)

    if state == 'stop' and not module.check_mode:
        if name == 'apachectl':
            stop_apachectl(module, path, name, state)
        if name == 'adminctl':
            stop_adminctl(module, path, name, state)

    if state == 'restart' and not module.check_mode:
        restart_service(module)

    if module.check_mode:
        if state == 'start':
            if name == 'adminctl':
                if os.path.exists("%s/logs/admin.pid" % (path)):
                    module.exit_json(
                            msg=">>>>>>>> adminctl service is already running <<<<<<<<",
                            changed=False
                    )
                else:
                    module.exit_json(
                            msg=">>>>>>>> adminctl will be sent into start state <<<<<<<<",
                            changed=True
                    )
            if name == 'apachectl':
                if os.path.exits("%s/logs/httpd.pid" % (path)):
                    module.exit_json(
                            msg=">>>>>>>> apachectl service is already running <<<<<<<<",
                            changed=False
                    )
                else:
                    module.exit_json(
                            msg=">>>>>>>> apachectl will be sent into start state",
                            changed=True
                    )

        if state == 'stop': 
            if name == 'adminctl':
                if not os.path.exists("%s/logs/admin.pid" % (path)):
                    module.exit_json(
                            msg=">>>>>>>> adminctl service is already stopped <<<<<<<<",
                            changed=False
                    )
                else:
                    module.exit_json(
                            msg=">>>>>>>> adminctl service will be sent into stop state <<<<<<<<",
                            changed=True
                    )
            if name == 'apachectl':
                if not os.path.exists("%s/logs/httpd.pid" % (path)):
                    module.exit_json(
                            msg=">>>>>>>> apachectl service is already stopped <<<<<<<<",
                            changed=False
                    )
                else:
                    module.exit_json(
                            msg=">>>>>>>> apachectl will be sent into stop state <<<<<<<<",
                            changed=True
                    )
        

if __name__ == '__main__':
    main()
