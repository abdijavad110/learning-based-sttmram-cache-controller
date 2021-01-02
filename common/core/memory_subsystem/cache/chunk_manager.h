#ifndef SNIPER_MEM_AUXILIARY_H
#define SNIPER_MEM_AUXILIARY_H

#include "chunk.h"

class ChunkManager {
private:

    Chunk current_chunk;

    void calc_densities();
    double get_qual(float min, float max, float current);

public:
//    static void initiate();

    void new_acc(int addr);

    void update_table();
};


#endif