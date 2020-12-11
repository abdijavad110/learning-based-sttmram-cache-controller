#include "auxiliary.h"
#include "simulator.h"


void Auxiliary::initiate(int cache_size, int chunk_size) {
    chunkSize = chunk_size;
    chunkNo = (int) cache_size / chunk_size;
    AuxElem arr[chunkNo];       // fixme: (JH) check if this syntax is correct or should use malloc instead
    array = arr;                // fixme: (JH) what is this warning
    Dens dens[chunkNo];
    densities = dens;
}

void Auxiliary::new_acc(int addr) {
    int idx = addr;                // fixme: (JH) find the proper translation for address
    array[idx].new_acc(addr);
}

void Auxiliary::update_table() {    // fixme: (JH) use properly
    calc_densities();
    for () { // fixme: (JH) for on approx_table or dens_table?
        // fixme: (JH) find the new value for quality
    }
}

void Auxiliary::calc_densities() {
    for (int i=0; i<chunkNo; i++) {
        densities[i] = array[i].calc_densities();
        array[i].reset()
    }
}
