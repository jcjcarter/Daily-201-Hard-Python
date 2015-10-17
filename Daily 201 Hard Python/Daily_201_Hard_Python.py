#!/usr/bin/env python3

from itertools import product
import sys
import numpy as np

def to_bin_digit(e):
    if e[0] == '!': return '1'
    else: return '0'

N, *events = input().split()
N = int(N)
E = len(events)

matrices = {}

for _ in range(N):
    row = [0 for _ in range(2 ** E)]
    not_row = [0 for _ in range(2 ** E)]
    es = list(map(lambda s: s.replace(':', ''), list(filter(lambda s: s != '&', input().split()))))
    d = {}

    for e in es[:-1]:
        idx = events.index(e.replace('!', ''))
        d[idx] = to_bin_digit(e)

    for s in [''.join(i) for i in product('01', repeat=E)]:
        match = True
        for k,v in d.items():
            if s[k] != v:
                match = False
                break
        if not match:
            not_row[int(s,2)] = 1
        else:
            row[int(s,2)] = 1

    matrices[tuple(row)] = float(es[-1])
    matrices[tuple(not_row)] = 1 - float(es[-1])

matrices[tuple([1 for _ in range(2 ** E)])] = 1.0

coef_mat = np.array(list(matrices.keys())[:2**E])
val_mat = np.array(list(matrices.values())[:2**E])

es = list(filter(lambda c: c != '&', input().split()))
d = {}

for e in es:
    idx = events.index(e.replace('!', ''))
    d[idx] = to_bin_digit(e)

try:
    probabilities = np.linalg.solve(coef_mat, val_mat)
except Exception:
    print('Not enough information.')
    sys.exit()

p = 0.0

for s in [''.join(i) for i in product('01', repeat=E)]:
    match = True
    for k,v in d.items():
        if s[k] != v:
            match = False
            break
    if not match:
        continue
    else:
        p += probabilities[int(s,2)]

print(p)