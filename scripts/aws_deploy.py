import argparse
from subprocess import call

parser = argparse.ArgumentParser(description = 'Deploy and manage a Mesos cluster on AWS.')

parser.add_argument("region",
                    choices = ["us-east-1", "us-west-1", "us-west-2"],
                    help = "The AWS region to search and deploy Mesos into")

parser.add_argument('cluster-id',
                    help = 'A unique identifier per AWS region for your Mesos cluster')

parser.add_argument('action', choices = ["provision", "freshen", "deploy-marathon", "destroy"],
                    help = 'The action to perform on the cluster')

parser.add_argument("-n", "--n-instances", dest = 'n', type = int,
                    help = "The number of instances to provision")

parser.add_argument("-z", "--zookeeper", dest = 'zookeeper', action = 'store_true',
                    help = "Provision these machines with ZooKeeper installed")

parser.add_argument("-m", "--mesos-master", dest = 'mesos_master', action = 'store_true',
                    help = "Provision these machines with a Mesos master installed")

parser.add_argument("-s", "--mesos-slave", dest = 'mesos_slave', action = 'store_true',
                    help = "Provision these machines with a Mesos slave installed")

parser.add_argument("-a", "--marathon", dest = 'marathon', action ='store_true',
                    help = "Provision these machines with a Marathon master installed")

parser.add_argument("-f", "--ansible-vault-password-file", dest = 'password_file',
                    help = "The location of the file containing the Ansible Vault password")

args = parser.parse_args()
arg_vars = vars(args)

ansible_prompt = "--ask-vault-pass"
if arg_vars["password_file"]:
  ansible_prompt = "--vault-password-file={}".format(args.password_file)


if args.action == "provision":
  if not args.zookeeper and not args.mesos_master and not args.mesos_slave and not args.marathon:
    print parser.error("Provisioning requires at least one role to be set (e.g. ZooKeeper, Mesos Master, etc)")
  elif not args.n:
    print parser.error("Provision machines requires --n-instances to be set to a positive integer")
  else:
    call(["ansible-playbook",
          ansible_prompt,
          "--private-key=~/.ssh/aws-us-west-2-mesos.pem",
          "-e", "remote_user=ubuntu",
          "-e", "aws_key_name=aws-us-west-2-mesos",
          "-e", "mesos_cluster_id={}".format(arg_vars["cluster-id"]),
          "-e", "aws_provision=True",
          "-e", "aws_region={}".format(arg_vars["region"]),
          "-e", "n_vms={}".format(arg_vars["n"]),
          "-e", "mesos_zookeeper={}".format(arg_vars["zookeeper"]),
          "-e", "mesos_master={}".format(arg_vars["mesos_master"]),
          "-e", "mesos_slave={}".format(arg_vars["mesos_slave"]),
          "-e", "mesos_marathon={}".format(arg_vars["marathon"]),
          "-i", ",",
          "tasks/aws.yml"])
elif args.action == "freshen":
    call(["ansible-playbook",
          ansible_prompt,
          "--private-key=~/.ssh/aws-us-west-2-mesos.pem",
          "-e", "remote_user=ubuntu",
          "-e", "aws_key_name=aws-us-west-2-mesos",
          "-e", "mesos_cluster_id={}".format(arg_vars["cluster-id"]),
          "-e", "aws_provision=False",
          "-e", "aws_region={}".format(arg_vars["region"]),
          "-i", ",",
          "tasks/aws.yml"])
elif args.action == "deploy-marathon":
    call(["ansible-playbook",
          ansible_prompt,
          "--private-key=~/.ssh/aws-us-west-2-mesos.pem",
          "-e", "remote_user=ubuntu",
          "-e", "aws_key_name=aws-us-west-2-mesos",
          "-e", "mesos_cluster_id={}".format(arg_vars["cluster-id"]),
          "-e", "aws_region={}".format(arg_vars["region"]),
          "-i", ",",
          "tasks/marathon.yml"])
elif args.action == "destroy":
    call(["ansible-playbook",
          ansible_prompt,
          "--private-key=~/.ssh/aws-us-west-2-mesos.pem",
          "-e", "remote_user=ubuntu",
          "-e", "aws_key_name=aws-us-west-2-mesos",
          "-e", "mesos_cluster_id={}".format(arg_vars["cluster-id"]),
          "-e", "aws_region={}".format(arg_vars["region"]),
          "-e", "aws_provision=False",
          "-e", "aws_destroy=True",
          "-i", ",",
          "tasks/aws_destroy.yml"])
