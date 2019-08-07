from lager import pour_lager, flog


log = pour_lager(filepath='logs4g.log')
log.info('some shit')
log.info('some bulllllll shit', howdy="someshit")


@flog(loglevel='info')
def add(a, b):
    return a + b



for i in range(14):
    add(i, 7)
#     log.info("info: " + str(i))
#     log.warning("warning: " + str(i))
#     if i % 7 == 0:
#         log.error('DA_error: ' + str(i))
#     if i % 13 == 0:
#         log.debug('DDDBUG: ' + str(i))
