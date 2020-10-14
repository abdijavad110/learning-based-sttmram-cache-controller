//https://en.wikipedia.org/wiki/Jaccard_index

#include <iostream>
#include <string>
#include <vector>
#include <fstream>

typedef struct {
  int bl_x, bl_y, tr_x, tr_y;
} bb_t;

std::vector<bb_t> readBBFile(char* fn);
std::pair<int,int> getMaxXY(std::vector<bb_t>);
bool** newMatrix(int dim_x, int dim_y);
void deleteMatrix(bool*** m, int dim_x);
void fillMatrix(bool** m, std::vector<bb_t> bbs);
void unionMatrix(bool** a, bool** b, bool** r, int dim_x, int dim_y);
void intersectionMatrix(bool** a, bool** b, bool** r, int dim_x, int dim_y);
int countTrue(bool** m, int dim_x, int dim_y);

int main(int argc, char **argv) {
  if(argc!=3) {
    std::cout << "USAGE: " << argv[0] << " bb_1.txt bb_2.txt" << std::endl;
    std::cout << "Each txt file contain a list of bounding box descriptions in the form:" << std::endl;
    std::cout << "BOTTOM_LEFT_X BOTTOM_LEFT_Y -> TOP_RIGHT_X TOP_RIGHT_Y" << std::endl;
    return 0;
  }
  
  std::vector<bb_t> bb1, bb2;
  bool **img1, **img2, **imgu, **imgi; //we use C convention: 1st index is Y coord and 2nd is X coord
  int dim_x, dim_y;
  std::pair<int,int> dim1, dim2;
  float jaccard;

  bb1=readBBFile(argv[1]);
  bb2=readBBFile(argv[2]);
  if(bb1.size()!=0 || bb2.size()!=0){
    dim1=getMaxXY(bb1);
    dim2=getMaxXY(bb2);
    if(dim1.first>dim2.first)
      dim_x=dim1.first;
    else
      dim_x=dim2.first;
    
    if(dim1.second>dim2.second)
      dim_y=dim1.second;
    else
      dim_y=dim2.second;
    dim_x++; //since bb edges are included we need to add +1 rows and cols
    dim_y++;
    img1 = newMatrix(dim_x, dim_y);
    img2 = newMatrix(dim_x, dim_y);
    imgu = newMatrix(dim_x, dim_y);
    imgi = newMatrix(dim_x, dim_y);
    fillMatrix(img1, bb1);
    fillMatrix(img2, bb2);
    unionMatrix(img1, img2, imgu, dim_x, dim_y);
    intersectionMatrix(img1, img2, imgi, dim_x, dim_y);
    jaccard = (float) countTrue(imgi, dim_x, dim_y)/countTrue(imgu, dim_x, dim_y);
    std::cout << "JACCARD: " << jaccard << std::endl;   

    deleteMatrix(&img1, dim_y);
    deleteMatrix(&img2, dim_y);
    deleteMatrix(&imgu, dim_y);
    deleteMatrix(&imgi, dim_y);
  } else {
    std::cout << "JACCARD: 1" << std::endl;
  }
  return 0;
 
}

bool** newMatrix(int dim_x, int dim_y){
  int i, j;
  bool** m = new bool*[dim_y];
  for(i=0; i<dim_y; i++){
    m[i] = new bool[dim_x];
    for(j=0; j<dim_x; j++)
      m[i][j]=false;
  }
  return m;
}

void deleteMatrix(bool*** m, int dim_y){
  int i;
  for(i=0; i<dim_y; i++)  
    delete [] (*m)[i];
  delete [] *m;
  *m = NULL;
}

std::vector<bb_t> readBBFile(char* fn){
  std::vector<bb_t> res;
  bb_t bb;
  int swap;
  std::string arrow;
  std::ifstream f(fn);
  if (f.is_open()){
    f >> bb.bl_x >> bb.bl_y >> arrow >> bb.tr_x >> bb.tr_y;
    while(! f.eof()){
      if(bb.bl_y > bb.tr_y || bb.bl_x > bb.tr_x){
        std::cout << "Malformed bb: " << bb.bl_y << " " << bb.bl_x 
                  << " ->  " << bb.tr_y << " " << bb.tr_x << " " << std::endl;
        f.close();
        exit(0);
      }
      res.push_back(bb);
      f >> bb.bl_x >> bb.bl_y >> arrow >> bb.tr_x >> bb.tr_y;
    }
    f.close();
  } else {
    std::cout << "Error while opening file: " << fn << std::endl;
    exit(1);
  }
  return res;
}

std::pair<int,int> getMaxXY(std::vector<bb_t> bbs) {
  int x=0, y=0;
  int i;
  for(i=0; i<bbs.size(); i++){
    if(bbs[i].tr_x>x)
      x=bbs[i].tr_x;
    if(bbs[i].tr_y>y)
      y=bbs[i].tr_y;
  }
  return std::pair<int,int>(x,y);
}

void fillMatrix(bool** m, std::vector<bb_t> bbs) {
  int x, y, i;
  for(i=0; i<bbs.size(); i++){
    for(x=bbs[i].bl_x; x<=bbs[i].tr_x; x++)
      for(y=bbs[i].bl_y; y<=bbs[i].tr_y; y++)
        m[y][x]=true;
  }
}

void unionMatrix(bool** a, bool** b, bool** r, int dim_x, int dim_y){
  int i, j;
  for(i=0; i<dim_y; i++)
    for(j=0; j<dim_x; j++)
      r[i][j]=a[i][j] || b[i][j];  
}


void intersectionMatrix(bool** a, bool** b, bool** r, int dim_x, int dim_y){
  int i, j;
  for(i=0; i<dim_y; i++)
    for(j=0; j<dim_x; j++)
      r[i][j]=a[i][j] && b[i][j];  
}

int countTrue(bool** m, int dim_x, int dim_y){
  int i, j, c;
  for(i=0, c=0; i<dim_y; i++)
    for(j=0; j<dim_x; j++)
      if(m[i][j])  
        c++;
  return c;  
}

