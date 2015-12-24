import sys
import itertools
from collections import defaultdict

def hashfunc(itemset, numbuckets):
    return reduce(lambda x, y: x+ord(y), itemset, 0)%numbuckets


if __name__ == '__main__':

    # Getting input arguments - inputfile, support, num of buckets
    if(len(sys.argv)!=4):
        print 'Format: python <script>.py input.txt <support> <num_buckets>'
        exit(0)

    inputfile   = open(sys.argv[1])
    support     = int(sys.argv[2])
    numbuckets  = int(sys.argv[3])

    bitmask     = 0
    filtered    = []

    i = 0;
    while(1):

        i+=1

        #Initialize data structures
        counts = defaultdict(int)
        hash_buckets = defaultdict(int)

        #Reading transaction lines
        inputfile.seek(0)
        for line in inputfile.readlines():
            transaction = line.strip().split(',')

            for pair in itertools.combinations(transaction, i):
                if(i==1):
                    counts[pair]+=1
                else:
                    pair = tuple(sorted(pair))
                    bucket = hashfunc(pair, numbuckets)
                    if(((bitmask & 1 << bucket) > 0) and all(item in filtered for item in list(itertools.combinations(pair,i-1)))):
                        counts[pair]+=1

            for pair in itertools.combinations(transaction,i+1):
                pair = tuple(sorted(pair))
                bucket = hashfunc(pair, numbuckets)
                hash_buckets[bucket]+=1

        filtered = [k for k,v in counts.items() if v >= support]
        if(len(filtered) == 0):
            break

        if(i==1):
            print list(reduce(lambda x,y: x+y, sorted(filtered)))
        else:
            print
            print prev_hash
            print map(list,sorted(filtered))
        prev_hash = dict(hash_buckets)

        #Create bitmask
        freqbuckets = [k for k,v in hash_buckets.items() if v >= support]
        bitmask = 0
        for bucket in freqbuckets:
            bitmask = bitmask | 1 << bucket
