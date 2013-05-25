#!/usr/bin/env python3

'''
Simple tool for getting timing statistics for an external execution.
Note that this depends on python3.3
'''

import argparse
import shutil
import sys
from hashlib import md5
from subprocess import Popen, DEVNULL
from time import strftime, perf_counter

def parse_arguments ():
    parser = argparse.ArgumentParser()

    parser.add_argument ( '-n', '--num',
            type = int,
            default = 5,
            help = 'Number of iterations'
            )

    parser.add_argument ( '--noout',
            action = 'store_true',
            help = 'Redirect all output to /dev/null'
            )

    parser.add_argument ( 'command',
            nargs = '+',
            help = 'Command to run'
            )

    args = parser.parse_args()
    return args

def get_hashsum ( command ):
    command_bytes = open( command, 'rb').read()
    hash_sum = md5 ( command_bytes )
    return hash_sum.hexdigest()

def run_command ( command, num, hashsum, cur_time ):
    results = []
    print ( 'Running: %s' % ' '.join ( command ) )

    if not args.noout:
        std_out = open ( '%s_%s_%s.stdout' % (command[0], hashsum, cur_time), 'a' )
        std_err = open ( '%s_%s_%s.stderr' % (command[0], hashsum, cur_time), 'a' )
    else:
        std_out = DEVNULL
        std_err = DEVNULL

    for n in range(num):
        pre_time = perf_counter()
        Popen ( command, stdout=std_out, stderr=std_err )
        post_time = perf_counter()
        results.append ( post_time - pre_time )
    return results

def main ( command, num ):

    # Verify command is on the path
    command_path = shutil.which ( command [0] )
    if not command_path:
        print ('Command %s not on PATH. Exiting' % command [0] )
        sys.exit ( 1 )

    # Get some broad information for logging the command passed
    cur_time = strftime('%Y-%m-%d_%H:%M:%S')
    hashsum = get_hashsum ( command_path )

    results = run_command ( command, num, hashsum, cur_time )

    total = sum(results)
    min_time = min(results)
    max_time = max(results)
    avg_time = total/num

    print ( 'After %d runs:' % num )
    print ( '-' * 80 )
    print ( 'Fastest run: %ss' % min_time )
    print ( 'Slowest run: %ss' % max_time )
    print ( 'Average run: %ss' % avg_time )
    print ( 'Cumulative runs: %ss' % total )
    print ( cur_time, str(hashsum) )

if __name__ == '__main__':
    args = parse_arguments()
    main ( args.command, args.num )

