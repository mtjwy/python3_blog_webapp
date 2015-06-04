#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yu'

import asyncio, logging
import aiomysql

def log(sql, args = ()):
	logging.info('SQL: %s' % sql)

#create a global connection pool
@asyncio.coroutine
def create_pool(loop, **kw):
	logging.info('create database connection pool..')
	global __pool
	__pool = yield from aiomysql.create_pool(
		host = kw.get('host', 'localhost'),
		port = kw.get('port', 3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charset = kw.get('charset', 'utf-8'),
		autocommit = kw.get('autocommit', True),
		maxsize = kw.get('maxsize', 10),
		minsize = kw.get('minsize', 1),
		loop = loop
	)
	
#wrap SELECT query
@asyncio.coroutine
def select(sql, args, size = None):
	log(sql, args)
	global __pool
	with (yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?', '%s'), args or ())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('row returned: %s' % len(rs))
		return rs

#wrap INSERT, UPDATE, DELETE
@asyncio.coroutine
def execute(sql, args, autocommit=True):
	log(sql)
	with (yield from __pool) as conn:
		if not autocommit:
			yield form conn.begin()
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?', '%s'), args)
			affected = cur.rowcount
			yield from cur.close()
			if not autocommit:
				yield from conn.commit()
		except BaseException as e:
			if not autocommit:
				yield from conn.rollback()
			raise
		return affected

#define the base class Model for all the ORM
class Model(dict, metaclass=ModelMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)
	
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s' %key")
	
	def __setattr__(self, key, value):
		self[key] = value
	
	def __getValue(self, key):
		return gatattr(self, key, None)
	
	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		if value is None:
			field =self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s: %s' %(key, str(value)))
				setattr(self, key, value)
		return value
		
#Add Field class and its various subclasses
class Field(object):
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
	def __str__(self):
		return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
	def __init__(self, name = None, primary_key=False, default=None, ddl='varchar(100)'):
		super().__init__(name, ddl, primary_key, default)
		
class BooleanField(Field):
	def __init__(self, name=None, default=False):
		super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
	def __init__(self, name=None, primary_key=False, default=0):
		super().__init__(name, 'bigint', primary_key, default)
		
class FloatField(Field):
	def __init__(self, name=None, primary_key=False, default=0.0):
		super().__init__(name, 'real', primary_key, default)
		
class TextField(Field):
	def __init__(self, name=None, default=None):
		super().__init__(name, 'text', False, default)

		





















