#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aysncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
from apis import APIError

#decorate a func to be a URL processing func

#Define decorator @get('/path')
def get(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator


#Define decorator @post('/path')
def post(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw)
			return func(*args, **kw)
		wrapper.__method__ = 'POST'
		wrapper.__route__ = path
		return wrapper
	return decorator
	
