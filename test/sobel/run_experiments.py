import subprocess
import sys
from multiprocessing import Pool
import os
import math
import time

## MPD == Min Pixel Difference
MPD_THR = 0.0001
PRECISION_THR = .90
RECALL_THR = .95

STEPS = 2
QL_MAX = 8

# IMG_ID_RANGE = [229, 235]
IMG_ID_RANGE = [252, 256+1]
# IMG_ID_RANGE = [227, 256+1]
IMG_NAME = 'frames/00XXX.pgm'
# NUM_INJ_PER_TEST = 10
NUM_INJ_PER_TEST = 1

SEED = 0

SOBEL_CMD='./sobel'
SOBEL_STTMRAM_CMD='./sobel_sttmram'


def read_pgm(pgmf):
  assert pgmf.readline() == 'P5\n'
  WH = pgmf.readline().split()
  if WH[0] == b'#':
    WH = pgmf.readline().split()
  (width, height) = [int(i) for i in WH]
  depth = int(pgmf.readline())
  assert depth <= 255

  raster = []
  for y in range(height):
    # row = []
    for y in range(width):
      raster.append(ord(pgmf.read(1)))
      # row.append(ord(pgmf.read(1)))
    # raster.append(ord(pgmf.read(1)))
  return raster

def analyze_output(output_id):
  golden = read_pgm(open('outs/golden_out.pgm', 'rb'))
  output = read_pgm(open('%d.pgm' % output_id, 'rb'))

  diff = [abs(golden[i] - output[i]) for i in range(len(golden))]
  return sum(diff) / len(diff) / 256.0


if __name__ == "__main__":
  start_time = time.time()

  #compile 'motion_sttmram.c',
  compile_cmd = ['g++', 'sobel_sttmram.c', 'cache-sim/cache.cpp', 'cache-sim/cache_model.cpp', 'cache-sim/fifo.cpp', 'cache-sim/lfu.cpp', 'cache-sim/lru.cpp',
      'cache-sim/nru.cpp', 'cache-sim/plru.cpp', 'cache-sim/srrip.cpp', '-O3', '-std=c++11',  '-lm', '-o', SOBEL_STTMRAM_CMD]
  gpp_p = subprocess.Popen(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
  errors = gpp_p.stdout.read()
  errors2 = gpp_p.stderr.read()
  ret= gpp_p.wait()
  if ret!=0:
    print "Error while compiling " + SOBEL_STTMRAM_CMD
    print errors
    print errors2
    sys.exit(0)
  gpp_p = subprocess.Popen(['g++', 'sobel.c', '-O3', '-no-pie', '-std=c++11', '-lm', '-o', SOBEL_CMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
  errors = gpp_p.stdout.read()
  errors2 = gpp_p.stderr.read()
  ret= gpp_p.wait()
  if ret!=0:
    print "Error while compiling " + SOBEL_CMD
    print errors
    print errors2
    sys.exit(0)

  #execute
  log_file=open('results.txt','w')

  curr_config = []
  for j in range(0,STEPS):
    curr_config.append(0)
  done=False
  curr_step=STEPS-1

  print "CONFIG PRECISION RECALL\n\n"

  while not done:
    curr_conf_str = ''
    for j in curr_config:
      curr_conf_str = curr_conf_str + str(j) + '-'
    curr_conf_str = curr_conf_str[:-1]

    #run exps
    TP = 0
    FN = 0
    FP = 0
    mpds = []
    for img_id in range(IMG_ID_RANGE[0], IMG_ID_RANGE[1]):
      curr_sobel_cmd = [SOBEL_CMD, IMG_NAME.replace("XXX", str(img_id)), 'golden_out.pgm']
      #print curr_motion_cmd
      #run golden run
      sobel_p = subprocess.Popen(curr_sobel_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
      out1 = sobel_p.stdout.read()
      ret = sobel_p.wait()
      if ret!=0:
        print "Nominal execution terminated with a reported problem"
        print curr_sobel_cmd
        sys.exit(0)
      del sobel_p

      curr_sobel_cmd[0]=SOBEL_STTMRAM_CMD
      curr_sobel_cmd.append(curr_conf_str)
      curr_sobel_cmd.append(str(SEED))
      curr_sobel_cmd[2] = 'output.pgm'
      # print(curr_sobel_cmd)
      exec_time = str(time.time() - start_time)
      exec_time = exec_time[:exec_time.index('.')]

      def inject(exec_id):
        curr_sobel_cmd[2] = '%s.pgm' % exec_id
        sobel_p = subprocess.Popen(curr_sobel_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out2 = sobel_p.stdout.read()
        ret = sobel_p.wait()
        if ret!=0:
          if ret==-11: #there was a segfault
            out2=''
          else:
            print "STTMRAM execution terminated with a reported problem"
            print curr_sobel_cmd
            print "stderr:" + sobel_p.stderr.read()
            sys.exit(0)
        del sobel_p

        mpd = analyze_output(exec_id)
        return mpd

      results = [inject(i) for i in range(NUM_INJ_PER_TEST)]
      # pool = Pool(4)
      # results = pool.map(inject, range(NUM_INJ_PER_TEST))
      avg_mpd = sum(results) / len(results)
      print "> %s\t config: %s\t image: %d\t mpd: %f" % (exec_time, curr_conf_str, img_id, avg_mpd)
      mpds.append(avg_mpd)
      # del pool


      # for exp in range(0, NUM_INJ_PER_TEST):
      #   # print "config: %s, image: %d, experiment: %d          " % (curr_conf_str, img_id, exp), "\r",
      #   #print exp
      #   sobel_p = subprocess.Popen(curr_sobel_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
      #   out2 = sobel_p.stdout.read()
      #   ret = sobel_p.wait()
      #   if ret!=0:
      #     if ret==-11: #there was a segfault
      #       out2=''
      #     else:
      #       print "STTMRAM execution terminated with a reported problem"
      #       print curr_sobel_cmd
      #       print "stderr:" + sobel_p.stderr.read()
      #       sys.exit(0)
      #   del sobel_p
      #
      #   #compute MPD
      #   mpd = analyze_output()
      #   mpds.append(mpd)
      #   # TP = TP + stats[0]
      #   # FP = FP + stats[1]
      #   # FN = FN + stats[2]
      #   log_file.write(str(curr_conf_str) + " " + str(img_id) + " " + str(SEED) + " " + str(mpd) + '\n')
      #
      #   SEED=SEED+1
      #   curr_sobel_cmd[4]=str(SEED)

    #compute precision and recall FIXME FIXME FIXME FIXME FIXME FIXME
    # precision = float(TP) / (TP+FP)
    # recall = float(TP) / (TP+FN)
    # print str(curr_conf_str) + " " + str(precision) + " " + str(recall)

    #accept or discard move and consequently select next configuration
    #the steps are scanned from the last one to the first one and we try to maximize the QL
    #if not possible or there is no higher QL level we move to the next step
    mpd = sum(mpds) / len(mpds)
    if mpd <= MPD_THR: #if the move is accepted and we are at the max QL move to next step
      if curr_config[curr_step] == QL_MAX:
        curr_step = curr_step - 1
    else: #if the move is discarded, restore previous QL level and move to the next step
      curr_config[curr_step] = curr_config[curr_step] - 1
      curr_step = curr_step - 1
    if curr_step >=0: #if the current step is valid improve the QL otherwise we have finished
      curr_config[curr_step] = curr_config[curr_step] + 1
    else:
      done = True

  curr_conf_str = ''
  for j in curr_config:
    curr_conf_str = curr_conf_str + str(j) + '-'
  curr_conf_str = curr_conf_str[:-1]
  end_time = time.time()

  print "\nFINAL CONFIG: " + curr_conf_str

  exe_sec = int(end_time-start_time)
  exe_min = exe_sec / 60
  exe_sec = exe_sec % 60

  print "Execution time: " + str(exe_min) + "m " + str(exe_sec) + "s"
  log_file.close()
