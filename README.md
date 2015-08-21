Mesos
=========

This playbook deploys Mesos with Marathon in high availability mode across an AWS cluster of EC2 nodes using Ansible 2.

### Set up

This section will get Ansible and this repository set up on your machine.

#### Install Ansible

Make sure you have Ansible 2 installed.

The easiest way to do this is to track Ansible from the `devel` branch of their Git repository:

```text
$ git clone --recursive git@github.com:ansible/ansible.git
$ cd ansible
$ source hacking/env-setup
$ ansible --version # Should be ansible 2.x.x
```

##### If Ansible isn't working...

Using Ansible from source requires a few Pip packages that you might not have.

Some Linux distributions require these additional packages first or the
subsequent `pip install` may fail:

```text
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```

Make sure you have these:

```text
$ sudo pip install paramiko PyYAML Jinja2 httplib2 six docker-py boto
```

#### Requirements

At the time of writing this, `ansible-galaxy install` is broken for Ansible 2. As such, we've bundled third party roles directly into this repository. Many of the roles, including [Java](https://github.com/smola/ansible-java-role), [ZooKeeper](https://github.com/MichaelDrogalis/ansible-zookeeper) and [Mesos](https://github.com/AnsibleShipyard/ansible-mesos), have modifications and bug fixes of our own directly in this repository. All credit to these projects belongs exclusively to their creators.

### Credentials

This playbook interfaces with AWS, and optionally DockerHub. We're using Ansible Vault to encrypt sensitive data. Fill out `vars/main.yml` with your information and encrypt it before checking it back into source control.

### Usage

We've provided a convenience Python script to launch a Mesos cluster on AWS. Run the following:

```text
$ python scripts/aws_deploy.py -h
```

This will render a description of how to use the script. You can provision a new cluster and stand up new machines, deploy playbooks without adjusting the cluster size, or destroy the cluster.

This script supports colocation of services on the same machine. By provisionining with `--zookeeper` and `--mesos-master`, with `--n-instances` set to 3, you will get three machines in your cluster that each runs ZooKeeper and a Mesos master.

Running this script will prompt you for a password. Obtain the password from LastPass.

#### Script Example

```text
# Provision 3 EC2 machines and run ZooKeeper on them.
$ python scripts/aws_deploy.py --ansible-vault-password-file ~/.ansible-vault.txt --n-instances 3 --zookeeper us-west-2 mdrogalis provision

# Provision 3 EC2 machines each running both a Mesos Master and Marathon master
$ python scripts/aws_deploy.py --ansible-vault-password-file ~/.ansible-vault.txt --n-instances 3 --mesos-master --marathon us-west-2 mdrogalis provision

# Provision 2 EC2 machines running only Mesos slaves
$ python scripts/aws_deploy.py --ansible-vault-password-file ~/.ansible-vault.txt --n-instancews 2 --mesos-slave us-west-2 mdrogalis provision

# Scale down Mesos slaves from 2 to 1 instances
$ python scripts/aws_deploy.py --ansible-vault-password-file ~/.ansible-vault.txt --n-instances 1 --mesos-slave us-west-2 mdrogalis provision

# Make a change to the playbook, update all the machines
$ python scripts/aws_deploy.py --ansible-vault-password-file ~/.ansible-vault.txt us-west-2 mdrogalis freshen
```

### Service Discovery

We use HAProxy with Marathon to do service discovery. All services that run on Marathon must take their dependent hosts and ports in as parameters, often looking up "localhost" to a predefined, agreed-upon port to discover the dependent service.

### License

Copyright © 2015 ViaSat

Distributed under the Eclipse Public License 1.0.
