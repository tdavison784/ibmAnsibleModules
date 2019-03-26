Role Name
=========

test_ibm_manager role

Requirements
------------

Requirments are shipped with role. The /library directory contains the needed modules to run ansible unit test on.
Tasks are tagged and its recommended to use. To start run with  --skip-tags "cleanup" then after first run use tag "Dmgr" to
test ibm_manager functionaility.

Role Variables
--------------

The following are the variables that can be set for this role:
was_root
profile_name
state
user
group

These variables are best used at the command line to test various states


Dependencies
------------

Dependencies are included with role.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
