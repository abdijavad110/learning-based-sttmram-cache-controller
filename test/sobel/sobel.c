/* sobel.c */
#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include "mypgm.h"

//#ifdef AMHM_APPROXIMATION
//#include "../../shared_lib/approximations.h"
//int reliability_level = 0;
//#endif

#include "../../include/sim_api.h"
#define ToUnsignedInt(X) *((unsigned long long*)(&X))

double ber[2] = {1e-5, 1e-4};
double temporal_arr[2][2] = {{-1, -1},
                             {-1, -1}};
double spatial_arr[2][2] = {{-1, -1},
                             {-1, -1}};

void sobel_filtering( )
/* Spatial filtering of image data */
/* Sobel filter (horizontal differentiation */
/* Input: image1[y][x] ---- Outout: image2[y][x] */
{
    /* Definition of Sobel filter in horizontal direction */
    int weight[3][3] = {{ -1,  0,  1 },
                        { -2,  0,  2 },
                        { -1,  0,  1 }};
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
                    pixel_value += weight[j + 1][i + 1] * image1[y + j][x + i];
                }
            }
            if (pixel_value < min) min = pixel_value;
            if (pixel_value > max) max = pixel_value;
        }
    }
    if ((int)(max - min) == 0) {
        printf("Nothing exists!!!\n\n");
        exit(1);
    }
    /* Initialization of image2[y][x] */
    x_size2 = x_size1;
    y_size2 = y_size1;
    for (y = 0; y < y_size2; y++) {
        for (x = 0; x < x_size2; x++) {
            image2[y][x] = 0;
        }
    }
    /* Generation of image2 after linear transformtion */
    for (y = 1; y < y_size1 - 1; y++) {
        for (x = 1; x < x_size1 - 1; x++) {
            pixel_value = 0.0;
            for (j = -1; j <= 1; j++) {
                for (i = -1; i <= 1; i++) {
                    pixel_value += weight[j + 1][i + 1] * image1[y + j][x + i];
                }
            }
            pixel_value = MAX_BRIGHTNESS * (pixel_value - min) / (max - min);
            image2[y][x] = (unsigned char)pixel_value;
        }
    }
}

int main(int argc, const char** argv)
{

//#ifdef AMHM_APPROXIMATION
    AMHM_approx((long long int) &image1[0][0], (long long int) (&image1[MAX_IMAGESIZE-1][MAX_IMAGESIZE-1]));
    AMHM_qual(ToUnsignedInt(ber[0]));
    JH_spat(spatial_arr[0][0], spatial_arr[0][1]);
    JH_temp(temporal_arr[0][0], temporal_arr[0][1]);
    AMHM_approx((long long int) &image2[0][0], (long long int) (&image2[MAX_IMAGESIZE-1][MAX_IMAGESIZE-1]));
    AMHM_qual(ToUnsignedInt(ber[1]));
    JH_spat(spatial_arr[1][0], spatial_arr[1][1]);
    JH_temp(temporal_arr[1][0], temporal_arr[1][1]);
//  m5_add_approx(  (uint32_t)&image1[0][0], (uint32_t)(&image1[MAX_IMAGESIZE-1][MAX_IMAGESIZE-1]), reliability_level);
//  m5_add_approx(  (uint32_t)&image2[0][0], (uint32_t)(&image2[MAX_IMAGESIZE-1][MAX_IMAGESIZE-1]), reliability_level);
//#endif

    load_image_data(argv[1]);   /* Input of image1 */
    sobel_filtering( );   /* Sobel filter is applied to image1 */
    save_image_data(argv[2]);   /* Output of image2 */

//#ifdef AMHM_APPROXIMATION
//    m5_remove_approx(  (uint32_t)&image1[0][0], (uint32_t)(&image1[MAX_IMAGESIZE-1][MAX_IMAGESIZE-1]), reliability_level);
//  m5_remove_approx(  (uint32_t)&image2[0][0], (uint32_t)(&image2[MAX_IMAGESIZE-1][MAX_IMAGESIZE-1]), reliability_level);
//#endif

    return 0;
}
