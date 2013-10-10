#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boto.ec2 import connect_to_region
from config import config
from fabric.api import env
from fabric.api import sudo
from fabric.api import task
from fabric.tasks import execute
from multiprocessing import Pool
from time import sleep


AMI_ID = "ami-ad3660c4"
AWS_REGION = config.get('aws', 'aws_region')
AMI_INSTANCE_TYPE = config.get('aws', 'ami_instance_type')
AMI_ACCESS_KEY_ID = config.get('aws', 'access_key_id')
AMI_SECRET_ACCESS_KEY = config.get('aws', 'secret_access_key')
AWS_KEY_NAME = config.get('aws', 'aws_key_name', None)
FABRIC_ENV_USER = config.get('fabric', 'user', None)
FABRIC_ENV_KEY_FILENAME = config.get('fabric', 'key_filename', None)


pool = Pool(processes=4)


def _run_instances(ami_id, tag_dict):
    
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


@roles('master')
def start_master():
    pass


@roles('slave')
def start_slave():
    pass

    
@task
def update():
    sudo('apt-get update && apt-get upgrade -y')
    sudo('apt install python') 
    sudo('apt install python-pip python-dev build-essential')
    sudo('pip install --upgrade pip')
    put('./sample-locust.py', '/tmp/sample-locust.py')

if __name__ == '__main__':
    master = create_master(AMI_ID)

    # TODO: parallelize and parameterize 
    slave1 = create_slave(AMI_ID)
    slave2 = create_slave(AMI_ID)

    env.hosts = [master.ip_address, slave1.ip_address, slave2.ip_address]
    env.user = FABRIC_ENV_USER
    env.key_filename = FABRIC_ENV_KEY_FILENAME
    execute(update)


# vim: filetype=python
