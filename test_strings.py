

LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
giat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
"""
SAMPLE_ERROR = """
BEGIN_SAMPLE_ERROR (not a real error in django!)
Exception in thread django-main-thread:
Traceback (most recent call last):
  [...]
  File "/home/tianshu/projects/checkin/checkin/checkin/urls.py", line 25, in <module>
    path('api/', include('api.urls'))
  File "/home/tianshu/.local/lib/python3.6/site-packages/django/urls/conf.py", line 34, in include
    urlconf_module = import_module(urlconf_module)
  File "/usr/lib/python3.6/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 994, in _gcd_import
  File "<frozen importlib._bootstrap>", line 971, in _find_and_load
  File "<frozen importlib._bootstrap>", line 955, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 665, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 678, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/home/tianshu/projects/checkin/checkin/api/urls.py", line 2, in <module>
    from . import node
  File "/home/tianshu/projects/checkin/checkin/api/node.py", line 5, in <module>
    from .util import json_response
  File "/home/tianshu/projects/checkin/checkin/api/util.py", line 8
    type(out) == tuple:
                      ^
SyntaxError: invalid syntax
"""
