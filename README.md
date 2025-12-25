# ttl_lru_cache_ignition_jy_backport
LRU cache backport for use in Ignition Jython/python 2.7 version

This is just a quick and dirty backport of using lru cache with Ignition scada platform's jython/python 2.7 version

The main function can be imported and decorated on any usually long running and less changing data or results to be cached and returned.

Example:
```python
@ttl_lru_cache(maxsize=200, ttl=3600)
def function_returning_not_frewuqnt_changing_data(parameter_1, parameter_2):
    # long running query

    # main logic

    return functions_result
```
