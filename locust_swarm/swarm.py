#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import traceback

from .config import DEFAULT_CFG_FILEPATH
from .config import DEFAULT_NUM_SLAVES
from .config import DEFAULT_MASTER_BOOTSTRAP_DIR
from .config import DEFAULT_SLAVE_BOOTSTRAP_DIR
from .runner import swarm_down
from .runner import swarm_down_master
from .runner import swarm_down_slaves
from .runner import swarm_up
from .runner import swarm_up_master
from .runner import swarm_up_slaves


__all__ = ['main']
__author__ = "Ryan Kanno <ryankanno@localkinegrinds.com>"
__url__ = "http://github.com/ryankanno/locust-swarm/"
__version__ = "0.0.1"


LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


def init_argparser():
    common = argparse.ArgumentParser(
        description=__doc__, add_help=False)

    common.add_argument(
        '-c', '--config', type=str, default=DEFAULT_CFG_FILEPATH,
        help='path to locust-swarm config file')

    common.add_argument(
        '-v', '--verbose', action='store_true',
        help='increase chattiness of script')

    parser = argparse.ArgumentParser(description=__doc__)

    cmd_subparser = parser.add_subparsers(
        title='supported commands',
        metavar="<command>")

    swarm_up_parser = cmd_subparser.add_parser(
        'up', parents=[common],
        help='brings up a swarm',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    swarm_up_options = swarm_up_parser.add_subparsers(
        title='supported roles', metavar="<roles>")

    swarm_up_slave = swarm_up_options.add_parser(
        'slaves', parents=[common],
        help='brings up locust slaves',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    swarm_up_slave.add_argument(
        '-d', '--directory', type=str,
        default=DEFAULT_SLAVE_BOOTSTRAP_DIR,
        help='directory that contains the locust slave bootstrap files')
    swarm_up_slave.add_argument(
        '-s', '--num_slaves', type=int,
        default=DEFAULT_NUM_SLAVES,
        help='number of slaves to bring up')

    swarm_up_slave.set_defaults(func=swarm_up_slaves)

    swarm_up_master_cmd = swarm_up_options.add_parser(
        'master', parents=[common],
        help='brings up locust master',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    swarm_up_master_cmd.add_argument(
        '-d', '--directory', type=str,
        default=DEFAULT_MASTER_BOOTSTRAP_DIR,
        help='directory that contains all the locust master bootstrap files')
    swarm_up_master_cmd.set_defaults(func=swarm_up_master)

    swarm_down_parser = cmd_subparser.add_parser(
        'down', parents=[common],
        help='bringing down a swarm',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    swarm_down_options = swarm_down_parser.add_subparsers(
        title='supported roles', metavar="<roles>")

    swarm_down_slave = swarm_down_options.add_parser(
        'slaves', parents=[common],
        help='bringing down locust slaves',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    swarm_down_slave.set_defaults(func=swarm_down_slaves)

    swarm_down_master_cmd = swarm_down_options.add_parser(
        'master', parents=[common],
        help='bringing down locust master',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    swarm_down_master_cmd.set_defaults(func=swarm_down_master)

    swarm_down_all = swarm_down_options.add_parser(
        'all', parents=[common],
        help='brings down locust master and slaves',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    swarm_down_all.set_defaults(func=swarm_down)

    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = init_argparser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    try:
        args.func(args)
    except:
        trace = traceback.format_exc()
        logging.error("OMGWTFBBQ: {0}".format(trace))
        sys.exit(1)

    # Yayyy-yah
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# vim: filetype=python
