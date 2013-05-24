performance_sandbox
===================

Simple tool for collecting rough timing information on execution of input

The use case for this is simple. You're working on some code, and you want
to make a few different changes, and compare the performance. You may also
want to compare the performance with different input or arguments. 

This tool is written with the idea that you do this frequently enough that using
_time_ on unix and noting down the results isn't sufficient. You want to
store the results with some metadata attached, for example, what arguments
you ran with, how many iterations, including the best/worst/avg of that set.

Currently it does nothing other than run your command w/ optional args, and
print out results. Eventually it will probably store results in JSON or some
other non-offensive format with little to no dependancies to read.
