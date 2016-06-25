#!/usr/bin/env python3
import argparse
import sys

THRESHOLD = 0.9
POSITIVE_CNT_LIMIT = 3

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--reference', type=str, required=True,
                    help='The reference result.txt file.')
parser.add_argument('-f', '--file', type=str, required=True,
                    help='The user result.txt file.')
args = parser.parse_args()

ref = []

with open(args.reference, 'r') as ifile:
    lines = ifile.readlines()
    true_cnt = len(lines)
    for line in lines:
        t = line.strip()
        if not t:
            continue
        t = t.split()
        if len(t) != 3:
            print("Invalid reference file.")
            raise Exception

        t.append(0)
        ref.append(t)

with open(args.file, 'r') as ifile:
    lines = ifile.readlines()
    positive_cnt = len(lines)
    for line in lines:
        t = line.strip()
        if not t:
            continue
        t = t.split()
        if len(t) != 3:
            print("Invalid user result.txt file.")
            raise Exception

        for i in ref:
            if t[0] == i[0]:
                l = max(int(t[1]), int(i[1]))
                r = min(int(t[2]), int(i[2]))
                cov = max(r-l+1, 0)
                if cov==0:
                    continue
                rdist = int(i[2])-int(i[1])+1
                fdist = int(t[2])-int(t[1])+1
                se = cov/rdist
                pr = cov/fdist
                fscore = (2*se*pr)/(pr+se)
                if fscore > THRESHOLD and fscore > i[3]:
                    i[3] = fscore

point = [x[3] for x in ref]
true_positive_cnt = len([x for x in point if x != 0])
point_sum = sum(point) / true_cnt

print("Sensitivity: {0:.6f}".format(true_positive_cnt/true_cnt))
print("Precision: {0:.6f}".format(true_positive_cnt/positive_cnt))
print("Point: {0:.6f}".format(point_sum))

if positive_cnt > true_cnt * POSITIVE_CNT_LIMIT:
    print("WARNING: Too many recalls!!!")
    print("WARNING: Too many recalls!!!")
    print("WARNING: Too many recalls!!!")
print("LastJudgement: Finished.")

#for i in ref:
#    print("{0} {1} {2} {3}".format(i[0], i[1], i[2], i[3]!=0))

