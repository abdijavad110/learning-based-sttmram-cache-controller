#include "chunk_manager.h"
#include "simulator.h"


double qual_array[] = {1e-3, 1e-4, 1e-5, 1e-6, 1e-7};
int qual_arr_size = sizeof(qual_array)/sizeof(qual_array[0]);

void ChunkManager::new_acc(long long int  addr) {
    current_chunk.new_acc(addr);
    double ber = Sim()->get_error_rate(addr);
//    if (ber != 0) printf("%.9f\t", ber);
    if (ber == 0) {
        high_cur_wrt_num++;
        return;
    }
    for (int i=0; i<qual_arr_size; i++) {
        if (ber == qual_array[i]) {
            qual_write_num[i]++;
            return;
        }
    }
}

ChunkManager::~ChunkManager() {
    if (high_cur_wrt_num > 0) {
        printf("\n\nnumber of writes per ber:\n");
        printf("4dcc865dcd8a0440f3e955e66928b6a9");
        for (int i = 0; i < qual_arr_size; i++) {
            printf("%.9f: %d\n", qual_array[i], qual_write_num[i]);
        }
        printf("high current: %d\n", high_cur_wrt_num);
        printf("4dcc865dcd8a0440f3e955e66928b6a9");
        printf("\n\n");
    }
}

void ChunkManager::update_table() {    // fixme: (JH) use properly
//    return;
    Dens dens = current_chunk.calc_densities();
    float spatial = dens.spatial;
    float temporal = dens.temporal;

//    printf("\n\nInside update========================================================\n");
    for(int i = 0; i < approx_table_max_entry; i++) {

        double min = Sim()->approx_table[i].temp.min;
        double max = Sim()->approx_table[i].temp.max;

        if (temporal > max) Sim()->approx_table[i].temp.max = temporal;
        if (temporal < min || min == -1) Sim()->approx_table[i].temp.min = temporal;

//        double new_spat_qual = get_qual(Sim()->approx_table[i].spat.min, Sim()->approx_table[i].spat.max, spatial);
        double new_temp_qual = get_qual(Sim()->approx_table[i].temp.min, Sim()->approx_table[i].temp.max, temporal);
        if (new_temp_qual < Sim()->approx_table[i].quality_level_ref) {
            Sim()->approx_table[i].quality_level = Sim()->approx_table[i].quality_level_ref;
            continue;
        }
        Sim()->approx_table[i].quality_level = new_temp_qual;
        //fixme: felan faghat temporal
//        printf("%.9f -> ", Sim()->approx_table[i].quality_level);
//        printf("%.9f\t", Sim()->approx_table[i].quality_level);
    }
//    printf("========================================================\n");
    current_chunk.reset();

//        if((address >= (IntPtr) approx_table[i].start_address) && (address <= (IntPtr) approx_table[i].end_address))
//            return i;
}

double
ChunkManager::get_qual(float min, float max, float current){
//    return 1e-5;
//    max = max *10;
    if (current == 0) return 0;
    if (current <= min)
        return qual_array[0];
    else if (current >= max)
        return qual_array[qual_arr_size-1];
    else {
        float gap = max - min;
        float map_level = (current - min)/(gap);
        int idx = map_level*qual_arr_size;
        return qual_array[idx];
//        float map_level = (current - min)/(gap) * 31;
//        if (map_level < 16) return qual_array[0];
//        else if (map_level < 24) return qual_array[1];
//        else if (map_level < 28) return qual_array[2];
//        else if (map_level < 30) return qual_array[3];
//        else return qual_array[4];
    }
}
