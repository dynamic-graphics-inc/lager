
import logging

# Adding the 'username' and 'funcname' specifiers
# They must be attributes of the log record

# Custom log record
class OurLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        logging.LogRecord.__init__(self, *args, **kwargs)
        self.username = current_user()
        self.funcname = calling_func_name()

# Custom logger that uses our log record
class OurLogger(logging.getLoggerClass()):
    def makeRecord(self, *args, **kwargs):
        return OurLogRecord(*args, **kwargs)

# Register our logger
logging.setLoggerClass(OurLogger)


# Current user
def current_user():
    import pwd, os
    try:
        return pwd.getpwuid(os.getuid()).pw_name
    except KeyError:
        return "(unknown)"

# Calling Function Name
def calling_func_name():
    return calling_frame().f_code.co_name

import os, sys
def calling_frame():
    f = sys._getframe()

    while True:
        if is_user_source_file(f.f_code.co_filename):
            return f
        f = f.f_back

def is_user_source_file(filename):
    return os.path.normcase(filename) not in (_srcfile, logging._srcfile)

def _current_source_file():
    if __file__[-4:].lower() in ['.pyc', '.pyo']:
        return __file__[:-4] + '.py'
    else:
        return __file__

_srcfile = os.path.normcase(_current_source_file())


logging.log(msg='herm', level=logging.INFO)
def flog(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        args_str = ", ".join([str(arg) for arg in args])
        kwargs_str = ", ".join(["%s=%s" % (key, kwargs[key]) for key in kwargs])
        if args_str and kwargs_str:
            all_args_str = ", ".join([args_str, kwargs_str])
        else:
            all_args_str = args_str or kwargs_str
        # logger.debug("%s(%s)", func.__name__, all_args_str)
        print("%s(%s)", func.__name__, all_args_str)
        return func(*args, **kwargs)

    return wrap
