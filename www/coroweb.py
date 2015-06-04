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
		
def has_var_kw_arg(fn):
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.VAR_KEYWORD:
			return True

def has_named_kw_args(fn):
	param = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			return True

def get_named_kw_args(fn):
	agrs = []
	params = inspect.signature(fn).parameters
	for name, param in params.items()
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			args.append(name)
	return tuple(args)

def get_required_kw_args(fn):
	args = []
	params = inspect.signature(fn).parameters
	for name, param in param.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)

		
class RequestHandler(object):
	def __init__(self, app, fn):
		self._app = app
		self._func = fn
		self._has_request_arg = has_request_arg(fn)
		self._has_var_kw_args = has_var_kw_arg(fn)
		self._has_named_kw_args = has_named_kw_args(fn)
		self._named_kw_args = get_named_kw_args(fn)
		self._required_kw_args = get_required_kw_args(fn)
		
		
	@asyncio.coroutine
	def __call__(self, request):
		kw = None
		if self._has_var_kw_args or self._has_named_kw_args or self._required_kw_args:
			if request.method == 'POST':
				if not request.content_type:
					return web.HTTPBadRequest('Missing Content-Type.')
				ct = request.content_type.lower()
				if ct.startwith('application/json'):
					params = yield from request.json()
					if not isinstance(names, dict):
						return web.HTTPBadRequest('JSON body must be object.')
					kw = params
				elif ct.startwith('application/x-www-from-urlencoded' or ct.startswith('multipart/form-data')):
					params = yield from request.post()
					kw = dict(**params)
				else:
					return web.HTTPBadRequest('Unsuppored Content-Type: %s' % request.content_type)
			if request.method == 'GET':
				qs = request.query_string
				if qs:
					kw = dict()
					for k, v in parse.parse_qs(qs, True).items():
						kw[k] = v [0]
						
		if kw is None:
			kw = dict(**request.match_info)
		else:
			if not self._has_var_kw_args and self._named_kw_args:
				#remove all unnamed kw:
				copy = dict()
				for name in self._named_kw_args:
					if name in kw:
						copy[name] = kw[name]
				kw = copy
			# check named arg:
			for k, v in request.match_info.items():
				if k in kw:
					logging.warning('Duplicate arg name in named arg and kw args: %s' %k)
				kw[k] = v
		if self._has_request_arg:
			kw['request'] = request
		#check required kw:
		if self._required_kw_args:
			for name in self._required_kw_args:
				if not name in kw:
					return web.HTTPBadRequest('Missing argument: %s' % name)
		logging.info('call with args: %s' % str(kw))
		try:
			r = yield from self._func(**kw)
			return r
		except APIError as e:
			return dict(error=e.error, data=e.data, message=e.message)
					
		
#write a add_route function for register a URL processing function
def add_route(app, fn):
	method = getattr(fn, '__method__', None)
	path = getattr(fn, '__route__', None)
	if path is None or method is None:
		raise ValueError('@get or @post not defined in %s.' %str(fn))
	if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
		fn = asyncio.coroutine(fn)
	logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
	app.router.add_route(method, path, RequestHandler(app, fn))

		
		
		
		
		
		
		
		
		
		
		
		
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
