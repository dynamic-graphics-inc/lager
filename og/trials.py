# -*- coding: utf-8 -*-


from lager import LAGER
print(LAGER)


def somefunction():
    LAGER.info('somestring')
    # LAGER + "a string to log"

somefunction()


def flog(funk=None, loglevel="debug", funk_call=True, tictoc=False):
    """

    :param funk:
    :param loglevel:
    :param funk_call:
    :param tictoc:
    :return:
    """
    _logger = find_lager(name=str(funk))
    # print(_logger)
    _log_levels = {
        "debug": _logger.debug,
        "info": _logger.info,
        "warn": _logger.warning,
        "error": _logger.error,
    }

    def _decorate_flog_wrapper(_funk):
        def _fmt_args(*args):
            return ", ".join(str(arg) for arg in args)

        def _fmt_kwargs(**kwargs):
            return ", ".join("{}={}".format(str(k), str(v)) for k, v in kwargs.items())

        def _fmt_call(*args, **kwargs):
            params_str = ", ".join(
                s for s in (_fmt_args(*args), _fmt_kwargs(**kwargs)) if s
            )
            return "{}({})".format(funk.__name__, params_str)

        @wraps(_funk)
        def _flog_wrapper(*args, **kwargs):
            # _logger[loglevel]('=> {}'.format(_fmt_call(args, kwargs)))
            ti = time()
            _ret = _funk(*args, **kwargs)
            tf = time()
            print(ti)
            print(_logger, dir(_logger))
            _logger[loglevel](fmt.nseconds(ti, tf))
            # msg_parts = {
            #     "args-kwargs": _fmt_call(*args, **kwargs) if funk_call else None,
            #     "runtime": fmt.nseconds(ti, tf) if tictoc else None
            # }
            # _log_levels[loglevel](**msg_parts)
            return _ret

        return _flog_wrapper

    return _decorate_flog_wrapper(funk) if funk else _decorate_flog_wrapper

