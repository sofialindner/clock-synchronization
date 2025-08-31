from random import randint
import time

class Clock:

    def randomize_clock(self):
        timestamp = time.time()
        time_offset = randint(-1500, 1500)
        timestamp += time_offset

        return timestamp

    def seconds_to_hours(self, timestamp):
        return time.strftime('%H:%M:%S', time.localtime(timestamp))