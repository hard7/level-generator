import time


class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.name:
            print '[%s]' % self.name,
        e = (time.time() - self.start) * 1000
        print 'Elapsed: %.1f ms' % e