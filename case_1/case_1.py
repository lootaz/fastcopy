import argparse
import datetime
import logging
import mmap
import os
from contextlib import closing
import multiprocessing as mp

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
def via_mmap(src, dst):
    MAX_BUFFER_SIZE = 64 * 1024
    MAX_MMAP_SIZE = 512 * 1024 * 1024
    src_size = os.stat(src).st_size

    # Create empty dst file before (for linux)
    with open(dst, 'wb') as fdst:
        fdst.seek(src_size - 1)
        fdst.write(b'\0')

    with open(src, 'rb') as fsrc:
        with open(dst, 'r+b') as fdst:
            offset = 0
            total = 0
            msrc = None
            mdst = None
            while offset < src_size:
                buffer_size = min(src_size - offset, MAX_BUFFER_SIZE)
                if total <= 0:
                    if msrc:
                        msrc.close()
                    if mdst:
                        mdst.close()
                    mmap_size = min(src_size - offset, MAX_MMAP_SIZE)
                    msrc = mmap.mmap(fsrc.fileno(), mmap_size, offset=offset, access=mmap.ACCESS_READ)
                    mdst = mmap.mmap(fdst.fileno(), mmap_size, offset=offset)

                    total = MAX_MMAP_SIZE

                mdst.write(msrc.read(buffer_size))
                offset += buffer_size
                total -= buffer_size


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="source file path")
    parser.add_argument("dst", type=str, help="destination file path")

    args = parser.parse_args()
    via_mmap(args.src, args.dst)

