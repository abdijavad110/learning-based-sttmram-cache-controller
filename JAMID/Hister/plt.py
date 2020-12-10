import os
import matplotlib
import json as js
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

FONT_SIZE = 5 if os.name == 'nt' else 10
TITLE_SIZE = 5 if os.name == 'nt' else 20
CMAP = 'coolwarm'
THRESHOLD = 10 ** -10


def grouper(time: type({}), addr: type({}), reqs: list):
    lis = list(addr.items())
    times = list(time.items())
    lis.sort(key=lambda q: q[1])
    times.sort(key=lambda q: q[1])
    # print(lis)
    # print(times)
    write_per_addr = [[] for i in range(len(lis))]
    write_per_time = [[] for i in range(len(times))]
    lis.append(("end", lis[-1][1] + 750000))
    times.append(("output", reqs[-1][0]))
    # print(times)
    # print(lis)
    reqs = list(filter(lambda q: q[2] in ['W', 'WB'], reqs))
    time_periods = []
    addr_periods = []
    for r in reqs:
        for b in range(len(lis) - 1):

            if lis[b][1] <= r[1] < lis[b + 1][1]:
                write_per_addr[b].append(r)
                break
        for d in range(len(times) - 1):

            if times[d][1] <= r[0] <= times[d + 1][1]:
                write_per_time[d].append(r)
                break

    for b in range(len(lis) - 1):
        addr_periods.append(lis[b + 1][1] - lis[b][1])

    for d in range(len(times) - 1):
        time_periods.append(times[d + 1][1] - times[d][1])

    print(addr_periods)
    print(time_periods)
    tmp = 0
    time_count = []
    addr_count = []
    time_density = []
    addr_density = []
    time_addr_count = [[0 for j in range(len(write_per_time))] for i in range(len(write_per_addr))]
    # for i in range(len(write_per_time)):
    #     for j in range(len(write_per_time[i])):
    #         if times[i][1] <= write_per_time[i][j][0] <= times[i+1][1]:
    #             counter += 1
    print('addr')
    t = 0
    for a in write_per_addr:
        tmp += len(a)
        addr_count.append(len(a))
    print('sum: ' + str(tmp))
    tmp = 0
    print('times')
    for t in write_per_time:
        tmp += len(t)
        time_count.append(len(t))
        # print(len(t))
    print('sum: ' + str(tmp))
    # print(len(write_per_addr))
    # todo A huge toff, will fix it later
    for r in reqs:
        for j in range(len(lis) - 1):
            for k in range(len(times) - 1):
                if lis[j][1] <= r[1] <= lis[j + 1][1] and times[k][1] <= r[0] <= times[k + 1][1]:
                    time_addr_count[j][k] += 1

    for i in range(len(time_count)):
        time_density.append(time_count[i] / time_periods[i])
    for j in range(len(addr_count)):
        addr_density.append(addr_count[j] / addr_periods[j])
        for k in range(len(time_count)):
            time_addr_count[j][k] = time_addr_count[j][k] / time_periods[k]
    print(time_addr_count[6][3])

    addr_max = max(addr_density)
    time_max = max(time_density)
    for i in range(len(time_density)):
        time_density[i] = time_density[i] / time_max
    for j in range(len(addr_density)):
        addr_density[j] = addr_density[j] / addr_max

    print(time_density)
    print(addr_density)


def parse_borders():
    tms = {}
    tt = list(map(lambda q: q.split(','), open("logs/exec_time.txt").read().split('\n')))
    for t in tt:
        tms[t[0]] = float(t[2])
    ads = {}
    vv = list(map(lambda q: q.split(','), open("logs/var_addr.txt").read().split('\n')))
    for v in vv:
        ads[v[0]] = int(v[1])
    return tms, ads


def parse_log():
    ff = open('log_L2_core-0.log', 'r')
    nn = ff.read().split('\n')
    nn = list(map(lambda q: q.split(','), nn))
    nn = list(filter(lambda q: len(q) == 3, nn))
    return list(map(lambda q: [float(q[0]), int(q[1]), q[2]], nn))


def plot_borders(tts=None, adds=None, labels=True):
    if tts:
        cmap = plt.cm.get_cmap("Dark2", len(tts))
        for i, k in enumerate(tts.items()):
            k, v = k
            plt.axvline(v, lw=2.0, label=k if labels else None, c=cmap(i))
    if adds:
        cmap = plt.cm.get_cmap("Dark2", len(adds))
        for i, k in enumerate(adds.items()):
            k, v = k
            plt.axhline(v, lw=1.5, label=k if labels else None, c=cmap(i))


def plot(lls, tts, adds, separate_wb=False, heat_w_h=None, silent_mode=False):
    res = None
    matplotlib.use('TkAgg')

    # initialization
    lls = list(filter(lambda q: min(adds.values()) < q[1] < max(adds.values()) + 725000, lls))
    x_data = list(map(lambda q: q[0], lls))
    y_data = list(map(lambda q: q[1], lls))

    if not silent_mode:
        plt.subplot(1, 1, 1) if heat_w_h is None else plt.subplot(2, 2, 1)
        plot_borders(tts, adds)
        plt.legend(fontsize=FONT_SIZE)
        plt.xlabel("time (seconds)", fontsize=FONT_SIZE)
        plt.ylabel("Addresses", fontsize=FONT_SIZE)

        # draw plots
        if separate_wb:
            writes = list(filter(lambda q: q[2] == 'W', lls))
            wrs_idx = list(map(lambda q: q[0], writes))
            wrs_add = list(map(lambda q: q[1], writes))

            write_backs = list(filter(lambda q: q[2] == 'WB', lls))
            wbs_idx = list(map(lambda q: q[0], write_backs))
            wbs_add = list(map(lambda q: q[1], write_backs))

            if not silent_mode:
                plt.plot(wbs_idx, wbs_add, 'b.', label="Write Backs")
                plt.plot(wrs_idx, wrs_add, 'r.', label="Writes")
        else:
            plt.plot(x_data, y_data, '.')

    if heat_w_h:
        res = plot_heat(x_data, y_data, heat_w_h, adds, silent_mode)
    if not silent_mode:
        plt.show()
    return res


def plot_heat(x_data, y_data, heat_w_h, adds, silent_mode):
    try:
        wdt, hgt = heat_w_h
        x_min, x_max = min(x_data), max(x_data)
        y_min, y_max = min(y_data), max(y_data)
        wdt_bin = int((x_max - x_min) / wdt) + 1
        hgt_bin = int((y_max - y_min) / hgt) + 1
        for k, v in adds.items():
            adds[k] = round((y_max - v) / hgt)
        adds['start'] = 0

    except Exception as e:
        if type(e) == TypeError:
            print('\033[91m' + "ERROR: heat_w_h should be in the form (width, height). can't draw the plot.")
        else:
            print(e)
        return
    buckets = [[[] for _ in range(hgt_bin)] for _ in range(wdt_bin)]
    temp_dens = np.zeros((hgt_bin, wdt_bin), dtype='float')
    spat_dens = np.zeros((hgt_bin, wdt_bin), dtype='float')
    wrt_cnts = np.zeros((hgt_bin, wdt_bin), dtype='float')
    for x, y in zip(x_data, y_data):
        i = int((x - x_min) / wdt)
        j = int((y - y_min) / hgt)
        buckets[i][j].append((x, y))
    for i, row in enumerate(buckets):
        for j, cell in enumerate(row):
            write_count = len(cell)
            if write_count > 1:
                time_range = max(cell, key=lambda q: q[0])[0] - min(cell, key=lambda q: q[0])[0]
                addr_range = max(cell, key=lambda q: q[1])[1] - min(cell, key=lambda q: q[1])[1]
                temp_dens[hgt_bin - j - 1, i] = write_count / time_range if time_range != 0 else np.inf
                spat_dens[hgt_bin - j - 1, i] = write_count / addr_range if addr_range != 0 else 0
            else:
                spat_dens[hgt_bin - j - 1, i] = 0
                temp_dens[hgt_bin - j - 1, i] = 0
            wrt_cnts[hgt_bin - j - 1, i] = write_count
    hgt, y_min, y_max = list(map(lambda q: q // 10 ** 4, [hgt, y_min, y_max]))

    def draw(data):
        sns.heatmap(data / np.max(data, axis=(0, 1), keepdims=True), cmap=CMAP, robust=False,
                    cbar=False,
                    # yticklabels=range(y_min, y_max, hgt), xticklabels=range(int(x_min), int(x_max), wdt),
                    )
        #           annot=True, fmt='.1f')
    if not silent_mode:
        plt.subplot(2, 2, 2)
        plt.title("writes per chunk", fontsize=TITLE_SIZE)
        draw(wrt_cnts)
        plt.subplot(2, 2, 3)
        plt.title("temporal density", fontsize=TITLE_SIZE)
        draw(temp_dens)
        plt.subplot(2, 2, 4)
        plt.title("spatial density", fontsize=TITLE_SIZE)
        draw(spat_dens)

    return stat(adds, spat_dens, temp_dens)


class Arr(object):
    def __init__(self, arr):
        self.data = arr
        nonzero = arr[arr >= THRESHOLD]
        self.usage = len(nonzero) / len(arr)
        self.min = np.min(nonzero)
        self.max = np.max(nonzero)
        self.avg = np.mean(nonzero)

    def __str__(self):
        return '{"usage": %f, "min": %f, "avg": %f, "max": %f}' % (self.usage, self.min, self.avg, self.max)


class StatElem(object):
    def __init__(self, temp, spat):
        self.temp = Arr(temp)
        self.spat = Arr(spat)

    def __str__(self):
        return '{\n\t\t"temporal": %s,\n\t\t "spatial": %s\n\t}' % (str(self.temp), str(self.spat))


def stat(adds, spat, temp):
    pk, pv = list(adds.items())[0]
    for k, v in adds.items():
        if k == pk:
            continue
        adds[pk] = StatElem(temp[:, v:pv], spat[:, v:pv])
        pk, pv = k, v
    del adds['start']
    return adds


def rec_str(a):
    s = '{'
    for i, k in enumerate(a.items()):
        k, v = k
        s += '\n\t"%s": %s' % (k, v)
        if i != len(a) - 1:
            s += ','
    s += '\n}'
    return s


if __name__ == '__main__':
    logs = parse_log()
    times, addresses = parse_borders()

    res = plot(logs, times, addresses, heat_w_h=(0.5, 50000), silent_mode=True)

    f = open('stat.json', 'w')
    f.write(rec_str(res))
    f.close()
