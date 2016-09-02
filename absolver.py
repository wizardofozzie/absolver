import os, sys, string
import os.path as path
from bisect import bisect_left
from itertools import combinations
from collections import defaultdict
from time import time

# create anagram word dict
# see http://stackoverflow.com/questions/5485654/how-can-this-python-scrabble-word-finder-be-made-faster

INFILE, OUTFILE  = 'dictionary.txt', 'anadict.txt'

def make_anadict(infile=INFILE, outfile=OUTFILE):
    assert path.splitext(infile)[-1] and path.splitext(outfile)[-1] in (".txt"), \
           "Must use txt in/out files"
    if path.exists(outfile) and os.stat(outfile)[6] > 0:
        print("{0} exists, skipping creation.\nDelete {0} to re-create file".format(outfile))
        sys.exit()
    f = open(infile)
    d = {}
    lets = set(string.ascii_lowercase + "\n")
    for word in f:
        if len(set(word.lower()) - lets) == 0 and len(word) >= 2:
            word = word.lower().strip()
            key = "".join(sorted(word))
            if key in d:
                d[key].append(word)
            else:
                d[key] = [word]
    f.close()
    if str == bytes: # python 2
        anadict = [" ".join([key]+value) for key, value in d.iteritems()]
    else:
        anadict = list(
            (" ".join([key]+value) for key, value in d.items())
            )
    anadict.sort()
    f = open('anadict.txt', 'w')
    f.write('\n'.join(anadict))
    f.close()


def loadvars():
    make_anadict()
    f = open('anadict.txt', 'r')
    anadict = f.read().split('\n')
    f.close()
    return anadict


def findwords(rack, anadict):
    rack = ''.join(sorted(rack))
    foundwords = []
    for i in xrange(2, len(rack)+1):
        for comb in combinations(rack, i):
            ana = ''.join(comb)
            j = bisect_left(anadict, ana)
            if j == len(anadict):
                continue
            words = anadict[j].split()
            if words[0] == ana:
                foundwords.extend(words[1:])
    return foundwords


def create_turnmap(lstlst):
    """lstlst is [ [letters for 1 turn], [letters for 2 turns]... ] """
    tm = defaultdict(list)  # turnmap
    for index, lst in enumerate(lstlst, start=1):
        for letter in lst:
            if letter != ' ':
                tm[index].append(letter)
    return tm


def get_score(turnmap, match):
    """foo bar"""
    from copy import deepcopy
    score = 0
    tm = deepcopy(turnmap)

    for char in match:
        for value in tm:
            if char in tm[value]:
                # remove first character from list
                match = match[1:]
                tm[value].remove(char)

                if value == 1:
                    score += 100
                elif value == 2:
                    score += 6
                elif value == 3:
                    score += 5
                else:
                    score += 1
    return score

if __name__ == "__main__":    
    if len(sys.argv) == 2:
        rack = sys.argv[1].strip()
    else:
        print(
            """Usage: python cheat_at_scrabble.py <yourrack>"""
            )
        sys.exit()
    t = time()
    anadict = loadvars()
    print("Dictionary loading time:{}".format(time()-t))
    t = time()
    foundwords = set(findwords(rack, anadict))

    scored = [(score_word(word), word) for word in foundwords]
    scored.sort()
    for score, word in scored:
        print("%d\t%s" % (score, word))
    print("Time elapsed:", (time()-t))
