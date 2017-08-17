"""
Brief: Give total memory and list of process durations to consume
       1 byte each, this program finds the total time it would take
       to exhaust all memory.

Params:  ./eta_calculator.py <total_memory> <P1 time> <P2 time> ... <P-n time>

Example: ./eta_calculator.py 16 4 3 2

Author: Saurabh Singh
"""


# ---------------------------------------------------------------
# System Imports
# ---------------------------------------------------------------
import doctest
import logging
from sys import stdin


# ---------------------------------------------------------------
# Set Logging
# ---------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('eta_calculator')


# ---------------------------------------------------------------
# Developer Notes:
#
# Finding the time to exhaustion can take hours to complete
# specially if the memory size is huge.
# This algorithm fuzzy finds the closest time to exhaustion and
# then starts linear scan from there on to find the exact time
# to exhaustion.
#
# Also the algorithm sorts the process list early on so as to avoid
# unnecessary calculations as can be seen later on in
# get_bytes_used() function.
#
# This algorithms is huge improvement from the early prototypes
# which were O(n^2) in time complexity.
# While this algorithm is not exactly O(n log n), it is pretty
# close to that given we binary search the closest time
# for most of the algorithm.
# ---------------------------------------------------------------
def calculate_eta(user_input):
    """
    Given total memory and process times to exhaust 1 byte each
    Find the total time to exhaust all memory.

    >>> calculate_eta([4, 3 ,7])
    9
    >>> calculate_eta([15, 2, 4, 3, 6])
    12
    >>> calculate_eta([16, 2, 4, 3, 6])
    14

    :type user_input: list
    :param user_input: List containing user input numbers

    :return: time in seconds
    :rtype: int
    """
    # Extract total memory and process durations from user input
    total_memory = user_input[0]
    process_durations = user_input[1:]
    log.debug("Total Memory => {}B".format(total_memory))
    log.debug("Process Durations => {}".format(process_durations))

    # Check boundary condition. Returning early.
    if not total_memory:
        return 0

    # Sort process durations
    process_durations.sort()

    # Get bytes used at max process duration
    max_process_duration = process_durations[-1]
    bytes_used = get_bytes_used(max_process_duration, process_durations)
    log.debug("Bytes Used at MAX process duration = {}B".format(bytes_used))

    if bytes_used == total_memory:
        time_taken = max_process_duration
        return time_taken

    elif bytes_used > total_memory:
        # Start time from min process time
        time_taken = process_durations[0]

    else:
        log.debug("Fuzzy finding closest multiplier")
        # Fuzzy find the closest multiplier that takes us
        # close to memory exhaustion
        min_multiplier = 1
        max_multiplier = total_memory // bytes_used
        closest_multiplier = min_multiplier

        # Binary search the closest multiplier
        while min_multiplier < max_multiplier:
            multiplier = (min_multiplier + max_multiplier) // 2
            time_taken = max_process_duration * multiplier
            bytes_used = get_bytes_used(time_taken, process_durations)

            if bytes_used > total_memory:
                max_multiplier = multiplier - 1
            else:
                closest_multiplier = multiplier
                min_multiplier = multiplier + 1

        log.debug("Closest multiplier is {}".format(closest_multiplier))

        log.debug("Fuzzy finding closest time")
        # Fuzzy find the closest time that takes us
        # close to memory exhaustion
        min_time_taken = max_process_duration * closest_multiplier
        max_time_taken = max_process_duration * (closest_multiplier + 1)
        closest_time = min_time_taken

        # Binary search the closest time to exhaustion
        while min_time_taken < max_time_taken:
            time_taken = (min_time_taken + max_time_taken) // 2
            bytes_used = get_bytes_used(time_taken, process_durations)

            if bytes_used > total_memory:
                max_time_taken = time_taken - 1
            else:
                closest_time = min_time_taken
                min_time_taken = time_taken + 1

        time_taken = closest_time

    log.debug("Closest time is {}".format(time_taken))

    # Now that we have the closest time to exhaustion
    # linear scan the exact time to exhaustion
    bytes_used = get_bytes_used(time_taken, process_durations)

    log.debug("Starting linear scan from {}s".format(time_taken))

    while bytes_used < total_memory:
        bytes_used = get_bytes_used(time_taken, process_durations)
        time_taken += 1

    return time_taken - 1


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------
def get_bytes_used(current_time, process_durations):
    """
    Return bytes used at given time.

    >>> get_bytes_used(12, [2, 3, 4])
    13
    >>> get_bytes_used(14, [2, 3, 4])
    14

    :type current_time: int
    :param current_time: Array index

    :type process_durations: list
    :param process_durations: List containing process durations to exhaust 1 byte.

    :return: bytes_used
    :rtype: int
    """
    bytes_used = 0
    for p_time in process_durations:
        if p_time > current_time:
            # Since the array is sorted we can break early
            # and avoid unnecessary calculations.
            break
        bytes_used += current_time // p_time

    return bytes_used


def get_user_input():
    """
    Get user input

    :return: list of numbers
    :rtype: list[int]
    """
    input_list = list()
    for line in stdin:
        input_line = line.split(' ')
        input_list.append([int(item) for item in input_line])
    return input_list
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
def main():
    """
    Main function. Gets user input and calculates ETA to
    memory exhaustion.
    """
    input_list = get_user_input()

    for user_input in input_list:
        time_taken = calculate_eta(user_input)

        m, s = divmod(time_taken, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        log.info("{}s OR {}days {}h {}m {}s".format(time_taken, d, h, m, s))


if __name__ == '__main__':
    doctest.testmod()

    main()
