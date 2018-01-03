#!/usr/bin/python
import os
import subprocess
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

author: Tommy Davison (pwtwd35)
'''

EXAMPLES='''

- name: Start Admin Service
  ihs:
    state: started
    service: adminctl

- name: Restart HTTP Service
  ihs:
    state: restarted
    service: apachectl
'''

class IHS():

	Module = None

	def __init__(self):
		"""Function to init all needed arguments"""
		self.module = AnsibleModule(
			argument_spec = dict(
				state = dict(required=True, choices=['started', 'stopped', 'restarted']),
				service = dict(required=True, choices=['adminctl', 'apachectl'])
			)
		)

	def  main(self):
		"""Function that will be preforming all the work."""
		state = self.module.params['state']
		service = self.module.params['service']

		http_root = '/opt/WebSphere/HTTPServer'

		if state == 'started' and service == 'adminctl' and os.path.exists(http_root+"/logs/admin.pid") == False:
			child = subprocess.Popen(
				[http_root + "/bin/" +
				service + " " +
				"start "],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to start adminctl service",
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Started adminctl service",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)

		if state == 'started' and service == 'apachectl'and os.path.exists(http_root+"/logs/httpd.pid") == False:
			child = subprocess.Popen(
				[http_root + "/bin/" +
				service + " " +
				"start "],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to start HTTP service",
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Successfully started HTTP service",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)

		if state == 'restarted':
			child = subprocess.Popen(
				[http_root + "/bin/" +
				service + " " +
				"stop "],
				shell=True,
			),
			child = subprocess.Popen(
				[http_root + "/bin/" +
				service + " " +
				"start "],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode !=0:
				self.module.fail_json(
					msg="Failed to restart " + service,
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Successfully restarted " + service,
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)

		if state == 'stopped':
			child = subprocess.Popen(
				[http_root + "/bin/" +
				service + " " +
				"stop "],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to stop " + service,
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Stopped " + service,
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)
                else:
                        self.module.exit_json(
                                msg=service + " is already started",
                                changed=False
                        )


from ansible.module_utils.basic import *
if __name__ == "__main__":
	run = IHS()
	run.main()
