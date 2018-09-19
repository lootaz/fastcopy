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


def copy_func(args):
    src, dst, begin, size, max_buf_size = args

    with open(src, 'rb') as fsrc:
        with open(dst, 'r+b') as fdst:
            with closing(mmap.mmap(fsrc.fileno(), size, offset=begin, access=mmap.ACCESS_READ)) as msrc:
                with closing(mmap.mmap(fdst.fileno(), size, offset=begin)) as mdst:
                    offset = 0
                    while offset < size:
                        buffer_size = min(size - offset, max_buf_size)
                        mdst.write(msrc.read(buffer_size))
                        offset += buffer_size


@log
def fastcopy_via_mmap_pool(src, dst):
    MAX_BUFFER_SIZE = 1024 * 1024
    MAX_MMAP_SIZE = 512 * 1024 * 1024

    src_size = os.stat(src).st_size
    # Create empty dst file before (for linux)
    with open(dst, 'wb') as fdst:
        fdst.seek(src_size - 1)
        fdst.write(b'\0')

    full, remainder = divmod(src_size, MAX_MMAP_SIZE)
    if remainder:
        full += 1

    POOL_SIZE = max(mp.cpu_count() - 1, 1)

    p = mp.Pool(POOL_SIZE)
    args = []
    counter = 0
    for i in range(full):
        chunk_size = min(MAX_MMAP_SIZE, src_size - counter)
        args.append((src, dst, counter, chunk_size, MAX_BUFFER_SIZE))
        counter += chunk_size
    p.map(copy_func, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="source file path")
    parser.add_argument("dst", type=str, help="destination file path")

    args = parser.parse_args()
    fastcopy_via_mmap_pool(args.src, args.dst)
