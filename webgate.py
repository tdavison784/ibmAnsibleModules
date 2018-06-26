#!/usr/bin/python
import os
import subprocess

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

class webgate():
	Module = None

	def __init__(self):
		"""Function to init all needed args"""
		self.module = AnsibleModule(
			argument_spec = dict(
				response_file = dict(required=True),
				oraInst = dict(required=True),
			)
		)

	def main(self):
		"""Function that does all the work"""
		response_file = self.module.params['response_file']
		oraInst = self.module.params['oraInst']
		if os.path.exists('/opt/OAM/oracle/') == False:
			child = subprocess.Popen(
				["/was855/OAM-11g/Disk1/runInstaller -silent -response " +
				response_file + " -jreLoc /usr/ -invPtrLoc " + oraInst +
				" -ignoreSysPrereqs"],
				shell=True,
				stdout = subprocess.PIPE,
				stderr = subprocess.PIPE
			)
			stdout_value, stderr_value = child.communicate()

			if child.returncode != 0:
				self.module.fail_json(
					msg="Failed to install webgate",
					changed=False,
					stderr = stderr_value,
					stdout = stdout_value
				)
			self.module.exit_json(
				msg="Succefully installed webgate",
				changed = True,
				stdout = stdout_value,
				stderr = stderr_value
			)
		else:
			self.module.exit_json(
				msg="webgate already exists",
				changed=False
			)

from ansible.module_utils.basic import *
if __name__ == "__main__":
	wg_inst = webgate()
	wg_inst.main()
