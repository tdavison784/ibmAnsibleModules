#!/usr/bin/python
import subprocess as sp
from ansible.module_utils.basic import *

def start_manager():
	""" Starts Dmgr WAS profile """

	module_args = dict(
		state = dict(type='str', required=True, choices=['start', 'stop']),
		profile_root = dict(type='str', required=True)
	)

	module = AnsibleModule(
		argument_spec = module_args
	)

	state = module.params['state']
	profile_root = module.params['profile_root']

	child = sp.Popen(
		["find /opt/WebSphere/ -name dmgr.pid"],
		shell = True,
		stdout = sp.PIPE,
		stderr = sp.PIPE
	)
	stdout_value, stderr_value = child.communicate()

	if stdout_value:
		module.exit_json(
			msg = "Dmgr is already running",
			changed = False,
			stdout = stdout_value,
			stderr = stderr_value
		)

	elif state == 'start':
		child = sp.Popen(
			[profile_root+"/bin/startManager.sh"],
			shell = True,
			stdout = sp.PIPE,
			stderr = sp.PIPE
		)
		stdout_value, stderr_value = child.communicate()
		if child.returncode != 0:
			module.fail_json(
				msg = "Failed to start Dmgr profile",
				changed = False,
				stderr = stderr_value,
				stdout = stdout_value
			)
		module.exit_json(
			msg = "Started Dmgr profile",
			changed = True
		)

	elif state == 'stop':
		child = sp.Popen(
			[profile_root+"/bin/stopManager.sh"],
			shell = True,
			stdout = sp.PIPE,
			stderr = sp.PIPE
		)
		stdout_value, stderr_value = child.communicate()

		if child.returncode != 0:
			module.fail_json(
				msg = "Failed to stop Dmgr profile",
				changed = False,
				stdout = stdout_value,
				stderr = stderr_value
			)
		module.exit_json(
			msg = "Stopped Dmgr",
			changed = True,
			stdout = stdout_value,
			stderr = stderr_value
		)


def main():
	start_manager()

if __name__ == "__main__":
	main()
	
