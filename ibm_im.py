#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule


class IBM_InstallationManager():
    """Class dedicated to installing IBM Installation Manager.
    IBM IM is the first  peice needed to install most IBM Products.
    These products include WebSphere Application Server, Buisnuess Process Manager,
    IBM HTTP Server, etc.."""

    def __init__(self):
        """Init class, and all needded arguments for the module to run."""

        self.module = AnsibleModule(
                argument_spec = dict(
                    admin = dict(type='str', required='True', choices=['yes', 'no']),
                    src = dict(type='str', required='True'),
                    dest = dict(type='str', required='False', default='~/')
                ),
                supports_check_mode = True
        )

    def check_installation(self):
        """Function to check for IBM IM installation precense.
        If Install is present, module will force an exit status
        """

        if os.path.exists(dest):
            self.module.exit_json(
                msg='IBM IM is already installed',
                changed=False
            )

    def install_im(self):
        """Function to install Installation Manager.
        """

        run_install = self.module.run_command()
