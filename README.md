#Certifiable for Python

[![Author](https://img.shields.io/badge/Author:%20francis%20horsman-Available-brightgreen.svg?style=plastic)](https://www.linkedin.com/in/francishorsman)
[![Build Status](https://travis-ci.org/sys-git/certifiable.svg?branch=master)](https://travis-ci.org/sys-git/certifiable)
[![Coverage Status](https://coveralls.io/repos/github/sys-git/certifiable/badge.svg)](https://coveralls.io/github/sys-git/certifiable)
[![Documentation Status](https://readthedocs.org/projects/certifiable/badge/?version=latest)](http://certifiable.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/certifiable.svg)](https://badge.fury.io/py/certifiable)
[![PyPI](https://img.shields.io/pypi/l/certifiable.svg)]()
[![PyPI](https://img.shields.io/pypi/wheel/certifiable.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/certifiable.svg)]()
[![PyPI](https://img.shields.io/pypi/status/certifiable.svg)]()
[![Updates](https://pyup.io/repos/github/sys-git/certifiable/shield.svg)](https://pyup.io/repos/github/sys-git/certifiable/)
[![Python 3](https://pyup.io/repos/github/sys-git/certifiable/python-3-shield.svg)](https://pyup.io/repos/github/sys-git/certifiable/)

##Certifiable is a powerful runtime parameter validation library for python

It can validate the following types:

* Text
* Bytes
* Bool
* Int
* Long
* Number
* Decimal
* Float
* Enum
* List
* Tuple
* Iterable
* Set
* Dict
* Timestamp
* Date
* Json
* html
* Object
* Email

##Example
```python
    >>> from certifiable import validate_bool
    >>> validate_bool(True)
```

```python
    >>> validate_bool(False)
```

```python
    >>> validate_bool(1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 302, in certify_bool
        required=required,
    certifiable.errors.CertifierTypeError: expected bool, but value is of type 'int'
    >>>
```
##To install

```
    $ pip install certifiable
```

##Build documentation

```
    $ make docs
```
