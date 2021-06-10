import os
import sys
import time
import json
import subprocess
from tqdm import tqdm
from time import sleep
from random import random
import multiprocessing as mp

IMG_ID_RANGE = range(227, 256)
# IMG_ID_RANGE = range(227, 228)
IMG_NAME = 'frames/00{}.bmp'


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


def run_golden(a, b):
    r, o, e = execute("./motion {} {} golden".format(a, b))
    if r != 0:
        print(" > Error while running golden for {}, {} \n{}\n{}".format(a, b, o, e))
    return o


def run_sniper(a, b):
    r, o, e = execute("../../run-sniper -c base.cfg --cache-only -- ./motion {} {}".format(a, b))
    if r != 0:
        print(" > Error while running sniper for {}, {} \n{}\n{}".format(a, b, o, e))
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
        self.dict[test] = process(exp)
        self.processed_file.seek(0)
        self.processed_file.write(json.dumps(self.dict))

    def log(self, name, res):
        self._raw(name, res)
        self._pretty(name, res)

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


def process(exp):
    bbs_id = "2199e9c4bdf0ffd34f789e9551382509"
    wrt_id = "4dcc865dcd8a0440f3e955e66928b6a9"

    exp_bbs = extract(exp, bbs_id)
    exp_wrt_raw = extract(exp, wrt_id)
    exp_wrt = {}
    for w in exp_wrt_raw.split("\n"):
        if ": " not in w:
            continue
        key, value = w.split(": ")
        exp_wrt[key] = value
    return {'bbs': exp_bbs, 'writes': exp_wrt}


def pool_job(img_num):
    sleep(random() * 5)
    img_a = IMG_NAME.format(str(img_num))
    img_b = IMG_NAME.format(str(img_num + 1))
    test_name = "{} vs {}".format(img_num, img_num + 1)
    res_exp = run_sniper(img_a, img_b)
    return test_name, res_exp


if __name__ == "__main__":
    start_time = time.time()
    m = mp.Manager()
    lock = m.Lock()
    pool = mp.Pool(processes=mp.cpu_count())

    execute('make clean')
    compiler("new changes in sniper", 'make -C ../../')
    compiler("new changes in motion", 'make motion')

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

        for res in multiple_results:
            r = res.get()
            logger.log(r[0], r[1])

    except KeyboardInterrupt:
        pass
    pbar.close()
