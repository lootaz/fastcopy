#include "fastcopy.h"

void fastcopy(const char* inFile, const char* outFile) {
    const int BUFFER_SIZE = 1024*1024;
    std::vector<char> inBuffer(BUFFER_SIZE);

    std::ios::sync_with_stdio(false);
    std::ifstream ins(inFile, std::ifstream::ate | std::ifstream::binary);
    std::ifstream::pos_type inFileSize = ins.tellg();

    int in = open(inFile, O_RDONLY | O_BINARY);
    int out = open(outFile, O_CREAT | O_WRONLY | O_BINARY, 0666);

    for(std::ifstream::pos_type bytesLeft = inFileSize, chunk = inBuffer.size();
        bytesLeft > 0;
        bytesLeft -= chunk) {

        if(bytesLeft < chunk) {
            chunk = bytesLeft;
        }
        read(in, &inBuffer[0], chunk);
        write(out, &inBuffer[0], chunk);
    }

    close(in);
    close(out);
}