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
