#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import threading


def _every(delay, stop_event: threading.Event, task, *args, **kwargs):
    next_time = time.time() + delay
    while True:

        segments = delay // 3
        wait_time_per_segment = (next_time - time.time()) // segments
        for i in range(0, segments):
            time.sleep(max(0, wait_time_per_segment))
            if stop_event.is_set():
                return

        try:
            task(*args, **kwargs)
        except Exception as e:
            # in production code you might want to have this instead of course:
            logging.error(f"Problem while executing repetitive task: {e}")

        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay + delay


def every(delay, stop_event: threading.Event, task, *args, **kwargs):
    t = threading.Thread(target=lambda: _every(delay, stop_event, task, *args, **kwargs))
    t.start()
    return t
