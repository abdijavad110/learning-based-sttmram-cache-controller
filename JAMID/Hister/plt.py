from matplotlib import pyplot as plt
import matplotlib

times = {"bgImage to bgGreyImage (rgb2grey) END time": 7.000000,
         "originalImage to greyImage (rgb2grey) END time": 14.000000,
         "motion detection END time": 17.000000,
         "erosion filter END time": 72.000000,
         "blob detection END time": 128.000000}

# print(matplotlib.get_backend())
matplotlib.use("TkAgg")
print(matplotlib.get_backend())
ff = open('log_L2_core-0.log', 'r')
nn = ff.read().split('\n')
nn = list(map(lambda q: q.split(','), nn))
nn = list(filter(lambda q: len(q) == 3, nn))
nn = list(map(lambda q: [float(q[0]), int(q[1]), q[2]], nn))

WW = list(filter(lambda q: q[2] == 'W' and 47589976000000 < q[1] < 47589981000000, nn))
WW_idx = list(map(lambda q: q[0], WW))
WW_add = list(map(lambda q: q[1], WW))

WB = list(filter(lambda q: q[2] == 'WB' and 47589976000000 < q[1] < 47589981000000, nn))
WB_idx = list(map(lambda q: q[0], WB))
WB_add = list(map(lambda q: q[1], WB))

for k, v in times.items():
    plt.axvline(v, label=k)
plt.legend(fontsize='large')
WB_plot = plt.plot(WB_idx, WB_add, 'b.', label="Write Backs")
WW_plot = plt.plot(WW_idx, WW_add, 'r.', label="Writes")
plt.savefig("fig.jpg")
plt.show()

