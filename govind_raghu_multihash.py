import sys
import itertools
from collections import defaultdict

def hashfunc1(itemset, numbuckets):
    return reduce(lambda x, y: x+ord(y), itemset, 0)%numbuckets

def hashfunc2(itemset, numbuckets):
    return reduce(lambda x, y: x+ord(y)*ord(y), itemset, 0)%numbuckets

if __name__ == '__main__':

    # Getting input arguments - inputfile, support, num of buckets
    if(len(sys.argv)!=4):
        print 'Format: python <script>.py input.txt <support> <num_buckets>'
        exit(0)

    inputfile   = open(sys.argv[1])
    support     = int(sys.argv[2])
    numbuckets  = int(sys.argv[3])

    bitmask1    = 0
    bitmask2    = 0
    filtered    = []

    i = 0;
    while(1):
        i+=1

        #Initialize data structures
        counts = defaultdict(int)
        hash_bucket1 = defaultdict(int)
        hash_bucket2 = defaultdict(int)

        #Reading transaction lines
        inputfile.seek(0)
        for line in inputfile.readlines():
            transaction = line.strip().split(',')

            for pair in itertools.combinations(transaction, i):
                if(i==1):
                    counts[pair]+=1
                else:
                    pair = tuple(sorted(pair))
                    bucket1 = hashfunc1(pair, numbuckets)
                    bucket2 = hashfunc2(pair, numbuckets)
                    if(((bitmask1 & 1 << bucket1) > 0) and ((bitmask2 & 1 << bucket2) > 0) and all(item in filtered for item in list(itertools.combinations(pair,i-1)))):
                        counts[pair]+=1

            for pair in itertools.combinations(transaction,i+1):
                pair = tuple(sorted(pair))
                bucket1 = hashfunc1(pair, numbuckets)
                bucket2 = hashfunc2(pair, numbuckets)
                hash_bucket1[bucket1]+=1
                hash_bucket2[bucket2]+=1

        filtered = [k for k,v in counts.items() if v >= support]
        if(len(filtered) == 0):
            break

        if(i==1):
            print list(reduce(lambda x,y: x+y, sorted(filtered)))
        else:
            print
            print prev_hash1
            print prev_hash2
            print map(list,sorted(filtered))
        prev_hash1 = dict(hash_bucket1)
        prev_hash2 = dict(hash_bucket2)

        #Create bitmask
        freqbuckets1 = [k for k,v in hash_bucket1.items() if v >= support]
        freqbuckets2 = [k for k,v in hash_bucket2.items() if v >= support]
        bitmask1 = 0
        bitmask2 = 0
        for bucket in freqbuckets1:
            bitmask1 = bitmask1 | 1 << bucket
        for bucket in freqbuckets2:
            bitmask2 = bitmask2 | 1 << bucket
