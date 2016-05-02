#!/usr/bin/python3

''' SI 335 Spring 2015
    Project 1
    
    This program reads jobs from jobs.txt and names from names.txt,
    then uses the values of n and k given on the command line to
    generate random input for the program. This generated input file
    is written to standard out.
'''

from sys import argv, exit
from random import shuffle, sample

def usage():
    print("Usage: {} n k".format(argv[0]))
    print("jobs.txt and names.txt must exist in current directory.")
    exit(1)

if len(argv) != 3:
    usage()

n, k = map(int, argv[1:])

if n < 0 or k < 0:
    usage()

with open('names.txt') as namesfile:
    names = [line.strip() for line in namesfile]

with open('jobs.txt') as jobsfile:
    jobs = [line.strip() for line in jobsfile]

if n > len(names):
    print("ERROR: not enough names in names.txt")
    exit(2)

if k > len(jobs):
    print("ERROR: not enough jobs in jobs.txt")
    exit(2)

rankings = [list(range(1,n+1)) for i in range(k)]
for ranks in rankings:
    shuffle(ranks)

print(k)
for job in sample(jobs, k):
    print(job)

print(n)
for nameAndRanks in zip(sample(names, n), *rankings):
    print(*nameAndRanks)


