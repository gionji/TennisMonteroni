# importing the requests library 
import requests 
import sys
  
# defining the api-endpoint  
API_ENDPOINT = "http://localhost/"
  
# your API key here 
API_KEY = "XXXXXXXXXXXXXXXXX"
  
# your source code here 
court = sys.argv[1]
service = sys.argv[2]
time = sys.argv[3]


# data to be sent to api 
data = {'court':court,
        'service':service,
        'time':time} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 
