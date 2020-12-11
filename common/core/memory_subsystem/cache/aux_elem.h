//
// Created by javad on 11/12/2020.
//

#ifndef SNIPER_MEM_AUX_ELEM_H
#define SNIPER_MEM_AUX_ELEM_H

struct Dens {
    float spatial;
    float temporal;
};


class AuxElem {
private:
    int accesses;
    struct A {
        int min;
        int max;
    } addr;
    struct T {
        float start;
        float end;
    } time;
public:
    AuxElem();

    void new_acc(int a);

    void reset();

    Dens calc_densities();
};


#endif //SNIPER_MEM_AUX_ELEM_H
