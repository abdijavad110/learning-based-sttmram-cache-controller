from matplotlib import pyplot as plt
import matplotlib


FONT_SIZE = 20


def grouper(addr: type({}), reqs: list):
    lis = list(addr.items())
    lis.sort(key=lambda q: q[1])
    groups = [[] for i in range(len(lis))]
    lis.append(("end", lis[-1][1]+1000000))
    reqs = list(filter(lambda q: q[2] in ['W', 'WB'], reqs))
    for r in reqs:
        for b in range(len(lis) - 1):
            if lis[b][1] <= r[1] < lis[b+1][1]:
                groups[b].append(r)
                break
    for g in groups:
        print(len(g))


def parse_borders():
    tms = {}
    ads = {}
    vv = list(map(lambda q: q.split(','), open("logs/var_addr.txt").read().split('\n')))
    tt = list(map(lambda q: q.split(','), open("logs/exec_time.txt").read().split('\n')))
    for t in tt:
        tms[t[0]] = float(t[2])
    for v in vv:
        ads[v[0]] = int(v[1])
    return tms, ads


def parse_log():
    ff = open('log_L2_core-0.log', 'r')
    nn = ff.read().split('\n')
    nn = list(map(lambda q: q.split(','), nn))
    nn = list(filter(lambda q: len(q) == 3, nn))
    return list(map(lambda q: [float(q[0]), int(q[1]), q[2]], nn))


def plot(lls, tts, adds, separate_wb=True):
    matplotlib.use('TkAgg')
    # draw borders
    cmap = plt.cm.get_cmap("Dark2", len(tts))
    for i, k in enumerate(tts.items()):
        k, v = k
        plt.axvline(v, lw=2.0, label=k, c=cmap(i))
    cmap = plt.cm.get_cmap("Dark2", len(adds))
    for i, k in enumerate(adds.items()):
        k, v = k
        plt.axhline(v, lw=1.5, label=k, c=cmap(i))

    # initialization
    plt.legend(fontsize=FONT_SIZE)
    plt.xlabel("time (seconds)", fontsize=FONT_SIZE)
    plt.ylabel("Addresses", fontsize=FONT_SIZE)

    # draw plots
    if separate_wb:
        writes = list(filter(lambda q: q[2] == 'W' and min(adds.values()) < q[1] < max(adds.values())+1000000, logs))
        wrs_idx = list(map(lambda q: q[0], writes))
        wrs_add = list(map(lambda q: q[1], writes))

        write_backs = list(filter(lambda q: q[2] == 'WB' and min(adds.values()) < q[1] < max(adds.values())+1000000, logs))
        wbs_idx = list(map(lambda q: q[0], write_backs))
        wbs_add = list(map(lambda q: q[1], write_backs))

        plt.plot(wbs_idx, wbs_add, 'b.', label="Write Backs")
        plt.plot(wrs_idx, wrs_add, 'r.', label="Writes")
    else:
        logs_idx = list(map(lambda q: q[0], lls))
        logs_add = list(map(lambda q: q[1], lls))
        plt.plot(logs_idx, logs_add)
    plt.show()


if __name__ == '__main__':
    logs = parse_log()
    times, addresses = parse_borders()

    # plot(logs, times, addresses)

    grouper(addresses, logs)
