#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from locust_swarm.helpers import get_abs_path
from locust_swarm.helpers import can_ssh
import unittest


class TestHelpers(unittest.TestCase):

    def test_get_abs_path(self):
        path = get_abs_path('~')
        ok_('~' not in path)

    def test_can_ssh(self):
        ok_(can_ssh('github.com'))
        ok_(not can_ssh('espn.com'))

# vim: filetype=python
