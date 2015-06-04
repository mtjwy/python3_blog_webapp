#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yu'

'''
async web application.
'''

import logging; logging.basicConfig(level = logging.INFO)#Does basic configuration for the logging system . #Logging messages which are less severe than lvl will be ignored
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

@asyncio.coroutine
def logger_factory(app, handler):
	@asyncio.coroutine
	def logger(request):
		logging.info('Request: %s %s' % (request.method, request.path))
		# yield from asyncio.sleep(0.3)
		return (yield from handler(request))
	return logger

#response middleware is to convert return value to web.Response object，so as to meet the requirement of aiohttp：
@asyncio.coroutine
def response_factory(app, handler):
	@asyncio.coroutine
	def response(request):
		logging.info('Response handler...')
		r = yield from handler(request)
		if isinstance(r, web.StreamResponse):
			return r
		if isinstance(r, bytes):
			resp = web.Response(body=r)
			resp.content_type = 'application/octet-stream'
			return resp
		if isinstance(r, str):
			if r.startswith('redirect:'):
				return web.HTTPFound(r[9:])
			resp = web.Response(body=r.encode('utf-8'))
			resp.content_type = 'text/html;charset=utf-8'
			return resp
		if isinstance(r, dict):
			template = r.get('__template__')
			if template is None:
				resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
				resp.content_type = 'application/json;charset=utf-8'
				return resp
			else:
				resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
				resp.content_type = 'text/html;charset=utf-8'
				return resp
		if isinstance(r, int) and t >= 100 and t < 600:
			return web.Response(t)
		if isinstance(r, tuple) and len(r) == 2:
			t, m = r
			if isinstance(t, int) and t >= 100 and t < 600:
				return web.Response(t, str(m))
		# default:
		resp = web.Response(body=str(r).encode('utf-8'))
		resp.content_type = 'text/plain;charset=utf-8'
		return resp
	return response

def index(request):#create a request handler. # accepts only request parameters of type Request and returns Response instance.
	return web.Response(body = b'<h1>Awesome Blog</h1>')
	
@asyncio.coroutine
def init(loop):
	#in app.py, adding middleware、jinja2 template and auto register support：
	yield from orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='123', db='blogWeb')
	app = web.Application(loop = loop, middlewares = [
		logger_factory, response_factory
	])#create a Application instance 
	init_jinja2(app, filters=dict(datetime=datetime_filter))
	add_routes(app, 'handlers')
	add_static(app)
	#app.router.add_route('GET', '/', index)#register handler in the application’s router pointing HTTP method, path and handler.
	srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 5000)#Create a TCP server
	logging.info('server started at http://127.0.0.1:5000...')
	return srv

loop = asyncio.get_event_loop()#Returns an event loop object implementing the BaseEventLoop interface. #
loop.run_until_complete(init(loop))#Run until the Future is done.
loop.run_forever()

'''
The event loop is the central execution device provided by asyncio. 
It provides multiple facilities, amongst which:

Registering, executing and cancelling delayed calls (timeouts).
Creating client and server transports for various kinds of communication.
Launching subprocesses and the associated transports for communication with an external program.
Delegating costly function calls to a pool of threads.
'''
