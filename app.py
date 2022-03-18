# This is needed to send POST and GET requests
import requests
import pandas as pd

# This is needed to limit the frequeny 
# by which we are going to hit the API 
# endpoints. Only certain number of 
# requests can be made in a mintue
import time

# This is needed to convert API 
# responses into JSON objects
import json

# Godaddy developer key and secret
api_key = "your api_key"
secret_key = "your secret_key"

# API key and secret are sent in the header
headers = {"Authorization" : "sso-key {}:{}".format(api_key, secret_key)}

# Domain availability and appraisal end points
url = "https://api.ote-godaddy.com/v1/domains/available?checkType=FULL"
appraisal = "https://api.ote-godaddy.com/v1/appraisal/{}"

# If a domain name is available 
# decide whether to appraise or not
do_appraise = True

# Number of domains to check in each call. 
# For example, we can not check more than 500 
# domain names in one call so we need to split 
# the list of domain names into chunks
chunk_size = 500

# Filter domain names by length
max_length = 30

# Filter domain names by price range
min_price = 0
max_price = 1000000

# If appraisal is enabled, only include 
# domain names with min appraisal price
min_appr_price = 0

# When a domain is appraised, Godaddy API 
# returns similar domains sold. This is a 
# nice feature to take a look at sold domains. 
# To filter similar sold domains we can do that 
# by setting the min sale price and the min 
# year the domain was sold
min_sale_price = 0
min_sale_year = 2000
# This list holds similar domains sold
# This is retrieved from Godaddy appraisal API
similar_domains = []
# This holds available domains found that match
# the search criteria
found_domains = {}
all_domains = pd.read_excel("/content/drive/MyDrive/Data Science/backlinks.xlsx", engine='openpyxl')

df = pd.DataFrame(columns= ["Domains"])
#for domains in domain_chunks:
   # Get availability information by calling availability API
for x in range(0, len(all_domains)):

        # Define request parameter
      dom = all_domains.iloc[x]["domains"]
      availability_res = requests.get('https://api.ote-godaddy.com/v1/domains/available?domain={}&checkType=FAST'.format(dom), headers=headers);
      time.sleep(1)
        # Get only available domains with price range
      result = json.loads(availability_res.text)
      #if (availability_res.text.find('"available":true') != -1):
      if "available" in availability_res.text:
        if result["available"]==True:
          if result["definitive"]==True: 
            #price = float(result["price"])/1000000 
            #print("{:30} : {:10} {:10}".format(result["domain"], price, result["currency"]))
            df.loc[x, 'Domains'] = result["domain"]
            df.to_excel('/content/drive/MyDrive/work/domains.xlsx', sheet_name= 'sheet1')
            print(result["domain"])
            print(x+1)
