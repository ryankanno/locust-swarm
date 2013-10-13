#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cProfile
import functools
import platform
import pstats
import logging
import StringIO
import sys
import time
import traceback


__all__ = ['main']
__author__ = "Ryan Kanno <ryankanno@localkinegrinds.com>"
__url__ = "http://github.com/ryankanno/locust-swarm/"
__version__ = "0.0.1"


LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


def init_argparser():
    common = argparse.ArgumentParser(description=__doc__, add_help=False)
    common.add_argument('-c', '--config', type=str, 
                        help='path to config file')
    common.add_argument('-v', '--verbose', action='store_true',
                        help='increase chattiness of script')

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(title='supported commands', metavar="<command>")

    parser_swarm_up = subparsers.add_parser('up', parents=[common], help='bringing up a swarm')
    parser_swarm_up.add_argument('-d', '--directory', type=str, 
                                 help='directory that contains all the slave/master files')

    parser_swarm_down = subparsers.add_parser('down', parents=[common], help='shutting down a swarm')
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = init_argparser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    try:
        swarm_runner(args)
    except:
        trace = traceback.format_exc()
        logging.error("OMGWTFBBQ: {0}".format(trace))
        sys.exit(1)

    # Yayyy-yah
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# vim: filetype=python
