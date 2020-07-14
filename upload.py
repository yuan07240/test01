# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
import os,time
import sys
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
class Upfile:

    def __init__(self):
        self.secret_id = 'AKIDsVR2MOKpRWKJ1TiYBYeUEm45oHj1rxd5'  # 替换为用户的secret_id
        self.secret_key = 'PXOtnQmtVrA2nKZU8WfYopHVxFNFqEhl'
        self.config = CosConfig(Region='ap-guangzhou' , SecretId=self.secret_id, SecretKey=self.secret_key, Token=None)  # 获取配置对象
        self.client = CosS3Client(self.config)
        self.bucket='sprocomm-8011-1258754892'

    def upfile(self,m_path,d):
        for root, dirs, files in os.walk(m_path):  # 遍历上传文件
            for file in files:
                n_file = m_path + '\\' + file  # 完整路径
                print('Url:'+n_file)
                response = self.client.upload_file(  # 上传文件
                    Bucket=self.bucket,
                    LocalFilePath=n_file,
                    Key=d+'/'+file,
                    PartSize=10,
                    MAXThread=10
                )
                #print(response[])
                #print(self.get_url(d,file))
    #def get_url(self,d,file):
        #url=self.client.get_presigned_download_url(Bucket=self.bucket,Key=d+'/'+file)
        #return url

    # def main(self):
    #     #print(get_Sn(file_path))
    #     file_path =os.path.dirname(os.path.abspath(__file__))+'\\'+'test'
    #     for root, dirs ,files in os.walk(file_path):
    #         for d in dirs:#文件夹名
    #             print('SN ：'+ d)
    #             m_path = root+'\\'+d#上传为路径
    #             time.sleep(1)
    #             self.upfile(m_path,d)
    #         return dirs

# if __name__ == '__main__':
#     c = Upfile()
#     print(type(c.main()))
#     secret_id = 'AKIDsVR2MOKpRWKJ1TiYBYeUEm45oHj1rxd5'  # 替换为用户的secret_id
#     secret_key = 'PXOtnQmtVrA2nKZU8WfYopHVxFNFqEhl'
    # def getfilename(self):
    #     for root, dirs, files in os.walk(file_path):
    #         #dirs返回文件夹名字
    #         #files返回文件名字
    #         array = dirs
    #         if array:
    #             return array





