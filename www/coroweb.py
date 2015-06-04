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
	

'''
create RequestHandler() to encapsulate a URL processing function
define __call__() in class RequestHandler, and we can look at it as a instance func
1. parse URL function to get parameters needed
2. get required parameters from request
3. call URL function
4. convert result to web.Response object
'''
def has_request_arg(fn):
	sig = inspect.signature(fn)
	params = sig.parameters
	found = False
	for name, param in params.items():
		if name == 'request':
			found = True
			continue
		if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
			raise ValueError('request parameter must be the last named parameter in function:%s%s' %(fn.__name__, str(sig)))
		return found
		
class RequestHandler(object):
	def __init__(self, app, fn):
		self._app = app
		self._func = fn
		self._has_request_arg = has_request_arg(fn)
		self._has_var_kw_args = has_var_kw_arg(fn)
		self.has_named_kw_args = has_named_kw_args(fn)
		self._named_kw_args = get_named_kw_args(fn)
		self._required_kw_args = get_required_kw_args(fn)
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
