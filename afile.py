from lager import pour_lager, load_log

log = pour_lager()
log.info('some shit')
log.debug('some shit')
log.info('some bulllllll shit', howdy="someshit")
log.warning('some shit')
log = pour_lager(filepath='herm.log')
log.info('ho')
# for i in range(10000):
#     log.info("info: " + str(i))
#     log.warning("warning: " + str(i))
#     if i % 7 == 0:
#         log.error('DA_error: ' + str(i))
#     if i % 13 == 0:
#         log.debug('DDDBUG: ' + str(i))

a = load_log('herm.log')
