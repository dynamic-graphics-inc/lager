# Lager :beer: ~ small and EZ python logging

<img src="_data/dgpy_logo.svg" alt="drawing" width="120"/> **Dynamic Graphics Python**

[![Wheel](https://img.shields.io/pypi/wheel/lager.svg)](https://img.shields.io/pypi/wheel/lager.svg)
[![Version](https://img.shields.io/pypi/v/lager.svg)](https://img.shields.io/pypi/v/lager.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/lager.svg)](https://img.shields.io/pypi/pyversions/lager.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install lager`

Lager is a python logging library created primarily because of how fantastic the name is.

It's easy to use! It's got color support! It's got JSON!

```python
from lager import pour_lager
log = pour_lager()  # make logger
log.info("hello info")
log + "hello info"
log += "hello info"
log.debug("hello debug")
log - "hello debug"
log -= "hello debug"
log.warning("hello warning")
log * "hello warning"
log *= "hello warning"
log.error("hello error")
log ** "hello error"
log **= "hello error"
```

## Got JSON??

Checkout [jsonbourne](https://github.com/dynamic-graphics-inc/jsonbourne) (if you get the chance)!
