#!/usr/bin/python
import subprocess as sp
from ansible.module_utils.basic import *

def dmgr():
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


	if state == 'start':
            child = sp.Popen(
                [
                    'find ' + profile_root+'/logs/dmgr/dmgr.pid',
                ],
                shell=True,
                stdout = sp.PIPE,
                stderr = sp.PIPE
            )
            stdout_value, stderr_value = child.communicate()
            if stdout_value:
                module.exit_json(
                    msg='Dmgr is already running',
                    changed=False
                )
            elif stdout_value == '':
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
                [
                    'find ' + profile_root+'/logs/dmgr/dmgr.pid',
                ],
                shell=True,
                stdout = sp.PIPE,
                stderr = sp.PIPE
            )
            stdout_value, stderr_value = child.communicate()
            if stdout_value == '':
                module.exit_json(
                    msg='Dmgr is already stopped',
                    changed=False
                )
            elif stdout_value:
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
	dmgr()

if __name__ == "__main__":
	main()
	
