from lager.httpx import HttpxSink
from lager import LAGER_PORT
from lager import LOG as log
import httpx


httpx.post('http://localhost:52437/', data={
    'herm': 234
    })
httpsink = HttpxSink(url=f'http://localhost:{LAGER_PORT}')
log.add(
    httpsink, level="DEBUG",
    serialize=True
    )
log.info('something else')
log.debug('something else')
# log.info('some other thing herm', howdy="something")
log.warning('some warning')
# log = pour_lager(filepath='herm.log')
log.info('howdy')
# log + "herm"
#
# log += "herm plus eq"
# log + {
#     "hermo": "herm",
#     "somethign": "hwer"
#     }
# print(log)
#
# log - "debug msg"
# log -= "debug msg"
# log * "warning msg"
# log *= "warning msg"
# log ** "error"
# log **= "error msg"
#
# log.e("error msg again")
# log.c("critical msg again")
# # for i in range(10000):
# #     log.info("info: " + str(i))
# #     log.warning("warning: " + str(i))
# #     if i % 7 == 0:
# #         log.error('DA_error: ' + str(i))
# #     if i % 13 == 0:
# #         log.debug('DDDBUG: ' + str(i))
#
# # a = load_log('herm.log')
