import sys
import json


def compute_area(coords):
    if coords[2] >= coords[0] and coords[3] >= coords[1]:
        return (coords[2] - coords[0] + 1) * (coords[3] - coords[1] + 1)
    return 0


def jaccard(raw_test, raw_gold):
    TP = 0

    bb_exp = []
    f = raw_test.split('\n')
    for l in f:
        if l != '':
            bb_exp.append(l)

    bb_golden = []
    f = raw_gold.split('\n')
    for l in f:
        if l != '':
            if bb_exp.count(l) > 0:
                TP = TP + 1
                bb_exp.remove(l)
            else:
                bb_golden.append(l)

    bb_golden1 = []
    for l in bb_golden:
        bb = l.split(' ')
        bb.pop(2)
        bb_golden1.append([int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])])

    max_jaccard = None
    for bbe in bb_exp:
        bbe = bbe.split(' ')
        bbe.pop(2)
        bbe = [int(bbe[0]), int(bbe[1]), int(bbe[2]), int(bbe[3])]
        for bbg in bb_golden1:
            inters_coord = []
            if bbe[0] > bbg[0]:
                inters_coord.append(bbe[0])
            else:
                inters_coord.append(bbg[0])
            if bbe[1] > bbg[1]:
                inters_coord.append(bbe[1])
            else:
                inters_coord.append(bbg[1])
            if bbe[2] < bbg[2]:
                inters_coord.append(bbe[2])
            else:
                inters_coord.append(bbg[2])
            if bbe[3] < bbg[3]:
                inters_coord.append(bbe[3])
            else:
                inters_coord.append(bbg[3])
            intersArea = compute_area(inters_coord)
            unionArea = compute_area(bbe) + compute_area(bbg) - intersArea
            jaccard = float(intersArea) / unionArea
            if max_jaccard is None or jaccard > max_jaccard:
                max_jaccard = jaccard
    return max_jaccard if max_jaccard else "none"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("ERROR: enter test and golden file names")
    test_dict = json.loads(open(sys.argv[1]).read())
    gold_dict = json.loads(open(sys.argv[2]).read())

    test_keys = test_dict.keys()
    test_keys.sort()
    for k in test_keys:
        test_bbs = test_dict[k]['bbs']
        try:
            gold_bbs = gold_dict[k]['bbs']
        except KeyError:
            sys.exit("ERROR: no result for {} in golden file".format(k))

        print jaccard(test_bbs, gold_bbs)

