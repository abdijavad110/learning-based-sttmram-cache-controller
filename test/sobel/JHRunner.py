import os
import sys
import time
import json
import subprocess
from tqdm import tqdm
from time import sleep
from random import random
import multiprocessing as mp

# IMG_ID_RANGE = range(227, 230)
IMG_ID_RANGE = range(227, 256+1)
IMG_NAME = 'frames/00{}'


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


def execute(compile_cmd):
    gpp_p = subprocess.Popen(compile_cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
    out = gpp_p.stdout.read()
    errors = gpp_p.stderr.read()
    ret = gpp_p.wait()
    return ret, str(out), str(errors)


def compiler(msg, compile_cmd):
    print(" > compiling " + msg + " ...")
    r, e1, e2 = execute(compile_cmd)
    if r != 0:
        print("Error while compiling " + msg)
        print(e1)
        print(e2)
        sys.exit(0)


def run_golden(img):
    r, o, e = execute("./sobel {}.pgm {}-golden.pgm".format(img, img))
    if r != 0:
        print(" > Error while running golden for {} \n{}\n{}".format(img, o, e))


def run_sniper(img):
    r, o, e = execute("../../run-sniper -c base.cfg --cache-only -- ./sobel {}.pgm {}-out.pgm".format(img, img))
    if r != 0:
        print(" > Error while running sniper for {} \n{}\n{}".format(img, o, e))
    return o


class Logger:
    def __init__(self):
        self.dict = {}
        self.start_time = time.ctime()
        os.mkdir(self.start_time)
        self.raw_file = open("%s/raw_log.txt" % self.start_time, 'w')
        self.processed_file = open("%s/processed_log.json" % self.start_time, 'w')

    def _raw(self, *ts):
        self.raw_file.write("\n\n" + "X" * 50)
        for t in ts:
            self.raw_file.write(t + "\n")

    def _pretty(self, test, exp):
        self.dict[test] = process(test, exp)
        self.processed_file.seek(0)
        self.processed_file.write(json.dumps(self.dict))

    def log(self, name, res):
        self._raw(name, res)
        self._pretty(name, res)

    def spit_it_out(self):
        print("\n\n" + "=" * 30 + "\n")
        for k, v in self.dict.items():
            wrts = v['writes']
            print("{},{},,{},{},{},{},{},{}".format(k, v['mpd'], wrts['high current'], wrts['0.000000100'], wrts['0.000001000'], wrts['0.000010000'],wrts['0.000100000'], wrts['0.001000000']))
        print("\n" + "=" * 30 + "\n\n")


def __del__(self):
    self.raw_file.close()
    self.processed_file.close()


def extract(t, key):
    if t.count > 1:
        start = t.index(key)
        end = t.index(key, start + 1)
        return t[start + len(key):end]
    else:
        return None


def analyze_output(img):
    golden = read_pgm(open('%s-golden.pgm' % img, 'rb'))
    output = read_pgm(open('%s-out.pgm' % img, 'rb'))

    diff = [abs(golden[i] - output[i]) for i in range(min(len(golden), len(output)))]
    return sum(diff) / len(diff) / 256.0


def process(img, exp):
    wrt_id = "4dcc865dcd8a0440f3e955e66928b6a9"

    exp_wrt_raw = extract(exp, wrt_id)
    exp_wrt = {}
    for w in exp_wrt_raw.split("\n"):
        if ": " not in w:
            continue
        key, value = w.split(": ")
        exp_wrt[key] = value

    return {'writes': exp_wrt, 'mpd': analyze_output(img)}


def pool_job(img_num):
    sleep(random() * 2)
    img = IMG_NAME.format(str(img_num))
    run_golden(img)
    res_exp = run_sniper(img)
    return img, res_exp


if __name__ == "__main__":
    start_time = time.time()
    m = mp.Manager()
    lock = m.Lock()
    # pool = mp.Pool(processes=mp.cpu_count())
    pool = mp.Pool(processes=4)

    execute('make clean')
    compiler("new changes in sniper", 'make -C ../../')
    compiler("new changes in sobel", 'make sobel')

    logger = Logger()
    pbar = tqdm(IMG_ID_RANGE, colour='green', leave=False)

    try:
        multiple_results = [pool.apply_async(pool_job, (i,)) for i in IMG_ID_RANGE]

        done_cnt = 0
        while done_cnt < len(IMG_ID_RANGE):
            new_done_cnt = [res.ready() for res in multiple_results].count(True)
            if done_cnt < new_done_cnt:
                pbar.update(new_done_cnt - done_cnt)
                done_cnt = new_done_cnt
            sleep(5)

        for i, res in enumerate(multiple_results):
            r = res.get()
            logger.log(r[0], r[1])
            # logger.log(r[0] + "_" + str(i), r[1])
        logger.spit_it_out()
    except KeyboardInterrupt:
        pass
    pbar.close()
