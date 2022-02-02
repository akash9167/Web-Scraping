import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

url = 'https://www.zillow.com/graphql/'

headers = {'authority': 'www.zillow.com', 'method':'POST'
, 'path': '/graphql/?zpid=19620225&timePeriod=TEN_YEARS&metricType=LOCAL_HOME_VALUES&forecast=true&useNewChartAPI=false&operationName=HomeValueChartDataQuery'
, 'scheme': 'https'
, 'accept-encoding': 'gzip, deflate, br'
, 'content-length': '33427'
, 'content-type': 'text/plain'
, 'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6'
, 'cookie': 'JSESSIONID=C9CFDA3458EE55D2B3833E1FA62421C5; zguid=23|%241a1e0a42-46db-44d0-b8a9-6e67d723cdab; zgsession=1|2b602296-e195-4d0f-ab56-5bc045a980bb; _ga=GA1.2.129808499.1642902307; _gid=GA1.2.1098579153.1642902307; zjs_user_id=null; zjs_anonymous_id=%221a1e0a42-46db-44d0-b8a9-6e67d723cdab%22; _pxvid=17a75cc8-7bee-11ec-97f3-5772726f5258; _gcl_au=1.1.285860015.1642902318; KruxPixel=true; DoubleClickSession=true; __pdst=58252345e1ea4820afe5a5dd414a3f1e; _pin_unauth=dWlkPU1qVXhORGd5TldZdE9HRm1OeTAwWVdaaUxXRTVOamd0TnpoaE1XWXhaamN6TVRkaw; utag_main=v_id:017e849bebb90020854362d228f805072005406a00978$_sn:1$_se:1$_ss:1$_st:1642904118012$ses_id:1642902318012%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session; KruxAddition=true; _px3=2ecef9ad9b15952f08b1ca198cd88b1576a9e9ceb3857fe44a27dc6ca3ee5bef:LhuYPYRQLJjw/B/L3PNBAxoy9/O6wS7tZYvwhqTOsdYmv65VjkcWB7CA/QJ7MVkDFUQyiIOhkpuoNTfSjS25yw==:1000:nGDUsicK1s9r8Dm8BX4gaNNoq2U+3GOlroFevN+/526BPdIHMG/0tctiKrJgctpOsPtlTi1pzIRQsBh2zAMTXkxOii4Oeaq8E+3vdNm/NarlKuvgG6BrS2sAPPJ56arcBF5iJHuZ6JIWOJJH+MP0KuXE5CPuQoxbG7gyANYfoEbXJjQYj+8vufALqErzxDdLCMBo6FpBf7FWEOBipZxxUw==; _uetsid=1e362a207bee11ecbe0c2b873a9b719d; _uetvid=1e36aeb07bee11ec8f082d41bd835662; search=6|1645495076779%7Crect%3D37.37322667464881%252C-121.89459800720215%252C37.279311694254616%252C-122.16444969177246%26zpid%3D19620225%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%09%09%09%09%09%09%09; _gat=1; AWSALB=zYl9M9RvqyXjKxRWPU11W7EOvAmHX6Fg+FpK39wy68dJ0jzR7iAHNr8UWU0scnIoV7Ty+YlPv8E2EmwprxQRNCc5rmjs6243VQYj8ZlJ9AMOpxbxAbDh6fQJbO0X; AWSALBCORS=zYl9M9RvqyXjKxRWPU11W7EOvAmHX6Fg+FpK39wy68dJ0jzR7iAHNr8UWU0scnIoV7Ty+YlPv8E2EmwprxQRNCc5rmjs6243VQYj8ZlJ9AMOpxbxAbDh6fQJbO0X'
,'origin': 'https://www.zillow.com'
,'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

# Simulate API payload
def json_homevalue(zpid):
    #this is payload, i.e., the query sent to zillow server
    chartData = {"operationName":"HomeValueChartDataQuery","variables":{"zpid":00000}
    ,"query":"query HomeValueChartDataQuery($zpid: ID!, $metricType: HomeValueChartMetricType, $timePeriod: HomeValueChartTimePeriod, $useNewChartAPI: Boolean) {\n  property(zpid: $zpid) {\n    homeValueChartData(metricType: $metricType, timePeriod: $timePeriod, useNewChartAPI: $useNewChartAPI) {\n      points {\n        x\n        y\n      }\n      name\n    }\n  }\n}\n"
    ,"clientVersion":"home-details/6.0.11.7057.master.becbcc5"}
    chartData['variables']['zpid']=zpid

    return chartData

# Get homevalue json object using API
def get_json_homevalue(zpid):
    #get json query ready, zpid as input
    chartData = json_homevalue(zpid)
    homevalueScore = []

    try:
        chart_req = requests.post(url=url, json=chartData, headers=headers) #send request to zillow server

        chart_out = json.loads(chart_req.text) #get the response from zillow server and load as json object

        #parse the json object to extract scores
        homevalueScore.append(chart_out['data']['property']['homeValueChartData'])

        return homevalueScore

    except Exception as e:
        print ('error not 200, home value, try again', e)
        return homevalueScore

# Parsing json to get output
output=get_json_homevalue(19620225)
output_df = pd.DataFrame(output[0][0]['points'])

# Convert unix timestamp to date time
output_df['date'] = output_df['x'].apply(lambda x: datetime.utcfromtimestamp(x/1000).strftime('%d/%m/%Y'))
output_df['mm_y'] = output_df['date'].apply(lambda x: x[3:] )
output_df = output_df.sort_values(by='x')
output_df = output_df.drop('x', axis=1)

output_df['date'] = output_df['date'].astype('datetime64[ns, US/Central]')

print(output_df[['mm_y', 'y']])

output_df.to_csv('house_prices.csv')

plt.plot(output_df['date'], output_df['y'])
plt.xlabel('Year')
plt.ylabel('Housing Prices')
plt.title('Changing in housing prices over years')
# plt.xticks(np.arange(min(output_df['mm_y']), max(output_df['mm_y'])+1, 1.0))

plt.show()