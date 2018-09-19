# fastcopy
# case_0
Via Posix API Extension

Build:
- python setup.py build_ext --inplace

# case_1
Via mmap
~ near 1,5 minutes faster on my machine on 10G file size

# case_2
Via mmap and multiprocessing pool
~ near 2 minutes faster on my machine on 10G file size with 3 processes
 