# Copyright, 2013 by Victor Mireyev

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
	email = "PUT_EMAIL_HERE"
	password = "PUT_PASSWORD_HERE"

	dropbox = Dropbox(email, password)
	files = dropbox.list_files()
	pprint(files)