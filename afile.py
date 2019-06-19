from lager import pour_lager

log = pour_lager(logfile='logs4g.log')
log.info('some shit')
log.info('some bulllllll shit', howdy="someshit")

for i in range(10000):
    log.info("info: " + str(i))
    log.warning("warning: " + str(i))
    if i % 7 == 0:
        log.error('DA_error: ' + str(i))
    if i % 13 == 0:
        log.debug('DDDBUG: ' + str(i))


