#!/usr/bin/env python3

import argparse
from hashlib import md5
from subprocess import Popen
from time import strftime, time

def parse_arguments ():
    parser = argparse.ArgumentParser()

    parser.add_argument ( '-n', '--num',
            type = int,
            default = 5,
            help = 'Number of iterations'
            )

    parser.add_argument ( 'command',
            type = str,
            help = 'Command to run'
            )

    parser.add_argument ( '-a', '--arguments',
            help = 'Arguments to pass'
            )

    args = parser.parse_args()
    return args

def get_hashsum ( command ):
    command_bytes = open(command, 'rb').read()
    hash_sum = md5 ( command_bytes )
    return hash_sum

def run_command ( command, args, num ):
    results = []
    long_command = [ command ]
    if args:
        long_command.extend ( args.split(' ') )
    print ( 'Running: %s' % ' '.join ( long_command ) )
    # TODO - Possibly redirect stdX
    for n in range(num):
        pre_time = time()
        Popen ( long_command )
        post_time = time()
        results.append ( post_time - pre_time )
    return results

def main ( command, args, num ):

    # Get some broad information for logging the command passed
    cur_time = strftime('%Y-%m-%d_%H:%M:%S')
    hashsum = get_hashsum ( command )

    results = run_command ( command, args, num )

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
    print ( cur_time, str(hashsum.hexdigest()) )

if __name__ == '__main__':
    args = parse_arguments()
    main ( args.command, args.arguments, args.num )

