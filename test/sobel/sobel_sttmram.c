/* sobel.c */
#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include "mypgm.h"
#include "cache-sim/cache_model.h"
#include "sttmram.h"

#define CONFIG_FN "params3.cfg"

CacheModel cm(

CONFIG_FN);
#define TARGET_CACHE_LEVEL 2
long long oldBlockBaseAddress;
long long newBlockBaseAddress;
bool miss;
long long blockSize;


void sobel_filtering()
/* Spatial filtering of image data */
/* Sobel filter (horizontal differentiation */
/* Input: image1[y][x] ---- Outout: image2[y][x] */
{
    /* Definition of Sobel filter in horizontal direction */
    int weight[3][3] = {{-1, 0, 1},
                        {-2, 0, 2},
                        {-1, 0, 1}};
    double pixel_value;
    double min, max;
    int x, y, i, j;  /* Loop variable */

    /* Maximum values calculation after filtering*/
    printf("Now, filtering of input image is performed\n\n");
    min = DBL_MAX;
    max = -DBL_MAX;
    for (y = 1; y < y_size1 - 1; y++) {
        for (x = 1; x < x_size1 - 1; x++) {
            pixel_value = 0.0;
            for (j = -1; j <= 1; j++) {
                for (i = -1; i <= 1; i++) {
                    /////////////// JAMID
                    cm.access((long long) &image1[y + j][x + i], false);
                    cm.getLastAccessStats(TARGET_CACHE_LEVEL, &miss, &newBlockBaseAddress, &oldBlockBaseAddress);
                    if (miss) {
                        we_miss_block((long long) &image1[0][0], MAX_IMAGESIZE * MAX_IMAGESIZE * sizeof(unsigned char),
                                      newBlockBaseAddress, oldBlockBaseAddress, blockSize, 0);
                    }
                    /////////////////////

                    pixel_value += weight[j + 1][i + 1] * image1[y + j][x + i];
                }
            }
            if (pixel_value < min) min = pixel_value;
            if (pixel_value > max) max = pixel_value;
        }
    }
    if ((int) (max - min) == 0) {
        printf("Nothing exists!!!\n\n");
        exit(1);
    }
    /* Initialization of image2[y][x] */
    x_size2 = x_size1;
    y_size2 = y_size1;
    for (y = 0; y < y_size2; y++) {
        for (x = 0; x < x_size2; x++) {
            /////////////// JAMID
            cm.access((long long) &image2[y][x], false); // FIXME: LAST ARGUMENT FALSE OR TRUE?
            cm.getLastAccessStats(TARGET_CACHE_LEVEL, &miss, &newBlockBaseAddress, &oldBlockBaseAddress);
            if (miss)
                we_miss_block((long long) &image2[0][0], MAX_IMAGESIZE * MAX_IMAGESIZE * sizeof(unsigned char),
                              newBlockBaseAddress, oldBlockBaseAddress, blockSize, 1);
            /////////////////////

            image2[y][x] = 0;
        }
    }
    /* Generation of image2 after linear transformtion */
    for (y = 1; y < y_size1 - 1; y++) {
        for (x = 1; x < x_size1 - 1; x++) {
            pixel_value = 0.0;
            for (j = -1; j <= 1; j++) {
                for (i = -1; i <= 1; i++) {
                    /////////////// JAMID
                    cm.access((long long) &image1[y + j][x + i], false);
                    cm.getLastAccessStats(TARGET_CACHE_LEVEL, &miss, &newBlockBaseAddress, &oldBlockBaseAddress);
                    if (miss)
                        we_miss_block((long long) &image1[0][0], MAX_IMAGESIZE * MAX_IMAGESIZE * sizeof(unsigned char),
                                      newBlockBaseAddress, oldBlockBaseAddress, blockSize, 0);
                    /////////////////////

                    pixel_value += weight[j + 1][i + 1] * image1[y + j][x + i];
                }
            }
            pixel_value = MAX_BRIGHTNESS * (pixel_value - min) / (max - min);

            /////////////// JAMID
            cm.access((long long) &image2[y][x], false); // FIXME: LAST ARGUMENT FALSE OR TRUE?
            cm.getLastAccessStats(TARGET_CACHE_LEVEL, &miss, &newBlockBaseAddress, &oldBlockBaseAddress);
            if (miss)
                we_miss_block((long long) &image2[0][0], MAX_IMAGESIZE * MAX_IMAGESIZE * sizeof(unsigned char),
                              newBlockBaseAddress, oldBlockBaseAddress, blockSize, 1);
            /////////////////////

//            image2[y][x] = (unsigned char) pixel_value;
            we_assign_uchar(&image2[y][x], (unsigned char) pixel_value, 1);
        }
    }
}

int main(int argc, char* argv[]) {
    int seed = atoi(argv[4]);
    we_setup(argv[3], seed, true);

    blockSize = cm.getBlockSize(TARGET_CACHE_LEVEL);
    printf(">>>>>>>>>>>> %d", blockSize);

    load_image_data(argv[1]);   /* Input of image1 */
    sobel_filtering();   /* Sobel filter is applied to image1 */
    save_image_data(argv[2]);   /* Output of image2 */

    cm.printCacheStatus(stderr);

    return 0;
}
