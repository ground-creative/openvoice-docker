import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path
import configparser
import pymysql.cursors
import json
import os, sys
from dotenv import load_dotenv

dotenv_path = Path(str(Path.cwd()) + '/.env')
load_dotenv(dotenv_path=dotenv_path)

MYSQL_HOST = os.getenv('MYSQL_HOST')  
MYSQL_USER = os.getenv('MYSQL_USER') 
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_PORT = int(os.getenv('MYSQL_PORT'))
MAX_FORM_SUBMISSIONS_X_DOMAIN = int(os.getenv('MAX_FORM_SUBMISSIONS_X_DOMAIN'))

class SpiderSpider(CrawlSpider):
	name = 'spider'
	
	def build_db(self):
		self.connection = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, port = MYSQL_PORT, password = MYSQL_PASSWORD)
		try: 
			with self.connection.cursor() as cursor:
				cursor.execute('CREATE DATABASE IF NOT EXISTS `' + self.campaign + '`')
				cursor.execute('USE `' + self.campaign + '`')
				sqlQuery = '''CREATE TABLE IF NOT EXISTS forms(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
							session VARCHAR (255), 
							domain VARCHAR (255), 
							url TEXT, 
							sent DATETIME DEFAULT NOW(),
							method VARCHAR (255), 
							action TEXT,
							data TEXT,
							response TEXT,
							html TEXT)'''
				cursor.execute(sqlQuery)
		finally:
			print('Running campaign ' + self.campaign)

	def __init__(self, session, start_urls = '', campaign = 'default', mode = 'collect-data', *args, **kwargs):
		super(SpiderSpider, self).__init__(*args, **kwargs)
		self.start_urls = [ start_urls ] if isinstance(start_urls, str) else start_urls
		#self.base_url = start_urls
		self.campaign = campaign
		self.campaign_file = str(Path.cwd()) + '/campaigns/'+ campaign + '.txt'
		configParser = configparser.RawConfigParser()   
		configFilePath = self.campaign_file
		configParser.read(configFilePath)
		self.campaign_email = configParser.get('campaign-config', 'email')
		self.campaign_firstname = configParser.get('campaign-config', 'firstname')
		self.campaign_lastname = configParser.get('campaign-config', 'lastname')
		self.campaign_message = configParser.get('campaign-config', 'message')
		self.mode = mode
		self.build_db();
		self.form_count = 0
		self.session = session
		
	rules = [Rule(LinkExtractor(allow_domains = self.start_urls), callback = 'parse', follow = True)]
	
	def parse_start_url(self, response):
		return self.parse(response)
	
	def form_submitted(self, response):
		self.save_data(response.meta['data'], response.meta['action'], 
			response.meta['response'], response.meta['method'], response.meta['form'], response)
		if (response.status == 200):
			self.form_count = self.form_count + 1

	# We check if the html page has forms
	# We try to build the form action and method
	# We try to find textareas and submit buttons
	# If they do exist, we assume it's a contact form and use an engine to fill in all form fields
	# We will try to guess fields and populate them with the values
	# At this stage we will try to send the form and log the request and the response in the db
	
	def parse(self, response):
		if (self.form_count >= MAX_FORM_SUBMISSIONS_X_DOMAIN):
			raise CloseSpider('submitted_too_many_forms')
		forms = response.css('form')
		for form in forms:
			method = form.xpath('@method').extract_first()
			action = form.xpath('@action').extract_first()
			if (method is None):
				method = 'get'
			if (action is None or len(action) == 0 or action == '/'):
				action = response.request.url
			if (False == bool(urlparse(action).netloc)):
				if (action[0] == '/'):
					action = response.url + action
				else:
					base_url = response.request.url + '/' if response.request.url[-1] != '/' else response.request.url
					action = base_url + action
			action = action.replace('//', '/')
			action = action.replace('http:/', 'http://')
			action = action.replace('https:/', 'https://')
			textareas = form.xpath('.//textarea')
			submit_btn = form.xpath('.//input[@type="submit"]')
			submit_name = submit_btn.xpath('@name').extract_first()
			if (submit_btn and submit_name and textareas):	# check if we have textareas and submit buttons
				data = {}
				data[submit_btn.xpath('@name').extract_first()] = submit_btn.xpath('@value').extract_first()
				for textarea in textareas:
					data[textarea.xpath('@name').extract_first()] = self.campaign_message
				select_menus = form.xpath('.//select')
				if (select_menus):
					for select_menu in select_menus:
						options = select_menu.xpath('.//option')
						if (options):
							for option in options:
								value = option.xpath('@value').extract_first()
								if (len(value) > 0):
									data[select_menu.xpath('@name').extract_first()] = value
									break
				inputs = form.xpath('.//input')
				if (inputs):
					for input in inputs:
						name = input.xpath('@name').extract_first()
						type = input.xpath('@type').extract_first()
						# check placeholders
						placeholder = input.xpath('@placeholder').extract_first()
						if (placeholder):
							if "email" in placeholder.lower():
								data[name] = self.campaign_email
							elif "lastname" in placeholder.lower():
								data[name] = self.campaign_lastname
							elif "last name" in placeholder.lower():
								data[name] = self.campaign_lastname
							elif "firstname" in placeholder.lower():
								data[name] = self.campaign_firstname
							elif "first name" in placeholder.lower():
								data[name] = self.campaign_firstname
							elif "name" in placeholder.lower():
								data[name] = self.campaign_firstname	
						if (hasattr(data, name) == False and type != 'submit'):	# check types
							if (type == 'email'):
								data[name] = self.campaign_email
							elif (type == 'checkbox' or type == 'radio'):
								data[name] = input.xpath('@value').extract_first()
							elif (type == 'text'):
								if "lastname" in name.lower():
									data[name] = self.campaign_lastname
								elif "firstname" in name.lower():
									data[name] = self.campaign_firstname
								elif "name" in name.lower():
									data[name] = self.campaign_firstname
								elif "email" in name.lower():
									data[name] = self.campaign_email							
								else:								
									data[name] =  'n/c'
							else:
								data[name] = 'n/c'
					#print("FORM ACTION: ", action)
					#print("FORM METHOD: ", method.upper())		
					#print("FORM DATA: ", data)
					# Submit this form
					if (self.mode  == 'send-forms'):
						yield scrapy.FormRequest(url = action, meta = 
							{'data': data, 'action': action, 'response': response, 'method': method, 'form': form}, 
							formdata = data, method = method.upper(), callback = self.form_submitted)
					else:
						self.save_data(data, action, response, method, form)
			#print("done")
			
	def save_data(self, data, action, response, method, form, form_response = None):
		try:
			with self.connection.cursor() as cursor:
				sqlQuery = '''INSERT INTO forms (session, domain, url, method, action, data, html, response) 
						VALUES ("''' + self.session.lower() + '''","''' + response.url + '''","''' + response.request.url + '''","''' + method.upper() + '''","''' + action + '''", %s, %s, %s)'''
				#print(sqlQuery)
				cursor.execute(sqlQuery, (json.dumps(data), form.extract(), form_response))
				self.connection.commit()
				#record_id = cursor.execute('select last_insert_id() from forms')
		finally:
			#print('Saved record to db: ', record_id)
			print('Saved record to db')