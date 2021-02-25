
[![PyPI](https://img.shields.io/pypi/v/pycaches?style=flat-square)](https://pypi.org/project/pycaches/)
[![Travis build on master](https://img.shields.io/travis/codingjerk/pycaches/master?style=flat-square)](https://travis-ci.org/github/codingjerk/pycaches)
[![Travis build on develop](https://img.shields.io/travis/codingjerk/pycaches/develop?label=develop&style=flat-square)](https://travis-ci.org/github/codingjerk/pycaches)
[![Codecov coverage](https://img.shields.io/codecov/c/gh/codingjerk/pycaches/develop?token=VHP5IBJTDJ&style=flat-square)](https://codecov.io/gh/codingjerk/pycaches/)
[![Chat on Gitter](https://img.shields.io/gitter/room/codingjerk/pycaches?style=flat-square)](https://gitter.im/codingjerk/pycaches)
![License](https://img.shields.io/pypi/l/pycaches?style=flat-square)

Python Implements Caching

## 特点

✓ 支持的缓存策略 ：random, LRU

✓ 使用装饰器的形式来使用缓存

✓ 支持 `Hashable` keys (dictionaries, lists, sets)

✓ 支持超时缓存处理

✓ 支持缓存数据统计

## 安装

```
pip install mycache
```

## 使用

### `cache` 装饰器

```python
from mycache import cache


@cache()
def example():
    print("你好，这里是mycache测试案例")


example()  # 你好，这里是mycache测试案例
example()  # 没有任何输出
```

```python
import time

from mycache import cache


@cache()
def long_computation(x):
    print("Performing long computation...")
    time.sleep(1)
    return x + 1


long_computation(5)  # Sleeps for 1 second and returns 6
long_computation(5)  # Immediately returns 6

long_computation(6)  # Sleeps for 1 second and returns 7
long_computation(6)  # Immediately returns 7
long_computation(6)  # And again
```

### 缓存类

```python
import time
from datetime import timedelta

from mycache import Cache

cache = Cache()
cache.save("a", 1)
cache.save("b", 2)
cache.save("c", 3, expire_in=timedelta(seconds=10))

cache.has("c")  # returns True
cache.get("a")  # returns 1

time.sleep(10)
cache.has("c")  # False
cache.get("c")  # raises KeyError
```

### 设置缓存类型

```python
from mycache import Cache
from mycache.policies import LRU

"""
设置缓存处理方式和缓存个数
"""

cache = Cache(max_items=2, replacement_policy=LRU())
cache.save("a", 1)
cache.save("b", 2)
cache.save("c", 3)

cache.has("a")  # returns False
cache.has("b")  # returns True

cache.save("d", 4)

cache.has("b")  # returns False
```

### Disable `deepcopy` for keys

```python
from mycache import cache

"""
缓存类和缓存装饰器接受' copy_keys '参数。
如果你能保证即使键是可变的也不会改变，
你可以把它设置为“True”来加快速度。
"""


@cache(copy_keys=False)
def faster_caching(x):
    return x


faster_caching({1, 2, 3})  # returns {1, 2, 3}
```

## 使用相关工具

1. `make lint`: `pylint` and `pycodestyle`
1. `make typecheck`: `mypy`
1. `make test`: `pytest`
1. `make coverage`: `pytest` with `pytest-cov`
1. `make quality`: `radon`
1. `make build`: `setup.py`
