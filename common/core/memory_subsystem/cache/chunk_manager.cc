#include "chunk_manager.h"
#include "simulator.h"


void ChunkManager::initiate(int cache_size, int chunk_size) {
    chunkSize = chunk_size;
    chunkNo = (int) cache_size / chunk_size;
    Chunk arr[chunkNo];       // fixme: (JH) check if this syntax is correct or should use malloc instead
    chunks = arr;                // fixme: (JH) what is this warning
    Dens dens[chunkNo];
    densities = dens;
}

void ChunkManager::new_acc(int addr) {
    int idx = addr;                // fixme: (JH) find the proper translation for address
    chunks[idx].new_acc(addr);
}

void ChunkManager::update_table() {    // fixme: (JH) use properly
    calc_densities();
    for () { // fixme: (JH) for on approx_table or dens_table?
        // fixme: (JH) find the new value for quality
    }
}

void ChunkManager::calc_densities() {
    for (int i=0; i<chunkNo; i++) {
        densities[i] = chunks[i].calc_densities();
        chunks[i].reset()
    }
}
