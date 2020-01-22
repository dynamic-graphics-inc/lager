# Lager :beer:

<img src="_data/dgpy_logo.svg" alt="drawing" width="120"/> **Dynamic Graphics Python**

[![Wheel](https://img.shields.io/pypi/wheel/lager.svg)](https://img.shields.io/pypi/wheel/lager.svg)
[![Version](https://img.shields.io/pypi/v/lager.svg)](https://img.shields.io/pypi/v/lager.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/lager.svg)](https://img.shields.io/pypi/pyversions/lager.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install lager`

Logging library for python with a sweet name and the use of operators!

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
