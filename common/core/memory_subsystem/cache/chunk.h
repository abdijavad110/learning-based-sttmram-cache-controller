#ifndef SNIPER_MEM_AUX_ELEM_H
#define SNIPER_MEM_AUX_ELEM_H

struct Dens {
    float spatial;
    float temporal;
};


class Chunk {
private:
    int accesses;
    struct A {
        long long int  min;
        long long int  max;
    } addr;
    struct T {
        float start;
        float end;
    } time;
public:
    Chunk();

    void new_acc(long long int a);

    void reset();

    Dens calc_densities();
};


#endif //SNIPER_MEM_AUX_ELEM_H
