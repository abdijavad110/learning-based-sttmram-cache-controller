import numpy as np
from matplotlib import pyplot as plt
import sys


# extracting writes and writebacks from main log file

ff = open('log_L2_core-0.log')

ff = ff.read()
ff = ff.split("\n")
ff = ff[1:] if len(ff) > 0 else ff
ff = ff[:-1] if len(ff) > 0 else ff

w_wr_log = open('w_wr.log', 'w+')
for line in ff:
    if line[-2:] == 'WB' or line[-1:] == 'W':
        w_wr_log.write(line + '\n')

w_wr_log.close()

#plot intervals
write_intervals = []
addr_diff = []
addresses = []
time = []
w_wr = open('w_wr.log')
w_wr = w_wr.read()
w_wr = w_wr.split("\n")
w_wr = w_wr[:-1]

prev_w_time = 0
prev_addr = 0
for line in w_wr:
    splitted = line.split(',')
    write_intervals.append(float(splitted[0]) - prev_w_time)
    prev_w_time = float(splitted[0])
    addr_diff.append(int(splitted[1]) - prev_addr)
    prev_addr = int(splitted[1])
    addresses.append(int(splitted[1]))
    time.append(float(splitted[0]))


BINS = 1000

print(len(addresses))
plt.subplot(421)
#m1_hist, m1_bins = np.histogram(write_intervals, bins=BINS)
plt.plot(time, write_intervals, 'b.')
plt.ylabel('write_intervals')

plt.subplot(422)
plt.plot(time, addr_diff, 'b.')
#m2_hist, m2_bins = np.histogram(addr_diff, bins=BINS)
plt.ylabel('addr_diff')

plt.subplot(423)
plt.plot(time, addresses, 'b.')
#m3_hist, m3_bins = np.histogram(addresses, bins=BINS)
plt.ylabel('addresses(absolute)')


# print(addr_diff)


# javad



ff = open('log_L2_core-0.log')
ff = ff.read()
ff = ff.split("\n")
ff = ff[1:] if len(ff) > 0 else ff
ff = ff[:-1] if len(ff) > 0 else ff
ff = list(map(lambda f: f.split(","), ff))

mm = list(filter(lambda f: f[1] == '0', ff))
mm = list(map(lambda f: float(f[0]), mm))

hh = list(filter(lambda f: f[1] == '1', ff))
hh = list(map(lambda f: float(f[0]), hh))

tt = list(map(lambda f: float(f[0]), ff))

plt.subplot(426)
m_hist, m_bins = np.histogram(mm, bins=BINS)
plt.plot(m_bins[:-1], m_hist)
plt.title("misses count per time")


plt.subplot(425)
h_hist, h_bins = np.histogram(hh, bins=BINS)
plt.plot(h_bins[:-1], h_hist)
plt.title("hits count per time")

plt.subplot(424)
_, t_bins = np.histogram(tt, bins=BINS)
rates = [m / (m + h) * 100 if m + h != 0 else 0 for h, m in zip(h_hist, m_hist)]
plt.plot(t_bins[:-1], rates)
plt.title("miss rate per time")


plt.show()



