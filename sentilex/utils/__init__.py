from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import importlib


def add_logging_arguments(parser, default=logging.WARNING):
    """
    Add options to configure logging level
    :param parser:
    :param default:
    :return:
    """
    parser.add_argument(
        '--debug',
        help="Set logging level to DEBUG",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=default,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose. Sets logging level to INFO",
        action="store_const",
        dest="loglevel",
        const=logging.INFO
    )


def configure_colored_logging(loglevel):
    """
    Configure colored logging
    :param loglevel:
    :return:
    """
    import coloredlogs
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
    field_styles['asctime'] = {}
    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
    level_styles['debug'] = {}
    coloredlogs.install(
            level=loglevel,
            use_chroot=False,
            fmt='%(asctime)s %(levelname)-8s %(name)s  - %(message)s',
            level_styles=level_styles,
            field_styles=field_styles)


def get_class_from_path(path):
    """
    get class given path
    :param path:
    :return:
    """
    path_list = path.split('.')
    module = importlib.import_module('.'.join(path_list[0:-1]))
    iclass = getattr(module, path_list[-1])
    return iclass


def update_config(defaults, custom):
    config = defaults if defaults else {}
    if custom:
        config.update(custom)
    return config
