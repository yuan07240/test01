import requests
import json
import urllib
import hmac,time
import hashlib
class UpApi:
    def __init__(self,sn):
        self.sn=sn
    def getAuthString(self):
        path = '/api/file/8011/uploadDownload/v2/'
        params = ''
        host = 'ota.sprocomm.com'
        Method = 'POST'
        timestamp = str(int(time.time()) * 1000)
        #签名算法
        ACCESS_KEY_ID='ea905204f3884deeac6305eff4fc54fc'
        APP_SECRET='2b224525efb44493b259b6cc952ab9b0'
        expirationPeriodInSeconds = '1800'
        authStringPrefix='sprocomm-auth-v1/'+ACCESS_KEY_ID+"/"+timestamp+"/"+expirationPeriodInSeconds
        header = {"Host":host,
                  "content-type": "application/json;charset=utf-8",
                  "timestamp": timestamp
                  }
        CanonicalHeaders = 'host:'+host
        CanonicalRequst=Method + "\n" + path + "\n" + params +"\n" + CanonicalHeaders
        signingKey=hmac.new(APP_SECRET.encode('utf-8'),authStringPrefix.encode('utf-8'),hashlib.sha256)
        signature = hmac.new((signingKey.hexdigest()).encode('utf-8'), CanonicalRequst.encode('utf-8'), hashlib.sha256)
        print(signature)
        header['Authorization'] = authStringPrefix + "/" + 'host' + "/" + signature.hexdigest()
        #return authStringPrefix + "/" + 'host' + "/" + signature.hexdigest()#
        return header

    def up_post(self):
        #header=self.getAuthString()
        get_url='https://sprocomm-8011-1258754892.cos.ap-guangzhou.myqcloud.com'+'/'+self.sn
        body = json.dumps({"sn": self.sn,
                           "url": get_url
                           })
        url = "https://ota.sprocomm.com/api/file/8011/uploadDownload/v2/"  # 请求地址
        r = requests.post(url, data=body, headers=self.getAuthString())
        print(r)
        return r

#if __name__=='__main__':
    #cc=UpApi('324324324')
    #print(cc.Up_post())

    # header = {"Host": host,
    #               "content-type": "application/json;charset=utf-8",
    #               "timestamp": timestamp
    #               }
    # header['Authorization'] = getAuthString()
    # print(header)
    # sn="73434344"
    # body=json.dumps({
    #       "sn" : sn,
    #     "url":'testing'
    #       })
    # url="https://ota.sprocomm.com/api/file/8011/uploadDownload/v2/"#请求地址
    # r=requests.post(url,data=body,headers=header)
    # print(r.text)
    #
    # print('#########################################')
    # #get
    # ur=url+sn
    # rr=requests.get(ur,headers=header)
    # print(rr.status_code)
    # print(rr.headers)
