import os
from time import time
import datetime

class ProgressBar:
    """
    Simple progress bar implementation
    Constructor:
    - width: sets maximum width of the bar. If wdith is None, maximum width is the entire width of the terminal window
    """
    def __init__(self, width = None):
        if width is None:
            self.width = os.get_terminal_size().columns
        else: self.width = width

        self.counter = 0
        self.old_progress = None
    
    def __get_width(self):
        if self.width:
            return min(self.width, os.get_terminal_size().columns - 10)
        else:
            return os.get_terminal_size().columns - 10

    def __get_estimate_time(self):
        """
        Estimate time to completion using the elapsed time and the current progress
        """
        work_fraction = self.counter / self.work_length
        time_from_start = time() - self.start_time
        time_remain = (1 - work_fraction) / work_fraction * time_from_start
        return datetime.timedelta(seconds = round(time_remain))

    def __update_bar(self):
        """
        Progress bar update routine
        """
        inner_width = self.__get_width() - 10
        progress = self.counter * inner_width // self.work_length

        # avoid redrawing the bar if the progress hasn't changed
        if progress != self.old_progress: 
            self.old_progress = progress
            empty = inner_width - progress
            percentage = self.counter / self.work_length * 100

            bar = '[{}>{}] {}% | {}'.format(
                '=' * progress,
                ' ' * empty,
                round(percentage, 3),
                self.__get_estimate_time()
            )

            print(bar, end = '\r')

    def __call__(self, iterator):
        self.work_length = len(iterator)
        self.start_time = time()

        for item in iterator:
            yield item

            self.counter += 1
            self.__update_bar()

if __name__ == '__main__':
    pb = ProgressBar()
    from time import sleep

    for i in pb(range(100)):
        sleep(0.03)
