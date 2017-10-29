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
* Time
* Json
* html
* Object
* Email

And also these more `complex` or compound types into which you can pass `other` certifiers:

* List
* Tuple
* Set
* Iterable
* Dict
* Json
* Html
* Email

There are logical operators to combine certifiers:

* ANY   (certify_only_one)
* AND   (certify_all)
* ALL   (certify_all)
* NAND  (certify_none)
* XOR   (certify_only_one)

Custom Certifier
----------------

Use the `make_certifier` decorator and (optionally) bake-in some args and kwargs (any return value
from a certifier is ignored) to create your own certifier (first arg must be the value to certify):

```python
    >>> @make_certifier
    ... def my_certifier(value, *baked_args, **baked_kwargs):
    ...     print value
    ...     print baked_args
    ...     print baked_kwargs
    ...     baked_kwargs['data'].append('green')
    ...     if len(baked_kwargs['data'])==2:
    ...         raise MyError('damn!')

    >>> args_to_bake = ('eggs', 'ham')
    >>> kwargs_to_bake = dict(spam='lots', data=[])
    >>> certifier = my_certifier(*args_to_bake, **kwargs_to_bake)
```
certifier can now be used as an argument to other certifiers:

```
    >>> certify_list(
    ...     [1,'a'],
    ...     certifier=certifiers,
    ...     min_len=2,
    ...     max_len=5,
    ...     required=True,
    ... )
    1
    ('eggs', 'ham')
    {'spam': 'lots', data: []}
    'a'
    ('eggs', 'ham')
    {'spam': 'lots', data: ['green']}
    Traceback (most recent call last):
        ...
        ...
        ...
    MyError: damn!
```

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
    CertifierTypeError: expected bool, but value is of type 'int'
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
