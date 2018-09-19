import argparse
import datetime
import logging
import os

import _fastcopy

FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

def log(func):
    def func_wrapper(*args):
        logger.info("Start '%s'" % func.__name__)
        begin = datetime.datetime.now()
        func(*args)
        logger.info("Complete for %s" % (datetime.datetime.now() - begin))
    return func_wrapper

@log
def run(src, dst):
    if os.path.exists(dst_path):
        os.remove(dst_path)

    _fastcopy.fastcopy(src_path, dst_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="source file path")
    parser.add_argument("dst", type=str, help="destination file path")

    args = parser.parse_args()
    run(args.src, args.dst)
