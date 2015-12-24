import sys
import itertools
import random
from collections import defaultdict


def all_combinations(transaction, max_comb):
    combinations = []
    if(len(transaction) < max_comb):
        max_comb = len(transaction)-1
    for i in range(1,max_comb + 1):
        combinations.extend(list(itertools.combinations(sorted(transaction), i)))
    return combinations


if __name__ == '__main__':

    # Getting input arguments - inputfile, support
    if(len(sys.argv)!=3):
        print 'Format: python <script>.py input.txt <support>'
        exit(0)

    inputfile   = open(sys.argv[1])
    support     = int(sys.argv[2])
    fraction    = 0.4;
    new_support = int(0.9*fraction*support);

    alllines = inputfile.readlines()

    iterations = 0
    while(1):
        iterations+=1
        randomsample = random.sample(alllines, int(fraction*len(alllines)))
        filtered    = []
        negative_border = []
        frequent = []

        i = 0;
        while(1):

            i+=1

            #Initialize data structures
            counts = defaultdict(int)

            for line in randomsample:
                transaction = line.strip().split(',')

                for pair in itertools.combinations(transaction, i):
                    if(i==1):
                        counts[pair]+=1
                    else:
                        pair = tuple(sorted(pair))
                        if(all(item in filtered for item in list(itertools.combinations(pair,i-1)))):
                            counts[pair]+=1

            filtered = [k for k,v in counts.items() if v >= new_support]
            frequent.extend(filtered)
            negative_border.extend(k for k,v in counts.items() if v < new_support)

            if(len(filtered) == 0):
                break

        freq_counts = defaultdict(int)
        neg_counts = defaultdict(int)

        #Reading transaction lines
        inputfile.seek(0)
        for line in inputfile.readlines():
            transaction = line.strip().split(',')
            trans_combinations = all_combinations(transaction, i)

            freq = [item for item in trans_combinations if item in frequent]
            neg = [item for item in trans_combinations if item in negative_border]

            for item in freq:
                freq_counts[item]+=1
            for item in neg:
                neg_counts[item]+=1


        freq_filtered = [k for k,v in freq_counts.items() if v >= support]
        neg_filtered = [k for k,v in neg_counts.items() if v >= support]

        if(len(neg_filtered) == 0):
            break

    print iterations
    print fraction
    sorted_freqlist = sorted(freq_filtered, lambda x,y: len(x)-len(y))

    for k, g in itertools.groupby(sorted_freqlist, lambda x: len(x)):
        print map(list,sorted(list(g)))
        print
