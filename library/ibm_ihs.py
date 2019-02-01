#!/usr/bin/python

import os
import subprocess as sp
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION='''
---
module: ihs.py

short_description: Module to control IHS service state.

version_added: 1.0

description:
	- Control IHS service state

options:
  state:
    description:
      - started, stopped, restarted
      - will start, stop, or restart adminctl, or apachetcl service

  service:
    description:
      - adminctl, apachectl
      - adminctl is needed to communicate with WAS Dmgr cell
      - apachectl controls httpd process

author: Tommy Davison <tommy.davison@state.mn.us>
'''

EXAMPLES='''

- name: Start Admin Service
  ibm_ihs:
    state: start
    name: adminctl
    path: /opt/IBM/WebSphere/HTTPServer

- name: STOP ADMIN SERVICE
  ibm_ihs:
    state: stop
    name: adminctl
    path: /opt/IBM/WebSphere/HTTPServer  

- name: START APACHE SERVICE
  ibm_ihs:
    state: start
    name: apachectl
    path: /opt/IBM/WebSphere/HTTPServer

- name: STOP APACHE SERVICE
  ibm_ihs:
    state: stop
    name: apachectl
    path: /opt/IBM/WebSphere/HTTPServer


- name: Restart HTTP Service
  ibm_ihs:
    state: restarted
    service: apachectl
'''


def start_apachectl(module, path, name, state):
    """
    Function that will start ibm ihs apachectl service
    """
    if os.path.exists("%s/logs/httpd.pid" % (path)):
        module.exit_json(
                msg=">>>>>>>> httpd service is already running",
                changed=False
        )
    cmd = "%s/bin/%s %s" %(path, name, state)
    start_httpd = module.run_command(cmd, use_unsafe_shell=True)

    if start_httpd[0] != 0:
        module.fail_json(
                msg="failed to send  %s service into %s state. see stderr for more details..." % (name, state),
                changed=false
                stderr=start_httpd[2]
        )
    module.exit_json(
            msg=">>>>>>>> successfully sent  %s service into % state<<<<<<<<" % (name, state),
            changed=true
    )


def stop_apachectl(module, path, name, state):
    """
    Function that will stop ibm ihs apache service
    will only stop if found running
    """
    if not os.path.exists("%s/logs/admin.pid" % (path)):
        module.exit_json(
                msg=">>>>>>>> httpd service is not running <<<<<<<<",
                changed=False
        )

    cmd = "%s/bin/%s %s" %(path, name, state)
    stop_httpd = module.run_command(cmd, use_unsafe_shell=True)

    if stop_httpd[0] != 0:
        module.fail_json(
                msg="failed to send  %s service into %s state. see stderr for more details..." % (name, state),
                changed=false
                stderr=stop_httpd[2]
        )
    module.exit_json(
            msg=">>>>>>>> successfully sent  %s service into % state<<<<<<<<" % (name, state),
            changed=true
    )


def restart_apachectl(module, path, name, state):

    """
    Function that will restart ibm ihs apachectl service
    """

    cmd = "%s/bin/%s %s" % (path, name, state)
    restart_httpd = module.run_command(cmd, use_unsafe_shell=True)

    if restart_httpd[0] != 0:
        module.fail_json(
                msg=">>>>>>>> Failed to restart %s service <<<<<<<<" % (name),
                changed=False,
                stderr=restart_httpd[2]
        )
    module.exit_json(
            msg=">>>>>>>> Successfully restarted %s service <<<<<<<<" % (name),
            changed=True
    )


def start_adminctl(module, path, name, state):
    """
    Function that will start ibm ihs adminctl service.
    Will only start if found not running
    """

    if os.path.exists("%s/logs/admin.pid" % (path)):
        module.exit_json(
                msg=">>>>>>>> adminctl service is already running <<<<<<<<",
                changed=False
        )
    
    cmd = "%s/bin/%s %s" %(path, name, state)
    start_admin = module.run_command(cmd, use_unsafe_shell=True)

    if start_admin[0] != 0:
        module.fail_json(
                msg="failed to send  %s service into %s state. see stderr for more details..." % (name, state),
                changed=false
                stderr=start_admin[2]
        )
    module.exit_json(
            msg=">>>>>>>> successfully sent  %s service into % state<<<<<<<<" % (name, state),
            changed=true
    )


def stop_adminctl(module, path, name, state):
    """
    Function that will stop ibm ihs adminctl service.
    Will only stop if found not running.
    """

    if not os.path.exists("%s/logs/admin.pid" % (path)):
        module.exit_json(
                msg=">>>>>>>> adminctl service is already stopped <<<<<<<<",
                changed=False
        )
    
    cmd = "%s/bin/%s %s" %(path, name, state)
    stop_admin = module.run_command(cmd, use_unsafe_shell=True)

    if stop_admin[0] != 0:
        module.fail_json(
                msg="failed to send  %s service into %s state. see stderr for more details..." % (name, state),
                changed=false
                stderr=stop_admin[2]
        )
    module.exit_json(
            msg=">>>>>>>> successfully sent  %s service into % state<<<<<<<<" % (name, state),
            changed=true
    )


def restart_adminctl(module, path, name, state):
    """
    Function that will restart ibm ihs adminctl service
    """

    cmd = "%s/bin/%s %s" % (path, name, state)
    restart_adminctl = module.run_command(cmd, use_unsafe_shell=True)

    if restart_adminctl[0] != 0:
        module.fail_json(
                msg=">>>>>>>> Failed to restart %s service <<<<<<<<",
                changed=False,
                stderr=restart_adminctl[2]
        )
    module.exit_json(
            msg=">>>>>>>> Successfully restarted %s service <<<<<<<<",
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
        if name == 'adminctl':
            restart_adminctl(module, path, name, state)
        if name == 'apachectl':
            restart_apachectl(module, path, name, state)

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
