extern "C" {
#include <stdlib.h>
#include <stdio.h>
#include <io.h>
#include <fcntl.h>

extern void fastcopy(const char* inFile, const char* outFile);
}

#include <fstream>
#include <vector>
#include <iostream>