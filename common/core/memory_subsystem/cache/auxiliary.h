#ifndef SNIPER_MEM_AUXILIARY_H
#define SNIPER_MEM_AUXILIARY_H

#include "aux_elem.h"

class Auxiliary {
private:
    static int chunkNo;
    static int chunkSize;
    static AuxElem *array[];
    static Dens *densities[];

    static void calc_densities();

public:
    static void initiate(int cache_size, int chunk_size);

    static void new_acc(int addr);

    static void update_table();
};


#endif