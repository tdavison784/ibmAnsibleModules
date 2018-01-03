#!/usr/bin/python
import os
import datetime
import subprocess

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION='''
---
module: was.py

short_description: Module to install IBM WAS ND and other WAS products

version_added: 1.0

description:
	- Module to install IBM WAS ND and byproducts for DHS
	- Incorporates standart dir of '/opt/WebSphere/AppServer' if not specified otheriwse
	- Installs via response_file or specific IBM package name

options:
	src:
		description:
			- Location of IBM Product Binaries. Specifically repository.config

	dest:
		description:
			- Installation Directory of IBM Product. Ie. '/opt/WebSphere/AppServer/'

	state:
		description:
			- Determins whether or not to install or uninstall IBM Products

	package:
		description:
			- Name of IBM package to install

	response_file:
		description:
			- Boolean for whether or not to use a response file

	reponse_loc:
		description:
			- Location of response file to use for install

author: Tommy Davison (pwtwd35)
'''

EXAMPLES='''
---
-
  hosts: TEST
  become: true
  become_method: sudo
  become_user: wsadmin
  tasks:
    -
      name: Install WAS ND package only
      was:
        src: "/was855/WAS_855_BASE/"
        dest: "/opt/WebSphere/AppServer/"
        package: com.ibm.websphere.ND.v85_8.5.5000.20130514_1044
-------------------------
---
-
  hosts: TEST
  become: true
  become_method: sudo
  become_user: wsadmin
  tasks:
    -
      name: Install WAS ND using Response File
      was:
        state: present
        response_file: True
        response_loc: '/was855/InstallResponse.xml'
-------------------------
'''


class IBM_MW_Installer():

	Module = None

	def __init__(self):
		"""Function to init all needed args"""
		self.module = AnsibleModule(
			argument_spec = dict(
				state = dict(required=True, choices=['present', 'absent']),
				src = dict(required=False),
				dest = dict(required=False, default="/opt/WebSphere/AppServer/"),
				response_file = dict(type='bool', required=False),
				response_loc = dict(requried=False),
				package = dict(required=False),
				logdir= dict(required=False, default='/tmp/')
			),
			supports_check_mode = True
		)

	def check_existence(self, dest):
		"""Function to see if IBM MW product exists"""
		if os.path.exists(dest):
			self.module.exit_json(
				msg="IBM WAS ND Is Installed",
				changed=False
			)

	def main(self):
		"""Function that will be doing all the work for the new module"""
		state = self.module.params['state']
		src = self.module.params['src']
		dest = self.module.params['dest']
		response_file = self.module.params['response_file']
		response_loc = self.module.params['response_loc']
		package = self.module.params['package']
		logdir = self.module.params['logdir']


		if state == 'present' and response_file == True and os.path.exists(dest+"bin/versionInfo.sh") == False:
			imcl = '/opt/WebSphere/InstallationManager/eclipse/tools/imcl'
			child = subprocess.Popen(
				[imcl +
				" -acceptLicense "
				"-log /tmp/IBM_WASND_Install.log "
				"-input " + response_loc],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="WAS ND Failed to install",
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="WAS ND Installed Succesfully",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)


		if state == 'present' and os.path.exists(dest+"bin/versionInfo.sh") == False:
			imcl = '/opt/WebSphere/InstallationManager/eclipse/tools/imcl'
			child = subprocess.Popen(
				[imcl +
				" -acceptLicense "
				"-log /tmp/IBM_WASND_Install.log "
				"install " + package + " " +
				"-repositories " + src + " " +
				"-installationDirectory " + dest + " " +
				"-sharedResourcesDirectory /opt/WebSphere/IMShared"],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Installation has failed for " + package + ".",
					stderr=stderr_value,
					stdout=stdout_value
				)

			self.module.exit_json(
				msg=package + " Has installed successfully.",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)
		else:
			self.module.exit_json(
                                msg="WAS is already installed",
                                changed=False
                        )


		if state == 'absent':
			imcl = '/opt/WebSphere/InstallationManager/eclipse/tools/imcl'
			child = subprocess.Popen(
				[imcl + " " +
				"uninstallAll"],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to uninstall IBM Products",
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
					msg="Successfully uninstalled IBM Products",
					changed=True,
					stdout=stdout_value,
					stderr=stderr_value
			)
					

from ansible.module_utils.basic import *
if __name__ == "__main__":
	run_tool = IBM_MW_Installer()
	run_tool.main()	
