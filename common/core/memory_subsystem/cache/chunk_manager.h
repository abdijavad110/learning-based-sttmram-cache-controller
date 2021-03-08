#ifndef SNIPER_MEM_AUXILIARY_H
#define SNIPER_MEM_AUXILIARY_H

#include "chunk.h"

class ChunkManager {
private:

    Chunk current_chunk;
    int qual_write_num[5] = {0, 0, 0, 0, 0};
    int high_cur_wrt_num = 0;

    void calc_densities();
    double get_qual(float min, float max, float current);

public:
//    static void initiate();

    ~ChunkManager();

    void new_acc(long long int  addr);

    void update_table();
};


#endif