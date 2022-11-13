#! /usr/bin/env python3

"""
Sherlock: Find Usernames Across Social Networks Module

This module contains the main logic to search for usernames at social
networks.s
"""

import sys
# import os
# goal_dir = os.path.join(os.path.dirname(__file__), '../../')
# goal_dir = os.path.normpath(goal_dir)
# sys.path.insert(0, goal_dir)
from src.sherlock.sherlock.sherlock import main
from threading import Thread
from queue import Queue


class SherlockAdapter():
    def __init__(self):
        self.result_queue = Queue()
        self.sherlock_worker = None

    @staticmethod
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

    def dequeue(self):
        '''
        dequeue all the current data in result_queue
        ('end','end') indicating the end of process
        '''
        size = self.result_queue.qsize()
        data_list = []
        for _ in range(size):
            data_list.append(self.result_queue.get())
            self.result_queue.task_done()
        return data_list

    def start_sherlock(self, user_name):
        if self.sherlock_worker is not None:
            print("Error already one sherlock running")
        else:
            self.sherlock_worker = Thread(
                target=self.run_sherlock, kwargs={'result_queue': self.result_queue,
                                                'user_name': user_name})
            # start() run on different thread
            self.sherlock_worker.start()

    def get_result(self):
        # get result from sherlock worker
        data_list = self.dequeue()
        is_complete = False
        # None at last indicate finished
        if len(data_list) != 0:
            if (data_list[-1] is None):
                data_list.pop()
                self.sherlock_worker.join()
                self.sherlock_worker = None
                print("sherlock worker joined")
                is_complete = True
        return data_list, is_complete


# adapter = SherlockAdapter()
# adapter.start_sherlock('yiop')
# while True:
#     data, is_complete = adapter.get_result()
#     if is_complete:
#         break
#     if len(data) != 0:
#         print(data)
