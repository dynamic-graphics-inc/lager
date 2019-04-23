# -*- coding: utf-8 -*-


from lager import LAGER
print(LAGER)


def somefunction():
    LAGER.info('somestring')
    # LAGER + "a string to log"

somefunction()
