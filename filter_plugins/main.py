import boto.ec2
import uuid, os, sys

def is_true(x):
  return (x == True) or (x == 'True')

def append_uuid(x):
  return x + str(uuid.uuid4())

def vm_name(ip):
  from novaclient import client as novaclient

  creds = {}
  creds['username'] = os.getenv("OS_USERNAME")
  creds['api_key'] = os.getenv("OS_PASSWORD")
  creds['auth_url'] = os.getenv("OS_AUTH_URL")
  creds['project_id'] = os.getenv("OS_TENANT_NAME")

  nova = novaclient.Client("2", **creds)
  servers = nova.servers.list()

  s = filter(lambda s: (s.networks.get(creds['project_id'])[0] == ip), servers)[0]
  return s.name

def aws_tags(roles):
  tags = {}
  tags[roles[4]] = True

  if is_true(roles[0]):
    tags["mesos_zookeeper"] = True
  if is_true(roles[1]):
    tags["mesos_master"] = True
  if is_true(roles[2]):
    tags["mesos_slave"] = True
  if is_true(roles[3]):
    tags["mesos_marathon"] = True
  return tags

def instance_tags(roles):
  tags = aws_tags(roles)
  tags["Name"] = "mesos-node-{}".format(roles[4])
  tags["cluster_id"] = roles[4]

  return tags

def aws_security_groups(roles):
  sgs = ["[{}] Mesos Public Subnet Security Group".format(roles[4])]

  if is_true(roles[0]):
    sgs.append("[{}] ZooKeeper Security Group".format(roles[4]))
  if is_true(roles[1]):
    sgs.append("[{}] Mesos Master Security Group".format(roles[4]))
  if is_true(roles[2]):
    sgs.append("[{}] Mesos Slave Security Group".format(roles[4]))
  if is_true(roles[3]):
    sgs.append("[{}] Marathon Security Group".format(roles[4]))
  return sgs

def to_zookeeper_cluster_string(args):
  return (":" + str(args[1]) + ",").join(args[0]) + (":" + str(args[1]))

def private_zk_nodes(aws_region, cluster_id, access_key, secret_access_key):
  ips = []
  conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

  for r in conn.get_all_reservations():
    for i in r.instances:
      if (i.tags.get("cluster_id") == cluster_id) and (i.state == "running"):
        if i.tags.get("mesos_zookeeper") == 'True':
          ips.append(i.private_ip_address)
  return ips

def public_zk_nodes(aws_region, cluster_id, access_key, secret_access_key):
  ips = []
  conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

  for r in conn.get_all_reservations():
    for i in r.instances:
      if (i.tags.get("cluster_id") == cluster_id) and (i.state == "running"):
        if i.tags.get("mesos_zookeeper") == 'True':
          ips.append(i.ip_address)
  return ips

def mesos_master_nodes(aws_region, cluster_id, access_key, secret_access_key):
  ips = []
  conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

  for r in conn.get_all_reservations():
    for i in r.instances:
      if (i.tags.get("cluster_id") == cluster_id) and (i.state == "running"):
        if i.tags.get("mesos_master") == 'True':
          ips.append(i.ip_address)
  return ips

def mesos_slave_nodes(aws_region, cluster_id, access_key, secret_access_key):
  ips = []
  conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

  for r in conn.get_all_reservations():
    for i in r.instances:
      if (i.tags.get("cluster_id") == cluster_id) and (i.state == "running"):
        if i.tags.get("mesos_slave") == 'True':
          ips.append(i.ip_address)
  return ips

def mesos_marathon_nodes(aws_region, cluster_id, access_key, secret_access_key):
  ips = []
  conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

  for r in conn.get_all_reservations():
    for i in r.instances:
      if (i.tags.get("cluster_id") == cluster_id) and (i.state == "running"):
        if i.tags.get("mesos_marathon") == 'True':
          ips.append(i.ip_address)
  return ips

class FilterModule(object):
    ''' Ansible UUID jinja2 filters '''

    def filters(self):
      return {
        'append_uuid': append_uuid,
        'vm_name': vm_name,
        'aws_security_groups': aws_security_groups,
        'aws_tags': aws_tags,
        'instance_tags': instance_tags,
        'to_zookeeper_cluster_string': to_zookeeper_cluster_string,
        'private_zk_nodes': private_zk_nodes,
        'public_zk_nodes': public_zk_nodes,
        'mesos_master_nodes': mesos_master_nodes,
        'mesos_slave_nodes': mesos_slave_nodes,
        'mesos_marathon_nodes': mesos_marathon_nodes,
      }
