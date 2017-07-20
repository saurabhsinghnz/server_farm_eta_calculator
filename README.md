A server farm consists of tens of thousands of cores that all run processes which continuously eat up heaps of disk space. This script accurately predict the ETA to the next meltdown (i.e. when the server runs out of space).

Let's assume that n processes are running on the farm. They run forever, never die, and no new processes get spawned.
Each process eats memory at a constant, individual rate - process p_i (with 0 <= i < n) consumes 1 byte after
every d(p_i) seconds. The total amount of available disk space is denoted by X.

For each given input configuration (read from stdin), the script calculates the ETA in seconds.

A configuration is encoded as a single line like this:

X d(p_1) d(p_2) ... d(p_n)

Example:
 
$ echo -e "4 3 7\n15 2 4 3 6\n16 2 4 3 6" | python eta_calculator.py
> 9
> 12
> 14