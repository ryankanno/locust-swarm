#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
from helpers import get_abs_path


DEFAULT_CFG_FILEPATH = 'locust-swarm.cfg'
DEFAULT_MASTER_ROLE_NAME = 'locust-master'
DEFAULT_SLAVE_ROLE_NAME = 'locust-slave'
DEFAULT_MASTER_BOOTSTRAP_DIR = './bootstrap-master'
DEFAULT_SLAVE_BOOTSTRAP_DIR = './bootstrap-slave'
DEFAULT_NUM_SLAVES = 5
DEFAULT_CUSTOM_TAG_NAME = 'MachineRole'


def _parse(path_to_config=DEFAULT_CFG_FILEPATH):
    config = ConfigParser.SafeConfigParser()
    config_path = get_abs_path(path_to_config)
    try:
        with open(config_path, 'r') as f:
            config.readfp(f)
    except IOError:
        raise Exception("Unable to open locust-swarm configuration file @ {0}"
                        .format(config_path))
    return config

get_config = _parse

# vim: filetype=python
