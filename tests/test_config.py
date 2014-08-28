#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.tools import raises
from locust_swarm.config import DEFAULT_CFG_FILEPATH
from locust_swarm.config import DEFAULT_MASTER_ROLE_NAME
from locust_swarm.config import DEFAULT_SLAVE_ROLE_NAME
from locust_swarm.config import DEFAULT_MASTER_BOOTSTRAP_DIR
from locust_swarm.config import DEFAULT_SLAVE_BOOTSTRAP_DIR
from locust_swarm.config import DEFAULT_NUM_SLAVES
from locust_swarm.config import DEFAULT_CUSTOM_TAG_NAME
from locust_swarm.config import get_config
import unittest


class TestConfig(unittest.TestCase):

    def test_default_variables(self):
        eq_('locust-swarm.cfg', DEFAULT_CFG_FILEPATH)
        eq_('locust-master', DEFAULT_MASTER_ROLE_NAME)
        eq_('locust-slave', DEFAULT_SLAVE_ROLE_NAME)
        eq_('./bootstrap-master', DEFAULT_MASTER_BOOTSTRAP_DIR)
        eq_('./bootstrap-slave', DEFAULT_SLAVE_BOOTSTRAP_DIR)
        eq_(5, DEFAULT_NUM_SLAVES)
        eq_('MachineRole', DEFAULT_CUSTOM_TAG_NAME)

    @raises(Exception)
    def test_get_config_with_invalid_config_path(self):
        get_config('/f/a/k/e.config')

    def test_get_config_with_valid_config_path_returns_config(self):
        get_config('/f/a/k/e.config')

# vim: filetype=python
