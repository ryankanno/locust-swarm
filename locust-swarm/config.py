#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser


def _parse(config_name='locust-swarm.cfg'):
    config = ConfigParser.SafeConfigParser()
    config.read(config_name)
    return config


config = _parse()

# vim: filetype=python
