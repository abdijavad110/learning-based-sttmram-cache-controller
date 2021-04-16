import sys
import json

bers = ["0.001000000", "0.000100000", "0.000010000", "0.000001000", "0.000000100", "high current"]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: enter the file name")
        sys.exit()
    dic = json.loads(open(sys.argv[1]).read())
    ks = dic.keys()
    ks.sort()
    for k in ks:
        wrts = dic[k]['writes']
        if len(sys.argv) < 3:
            for b in bers:
                print wrts[b],
        else:
            print wrts['high current'],
        print
