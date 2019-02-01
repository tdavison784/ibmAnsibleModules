# IBM WebSphere Application Server Modules

IBM WebSphere Application Server modules. Modules that assist with simplifing and scaling IBM WAS Middleware build outs. All latest modules following a standard naming convention of ibm_command_name. This is to help isolate commands for end users and modules for ibm software use cases. These modules are being worked on to merge into the Ansible core engine under the web_infrastructure module group name.

## Getting Started

To get started contributing to these modules you will need git on your machine of choice. I would recommend forking this into a repo  of your own, make changes and then a merge request. You will need a github account to preform these actions. Once you have forked this working repositoring into a repository of your own, run git clone https://github.com<account>/<repository_name>.git and start work.

### Prerequisites

Seeing that this is for IBM software, a pre-requiste would be having access to the software binaries for integration testing. There are free developer accounts that allow this access. You must sign up for an IBM account to get access.
This step is not needed if you have the binaries local to you in another manor.

If your machine does not have ansible on it, or if you would preffer to keep development work seperate from systems ansible installation. Please access the latest upstream at https://github.com/ansible/ansible.git

```
git clone https://github.com/ansible/ansible.git
```
If this method is taken. Then setting up the ansible environment is the next steps. We will start with creating a python virtual environment. This assumes python3 is being used.

```
python3 -m virtualenv venv
```

Once the new virtual environment is created, run:

```
. ~/venv/bin/activate
```
This sources out the virtual environment and places you in it, seperating additional python libraries from the ones present on the host machine.

Now that we are in our virtual environment, we can create our ansible environment. To do so, run:

```
. ~/ansible/hacking/env-setup
```
If you'd like for this to be done on user sign in, place the above command in your users ~/.bashrc file.
To ensure that your environment is pointing to the correct ansible runtime, run:

```
which ansible
```
### Installing

To get started, please view the Getting Started section for initial steps. If you  don't fork, you can just clone the repository to your machine of choice. It is assumed that the latest version of ansible was cloned. Please see pre-requeists.

If this method is taken. Then setting up the ansible environment is the next steps. We will start with creating a python virtual environment. This assumes python3 is being used.

```
python3 -m virtualenv venv
```

Once the new virtual environment is created, run:

```
. ~/venv/bin/activate
```
This sources out the virtual environment and places you in it, seperating additional python libraries from the ones present on the host machine.

Now that we are in our virtual environment, we can create our ansible environment. To do so, run:

```
. ~/ansible/hacking/env-setup
```
If you'd like for this to be done on user sign in, place the above command in your users ~/.bashrc file.
To ensure that your environment is pointing to the correct ansible runtime, run:

```
which ansible
```

We can now install the needed python requirments to run anisble. Run the below command to do so:

```
pip3 install -r ~/ansible/requirments.txt
```

Your environment is now setup and ready to help contribute! Take a look at the modules for examples. A simple module to use as a basic understanding is the versionInfo module. 

## Running the tests

Running tests still needs work. This is lacking in units tests, and needs full integreation tests to ensure funcitonality.

## Deployment

See code examples for getting started with ansible examples.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Tom Davison** - *Initial work* - [TDavison784](https://github.com/tdavison784)

See also the list of [contributors](https://github.com/tdavison784/Ansible/contributors) who participated in this project.

## License

Working on getting these licensed...
