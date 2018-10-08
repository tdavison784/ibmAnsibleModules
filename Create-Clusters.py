#!/usr/bin/python
import os
import subprocess

class Cluster_Creation():

	Module = None

	def __init__(self):
		"""Function to init all needed arguments"""
		self.module = AnsibleModule(
			argument_spec = dict(
				state = dict(required=True, choices=['present', 'absent']),
				serverName = dict(required=True),
				#clusterName = dict(required=True)
			),
			supports_check_mode = True
		)

		def main(self):
			"""Main function will do all the work"""
			state = self.module.params['state']
			serverName = self.module.params['serverName']
			#clusterName = self.module.parmas['clusterName']

			if state == 'present':
				wsadmin = '/opt/WebSphere/AppServer8.5.5/profiles/Dmgr01/bin/wsadmin.sh -c '
				cell_dir = '/opt/WebSphere/AppServer8.5.5/profiles/Dmgr01/config/cells/'

				cell = os.listdir(cell_dir)[1]

				node_dir = '/opt/WebSphere/AppServer8.5.5/profiles/Dmgr01/config/cells/'+cell+'/nodes/'
				node = os.listdir(node_dir)[1]

				child = subprocess.Popen(
					[wsadmin + "'AdminConfig.create(''Server',"+node+"'[name',"+' '+ serverName+"])"],
					shell=True,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
				stdout_value, stderr_value = child.communicate()

				if child.returncode !=0:
					self.module.fail_json(
						msg="Failed to create Server",
						stderr=stderr_value,
						stdout=stdout_value
					)
				self.module.exit_json(
					msg="Succesfully created servers",
					changed=True,
					stdout=stdout_value,
					stderr=stderr_value
				)

if __name__ == '__main__':
	mkserver = Cluster_Creation()
	mkserver.main()