
import http.server
import requests
import os
from PRNG import PRNG
import threading
from socketserver import ThreadingMixIn
from urllib.parse import unquote, parse_qs


prng = PRNG()

dtype = 6

b = prng.GetRandomInt(dtype)

print(b)

dtype = 8

b = prng.GetRandomInt(dtype)

print(b)

dtype = 20

b = prng.GetRandomInt(dtype)

print(b)

