//
// Created by javad on 11/12/2020.
//

#include <time.h>
#include "chunk.h"


Chunk::Chunk() {
    reset();
}

void Chunk::new_acc(int a) {
    accesses += 1;

    if (a < addr.min || addr.min == -1)
        addr.min = a;
    else if (a > addr.max)
        addr.max = a;

    double now = double(clock())/CLOCKS_PER_SEC;
    if (time.start == -1)
        time.start = now;
    time.end = now;

}

void Chunk::reset() {
    accesses = 0;
    addr.min = -1;
    addr.max = 0;
    time.start = -1;
    time.end = 0;
}

Dens Chunk::calc_densities() {
    Dens res;
    res.spatial = 0;
    res.temporal = 0;
    if (accesses > 2) {
        if (addr.min != addr.max) res.spatial = accesses / (addr.max - addr.min);
        if (time.start != time.end) res.temporal = accesses / (time.end - time.start);
    }
    return res;
}
