import json
from grab import Grab
from pprint import pprint

class Dropbox():
	"""Dropbox client"""

	login_url = 'https://www.dropbox.com/login'
	home_url = 'https://www.dropbox.com/home'

	def __init__(self, email, password):
		self.email = email
		self.password = password

		self.g = Grab()
		self.login()
		self.get_keys()
		
	def login(self):
		self.g.go(self.login_url)
		self.g.set_input('login_email', self.email)
		self.g.set_input('login_password', self.password)
		self.g.submit()

	def get_keys(self):
		self.g.go(self.home_url)
		self.ns = self.g.rex(r"root_ns: (\d+)").group(1)
		self.token = self.g.rex(r"TOKEN: '(.+?)'").group(1).decode('string_escape')

	def list_files(self, dirname=''):
		url = 'https://www.dropbox.com/browse%s' % dirname
		referer = 'https://www.dropbox.com/home%s' % dirname

		self.g.setup(
			headers=dict(referer=referer),
			post=dict(ns_id=self.ns, t=self.token),
			url=url
		)
		self.g.request()
		return json.loads(self.g.response.body)

if __name__ == '__main__':
	email = u"rocklasi@gmail.com"
	password = u"r0cklas1"

	dropbox = Dropbox(email, password)
	files = dropbox.list_files()
	pprint(files)