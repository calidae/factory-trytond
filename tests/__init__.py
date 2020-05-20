import os
import time

from trytond import backend

# import pdb; pdb.set_trace()

try:
    backend_name = backend.name()
except TypeError:
    backend_name = backend.name

if backend_name == 'sqlite':
    database_name = ':memory:'
else:
    database_name = 'test_' + str(int(time.time()))
os.environ.setdefault('DB_NAME', database_name)
