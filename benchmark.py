import datetime as dt
# from typing import *


class AlreadyStartedError(ValueError):
    pass


class NotStartedError(ValueError):
    pass


class StillRunningError(ValueError):
    pass


class BenchMark:
    def __init__(self, name):
        # type: (str) -> ()
        self.name = name
        self.delta = dt.timedelta()
        self.t_started = None

    def start(self):
        # type: () -> ()
        if self.t_started is not None or self.delta.total_seconds() != 0:
            raise AlreadyStartedError(self.name)
        else:
            self.t_started = dt.datetime.now()

    def stop(self):
        # type: () -> ()
        if self.t_started is None:
            raise NotStartedError(self.name)
        else:
            self.delta = dt.datetime.now() - self.t_started
            self.t_started = None

    def time(self):
        return self.delta.total_seconds()

    def result(self):
        # type: () -> str
        if self.t_started is not None:
            raise StillRunningError(self.name)
        else:
            return "%s took %f seconds" % (self.name, self.delta.total_seconds())
