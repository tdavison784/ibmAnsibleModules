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
module: pmt.py

short_description: Module to create WAS profiles. Primarilly Dmgr and AppSrv

version_added: 1.0

description:
	- Module to create WAS profiles (Dmgr & AppSrv)
	- AppSrv profile will federate to Dmgr Cell
	- Dmgr Cell needs to be started first
	- If profile_root exists, script will skip

options:
	state:

		description:
			- Determines if profile will be created or deleted
			- present will create
			- absent will delete
			- state is required for playbook to run

	profileName:

		description:
			- Name of profile to be created

	adminUser:

		description:
			- Name of admin user for when cell security is enabled

	adminPasswd:

		description:
			- Password that is associated with adminUser for cell security

	templatePath:

		description:
			- Path to available profile templates for WAS profile creation

	profilePath:

		description:
			- Path needed for AppSrv profile creation

	dmgrHost:

		description:
			- Hostname of server that Dmgr is running on
			- Required when wanting to federate additonal profile into Dmgr cell

	startManager:

		description:
			- Starts IBM Dmgr Process. 
			- Boolean option:
			- Specify True to start
			- False to skip

author: Tommy Davison (pwtwd35)
'''

EXAMPLES='''
---
-
  hosts: dev
  become: true
  become_method: sudo
  become_user: wsadmin
  tasks:
    -
      name: Create Dmgr Profile
      pmt:
        profileName: Dmgr01
        templatePath: /opt/WebSphere/AppServer/profileTemplates/management/
        profilePath: /opt/WebSphere/AppServer/profiles/Dmgr01
        adminUser: wsadmin
        adminPasswd: examplepassword123

-------------------------
---
-
  hosts: dev
  become: true
  become_method: sudo
  become_user: wsadmin
  tasks:
    -
      name: Create Dmgr and Start Dmgr process after profile creation
      pmt:
        profileName: Dmgr01
        templatePath: /opt/WebSphere/AppServer/profileTemplates/management/
        profilePath: /opt/WebSphere/AppServer/profiles/Dmgr01
        adminUser: wsadmin
        adminPasswd: examplepassword123
        startManager: True

-------------------------
---
-
  hosts: dev
  become: true
  become_method: sudo
  become_user: wsadmin
  tasks:
    -
      name: Create AppSrv01 Profile
      pmt:
        profileName: AppSrv01
        templatePath: /opt/WebSphere/AppServer/profileTemplates/managed/
        profilePath: /opt/WebSphere/AppServer/profiles/AppSrv01
        dmgrHost: some_server_hostname
        adminUser: wsadmin
        adminPasswd: examplepassword123	

-------------------------
'''

class PMT_Tool():

	Module = None

	def __init__(self):
		"""Function to init all needed args"""
		self.module = AnsibleModule(
			argument_spec = dict(
				state = dict(required=True, choices=['present', 'absent']),
				profileName = dict(required=True),
				adminUser = dict(required=False),
				adminPasswd = dict(required=False),
				templatePath = dict(required=False),
				profilePath = dict(required=False),
				dmgrHost = dict(required=False),
				was_root = dict(required=False),
				startManager = dict(type='bool', required=False)
			),
			supports_check_mode = True
		)

	def main(self):
		"""Function that will be doing all the work."""
		state = self.module.params['state']
		profileName = self.module.params['profileName']
		adminUser = self.module.params['adminUser']
		adminPasswd = self.module.params['adminPasswd']
		templatePath = self.module.params['templatePath']
		profilePath = self.module.params['profilePath']
		dmgrHost = self.module.params['dmgrHost']
		was_root = self.module.params['was_root']
		startManager = self.module.params['startManager']

		if state == 'present' and profileName == 'Dmgr01' and os.path.exists(profilePath+"/properties/version/profile.version") == False and startManager:
			child = subprocess.Popen(
				[was_root + "/bin/manageprofiles.sh "+
				"-create "
				"-templatePath " + templatePath + " " +
				"-adminUserName " + adminUser + " " +
				"-adminPassword " + adminPasswd + " "+
				"-enableAdminSecurity true "
				"-profilePath " + profilePath + " " +
				"-personalCertValidityPeriod 15 "
				"-serverType DEPLOYMENT_MANAGER "
				"-signingCertValidityPeriod 20 "
				"-profileName " + profileName],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to install " + profileName + " profile.",
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Succesfully installed " + profileName + " profile.",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)
			dmgr_start = profilePath + "/bin/startManager.sh"
			child = subprocess.Popen(
				[dmgr_start],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to start Dmgr Process.",
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Started Dmgr Process.",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)

		if profileName == 'Dmgr01' and startManager and os.path.exists(profilePath+"/logs/dmgr/dmgr.pid") == False:
			dmgr_start = profilePath + "/bin/startManager.sh"
			child = subprocess.Popen(
				[dmgr_start],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to start DMGR Process",
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Dmgr is open for e-buisnuess",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)
		else:
			self.module.exit_json(
				msg="DMGR is already running",
				changed=False,
			)

		if state == 'present' and profileName == 'AppSrv01' and os.path.exists(profilePath+"/properties/version/profile.version") == False:
			child = subprocess.Popen(
				[was_root + "/bin/manageprofiles.sh " +
				"-create "
				"-templatePath " + templatePath + " " +
				"-profilePath " + profilePath + " " +
				"-federateLater false "
				"-dmgrHost " + dmgrHost + " " +
				"-dmgrPort 8879 "
				"-dmgrAdminUserName " + adminUser + " " +
				"-dmgrAdminPassword " + adminPasswd + " " +
				"-profileName " + profileName],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg='Failed to create ' + profileName + " profile.",
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Succesfully installed " + profileName + " profile.",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)
		else:
			self.module.exit_json(
				msg=profileName + " already exists",
				changed=False,
			)


		if state == 'absent':
			child = subprocess.Popen(
				[was_root + "/bin/manageprofiles.sh " +
				"-delete "
				"-profileName " + profileName],
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to uninstall " + profileName + " profile.",
					changed=False,
					stderr=stderr_value,
					stdout=stdout_value
				)
			self.module.exit_json(
				msg="Succesfully installed " + profileName + " profile.",
				changed=True,
				stdout=stdout_value,
				stderr=stderr_value
			)

from ansible.module_utils.basic import *
if __name__ == "__main__":
	mkprofile = PMT_Tool()
	mkprofile.main()
