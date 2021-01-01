#ifndef SNIPER_MEM_AUXILIARY_H
#define SNIPER_MEM_AUXILIARY_H

#include "chunk.h"

class ChunkManager {
private:
    static int chunkNo;
    static int chunkSize;
    static Chunk *chunks[];
    static Dens *densities[];

    static void calc_densities();

public:
    static void initiate(int cache_size, int chunk_size);

    static void new_acc(int addr);

    static void update_table();
};


#endif