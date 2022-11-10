#! /usr/bin/env python3

"""
Sherlock: Find Usernames Across Social Networks Module

This module contains the main logic to search for usernames at social
networks.
"""

import sys
import os.path
goal_dir = os.path.join(os.path.dirname(__file__), '../../src/sherlock/sherlock/')
goal_dir = os.path.normpath(goal_dir)
sys.path.append(goal_dir)
from src.sherlock.sherlock.sherlock import main


def dequeue(result_queue):
    '''
    dequeue all the current data in result_queue
    ('end','end') indicating the end of process
    '''
    size = result_queue.qsize()
    data_list = []
    for _ in range(size):
        data_list.append(result_queue.get())
        result_queue.task_done()
    return data_list


def run_sherlock(result_queue, user_name):
    '''
    run sherlock on user name, using local website data set and also show nsfw site
    '''
    sys.argv = [sys.argv[0]]
    sys.argv.append("--local")
    sys.argv.append("--nsfw")
    # sys.argv.append("--no-color")
    sys.argv.append(user_name)
    main(result_queue)



