import scrapy
import json
import re
from termcolor import cprint 
from config import *
from zerodha_apis import generate_access_token

class ZerodhaSpider(scrapy.Spider):
	name = "request_token"
	start_urls = ['https://kite.zerodha.com']

	def parse(self, response):
		payload = {"user_id":user_id,"password":password}
		headers = {
			'Content-Type': "application/x-www-form-urlencoded",
			'Cache-Control': "no-cache"
			}

		link = self.make_req(payload,self.parse2,url='https://kite.zerodha.com/api/login',headers=headers) 
		return link


	def parse2(self,response):
		jsonresponse = json.loads(response.body_as_unicode())
		request_id = jsonresponse.get("data").get("request_id")

		url = "https://kite.zerodha.com/api/twofa"
		payload = {"user_id":user_id,"request_id":request_id ,"twofa_value":pin}
		headers = {
		'Content-Type': "application/x-www-form-urlencoded",
		'Cache-Control': "no-cache",
		}

		req = self.make_req(payload,self.parse3,url=url,headers=headers)
		return req

	def parse3(self,response):
		url = "https://kite.trade/connect/login?v=3&api_key={api_key}".format(api_key=api_key)

		headers = {
		'Cache-Control': "no-cache",
		'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
		'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}

		req = self.make_req({},self.parse4,url=url,headers=headers,method='GET')
		return req

	def parse4(self,response):
		url = response.url
		request_token_regex = re.search("request_token\=(.*?)[^\&]+",url)
		request_token = request_token_regex.group(0).split("=")[1]
		access_token = generate_access_token(api_key,api_secret,request_token)
		cprint('request_token : '+request_token, 'green', 'on_red') 
		cprint('access_token : '+access_token, 'green', 'on_red')



	def make_req(self,form_data,callback,dont_filter=False,*args,**kwargs):
		url = kwargs.get('url')
		method = kwargs.get('method')
		headers = kwargs.get('headers')
		if method is None:
			method = 'POST'
		if headers is None:
			headers = {}

		link = scrapy.FormRequest(
						url=url,
						method=method,
						formdata=form_data,
						errback=self.handle_page_error,
						callback=callback,
						dont_filter=True,
						headers=headers,
							)
		link.meta['formdata'] = form_data
		return link

	def handle_page_error(self,failure):
		print("[*]Inside handle_page_error",failure.request.url)
		return failure.request