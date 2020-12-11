//
// Created by javad on 11/12/2020.
//

#include "aux_elem.h"

AuxElem::AuxElem() {
    reset();
}

void AuxElem::new_acc(int a) {
    accesses += 1;
    // fixme: (JH) implemet addr & time updates
}

void AuxElem::reset() {
    accesses = 0;
    addr.min = -1;
    addr.max = 0;
    time.start = -1;
    time.end = 0;
}

Dens AuxElem::calc_densities() {
    Dens res;
    res.spatial = 0;
    res.temporal = 0;
    if (accesses > 2) {
        if (addr.min != addr.max) res.spatial = accesses / (addr.max - addr.min);
        if (time.start != time.end) res.spatial = accesses / (addr.max - addr.min);
    }
    return res
}
