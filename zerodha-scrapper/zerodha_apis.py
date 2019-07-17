from kiteconnect import KiteConnect

def generate_access_token(api_key,api_secret,request_token):
	kite = KiteConnect(api_key=api_key)
	data = kite.generate_session(request_token, api_secret=api_secret)
	return data.get('access_token')

