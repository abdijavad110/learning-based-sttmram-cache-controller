from matplotlib import pyplot as plt
import matplotlib


times = {}
addresses = {}
vv = list(map(lambda q: q.split(','), open("logs/var_addr.txt").read().split('\n')))
tt = list(map(lambda q: q.split(','), open("logs/exec_time.txt").read().split('\n')))
for t in tt:
    times[t[0]] = float(t[2])
for v in vv:
    addresses[v[0]] = int(v[1])

# print(matplotlib.get_backend())
matplotlib.use("TkAgg")
print(matplotlib.get_backend())
ff = open('log_L2_core-0.log', 'r')
nn = ff.read().split('\n')
nn = list(map(lambda q: q.split(','), nn))
nn = list(filter(lambda q: len(q) == 3, nn))
nn = list(map(lambda q: [float(q[0]), int(q[1]), q[2]], nn))

WW = list(filter(lambda q: q[2] == 'W' and min(addresses.values()) < q[1] < max(addresses.values())+1000000, nn))
WW_idx = list(map(lambda q: q[0], WW))
WW_add = list(map(lambda q: q[1], WW))

WB = list(filter(lambda q: q[2] == 'WB' and min(addresses.values()) < q[1] < max(addresses.values())+1000000, nn))
WB_idx = list(map(lambda q: q[0], WB))
WB_add = list(map(lambda q: q[1], WB))

cmap = plt.cm.get_cmap("Dark2", len(times))
for i, k in enumerate(times.items()):
    k, v = k
    plt.axvline(v, lw=2.0, label=k, c=cmap(i))
cmap = plt.cm.get_cmap("Dark2", len(addresses))
for i, k in enumerate(addresses.items()):
    k, v = k
    plt.axhline(v, lw=1.5, label=k, c=cmap(i))
plt.legend(fontsize=23)
plt.xlabel("time (seconds)", fontsize=23)
plt.ylabel("Addresses", fontsize=23)
WB_plot = plt.plot(WB_idx, WB_add, 'b.', label="Write Backs")
WW_plot = plt.plot(WW_idx, WW_add, 'r.', label="Writes")
plt.savefig("fig.jpg")
plt.show()
