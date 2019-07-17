# generate-zerodha-access-token
Here is simple and easy way for generating zerodha access key programmatically.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Requirements
* python3
* scrapy-1.6.0
* zerodha kite-apis

### Install Requirements
Install all requirement related to this code by using command 
> pip install -r requirements.txt

### Set Configurations
For generating access-token we need some details related to zerodha user account.
You can set all neccessary details inside config.py
```
.
├── zerodha-scrapper 
│   ├── config.py
```

```
user_id = ""
password = ""
pin = ""
api_key = ""
api_secret = ""
```

### Run
Finally to get access-token run scraper.py using command
> scrapy runspider scraper.py
