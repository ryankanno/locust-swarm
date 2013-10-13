#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boto.ec2 import connect_to_region
from config import config
from fabric.api import env
from fabric.api import put
from fabric.api import roles
from fabric.api import run
from fabric.api import sudo
from fabric.tasks import execute
from multiprocessing import Pool
from time import sleep


AMI_ID = config.get('aws', 'ami_id')
AWS_REGION = config.get('aws', 'aws_region')
AMI_INSTANCE_TYPE = config.get('aws', 'ami_instance_type')
AMI_ACCESS_KEY_ID = config.get('aws', 'access_key_id')
AMI_SECRET_ACCESS_KEY = config.get('aws', 'secret_access_key')
AWS_KEY_NAME = config.get('aws', 'aws_key_name', None)
FABRIC_ENV_USER = config.get('fabric', 'user', None)
FABRIC_ENV_KEY_FILENAME = config.get('fabric', 'key_filename', None)


pool = Pool(processes=4)


def _get_instances(filters):
    
    conn = connect_to_region(
        AWS_REGION,
        aws_access_key_id=AMI_ACCESS_KEY_ID,
        aws_secret_access_key=AMI_SECRET_ACCESS_KEY)

    return conn.get_all_instances(filters=filters)


def _run_instances(ami_id, tag_dict, security_groups):
    
    conn = connect_to_region(
        AWS_REGION,
        aws_access_key_id=AMI_ACCESS_KEY_ID,
        aws_secret_access_key=AMI_SECRET_ACCESS_KEY)

    reservation = conn.run_instances(
        image_id=ami_id,
        key_name=AWS_KEY_NAME,
        security_groups=[],
        instance_type=AMI_INSTANCE_TYPE).instances[0]

    _wait_for_instance_state(reservation, 'running')

    for tag, value in tag_dict.items():
        reservation.add_tag(tag, value)

    return reservation


def _wait_for_instance_state(instance, state, num_secs_to_sleep=20,
                             max_num_times=5):
    num_times = 0
    while True and num_times < max_num_times:
        instance.update()
        if state == instance.state:
            return
        else:
            num_times += 1
            sleep(num_secs_to_sleep)
    raise Exception


def create_master(ami_id, name='Locust-Master'):
    return _run_instances(ami_id, {'Name': name})


def create_slave(ami_id, name='Locust-Slave'):
    return _run_instances(ami_id, {'Name': name})


def get_masters(name='Locust-Master'):
    return _get_instances({'tag:Name': name})


def get_slaves(name='Locust-Slave'):
    return _get_instances({'tag:Name': name})


@roles('master')
def bootstrap_master():
    _bootstrap("master")
    run('locust -f /tmp/locust/bootstrap-master/locustfile.py --master &', pty=False) 


@roles('slave')
def bootstrap_slave(master_ip_address):
    _bootstrap("slave")
    run("locust -f /tmp/locust/bootstrap-slave/locustfile.py --slave --master-host {0} &".format(master_ip_address), pty=False)

def _bootstrap(role):
    run('mkdir -p /tmp/locust/')
    put("/Users/ryankanno/Projects/github/me/locust-swarm/example/bootstrap-{0}/".format(role), '/tmp/locust/')
    sudo("chmod +x /tmp/locust/bootstrap-{0}/bootstrap.sh".format(role))
    sudo("/tmp/locust/bootstrap-{0}/bootstrap.sh".format(role))


def update_role_defs(reservations, role_key):
    env.roledefs[role_key] = []
    for reservation in reservations:
        for instance in reservation.instances:
            if instance.ip_address:
                env.roledefs[role_key].append(instance.ip_address)


if __name__ == '__main__':
    #create_master(AMI_ID)

    # TODO: parallelize and parameterize 
    #create_slave(AMI_ID)
    #create_slave(AMI_ID)
    #create_slave(AMI_ID)
    #create_slave(AMI_ID)

    masters = get_masters()
    slaves = get_slaves()

    update_role_defs(masters, 'master')
    update_role_defs(slaves, 'slave')

    env.user = FABRIC_ENV_USER
    env.key_filename = FABRIC_ENV_KEY_FILENAME

    execute(bootstrap_master)
    execute(bootstrap_slave)

# vim: filetype=python
