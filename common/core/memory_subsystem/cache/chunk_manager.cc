#include "chunk_manager.h"
#include "simulator.h"


//void ChunkManager::initiate() {
//    current_chunk = new Chunk();
//}


float qual_array[] = {10e-3, 10e-4, 10e-5, 10e-6, 10e-7};
int qual_arr_size = sizeof(qual_array)/sizeof(qual_array[0]);

void ChunkManager::new_acc(int addr) {
    current_chunk.new_acc(addr);
}

void ChunkManager::update_table() {    // fixme: (JH) use properly
    Dens dens = current_chunk.calc_densities();
    float spatial = dens.spatial;
    float temporal = dens.temporal;

    for(int i = 0; i < approx_table_max_entry; i++) {
        double new_spat_qual = get_qual(Sim()->approx_table[i].spat.min, Sim()->approx_table[i].spat.max, spatial);
        double new_temp_qual = get_qual(Sim()->approx_table[i].temp.min, Sim()->approx_table[i].temp.max, temporal);
        //fixme: felan faghat temporal
        Sim()->approx_table[i].quality_level = new_temp_qual;
    }
    current_chunk.reset();

//        if((address >= (IntPtr) approx_table[i].start_address) && (address <= (IntPtr) approx_table[i].end_address))
//            return i;
}

double
ChunkManager::get_qual(float min, float max, float current){
    return qual_array[qual_arr_size-1];
    if (current <= min)
        return qual_array[0];
    else if (current >= max)
        return qual_array[qual_arr_size-1];
    else {
        float gap = max - min;
        float map_level = (current - min)/(gap);
        int idx = map_level*qual_arr_size;
        return qual_array[idx];
    }
}
