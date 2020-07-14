import urllib
import hmac,time
import hashlib
path='/api/file/8011/uploadDownload/v2/'
params=''
host='ota.sprocomm.com'
Method='POST'
timestamp = str(int(time.time())*1000)
print(timestamp)
#timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ',timestamp)
def getAuthString(path,params,host,Method,timestamp):
    #签名算法
    ACCESS_KEY_ID='ea905204f3884deeac6305eff4fc54fc'
    APP_SECRET='2b224525efb44493b259b6cc952ab9b0'
    expirationPeriodInSeconds = '1800'
    authStringPrefix='sprocomm-auth-v1/'+ACCESS_KEY_ID+"/"+timestamp+"/"+expirationPeriodInSeconds
    header = {"Host": host,
              "content-type": "application/json;charset=utf-8",
              "timestamp": timestamp
              }
    CanonicalHeaders = 'host:'+host
    CanonicalRequst=Method + "\n" + path + "\n" + params +"\n" + CanonicalHeaders
    signingKey=hmac.new(APP_SECRET.encode('utf-8'),authStringPrefix.encode('utf-8'),hashlib.sha256)
    signature = hmac.new((signingKey.hexdigest()).encode('utf-8'), CanonicalRequst.encode('utf-8'), hashlib.sha256)
    print(signature)
    header['Authorization'] = authStringPrefix + "/" + 'host' + "/" + signature.hexdigest()
    return authStringPrefix + "/" + 'host' + "/" + signature.hexdigest()#
cc=getAuthString(path,params,host,Method,timestamp)
print(cc)

import requests
import json

header = {"Host": host,
              "content-type": "application/json;charset=utf-8",
              "timestamp": timestamp
              }
header['Authorization'] = getAuthString(path,params,host,Method,timestamp)
print(header)
sn="7324534344"
url='https://sprocomm-8011-1258754892.cos.ap-guangzhou.myqcloud.com/'+sn
#腾讯云返回的存储sn号和url

body=json.dumps({
      "sn" : sn,
    "url":url
      })
url_hm="https://ota.sprocomm.com/api/file/8011/uploadDownload/v2/"#请求地址
r=requests.post(url_hm,data=body,headers=header)
print(r.text)

print('#########################################')
#get
ur=url+sn
print(ur)
rr=requests.get(ur,headers=header)
print(rr.status_code)
print(rr.headers)
