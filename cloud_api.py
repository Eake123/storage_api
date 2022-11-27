import requests
import base64
import json

class Clout_Api:
    def __init__(self,password) -> None:
        self.__sess = requests.Session()
        self.header = {
            'Content-Type':'application/json',
            'PASSWORD':password
        }


    def __url(self,*args,data=None,method='get'):
        url = '' + '/'.join(args)
        if method == 'get':
            r = self.__sess.get(url,data=data,headers=self.header)
        elif method == 'post':
            r = self.__sess.post(url,data,headers=self.header)
        elif method == 'delete':
            r = self.__sess.delete(url,data=data,headers=self.header)
        return r

    def download(self,root,folder,file_name,file):
        with open(file,'rb') as file:
            b = file.read()
            tb = base64.b64encode(b)
            tb_str = tb.decode('utf-8')
        params = {
                'root':root,
                'folder':folder,
                'file_name':file_name,
                'file':tb_str
        }
        return self.__url(
            'clout',
            data=json.dumps(params),
            method='post'
            )
        r = self.__sess.post(
            BASE + 'clout',
            data=json.dumps({
                'root':root,
                'folder':folder,
                'file_name':file_name,
                'file':tb_str
            }),
            headers={'Content-Type':'application/json'}
        )
        return r.json()
    
    def subdirectory(self,root,folder=None):
        data = {
            'root':root,
            'folder':folder
        }
        return self.__url(
            'navigation',
            data=json.dumps(data),
            method='get'
        ).json()
    def delete(self,root,folder,file_name):
        data = {
            'root':root,
            'folder':folder,
            'file_name':file_name,
        }
        return self.__url(
            'clout',
            data=json.dumps(data),
            method='delete'
        ).json()
    def read(self,root,folder,file_name,download_file=None):
        data = {
            'root':root,
            'folder':folder,
            'file_name':file_name,
        }
        if download_file is None:
            r = self.__url(
            'clout',
            data=json.dumps(data),
            method='get'
        ).json()
        else:
            r = self.__url(
            'clout',
            data=json.dumps(data),
            method='get'
            )
            data = r.json()['file'].encode('utf-8')
            data = base64.b64decode(data)
            # print(data)
            with open(download_file,'wb') as file:
                # data = json.loads(data)
                file.write(data)
            r = file_name
        return r
    
    def powershell(self,cmd_str):
        data = {
            'cmd_str':cmd_str
        }
        return self.__url(
            'powershell',
            data=json.dumps(data),
            method='post'
        )
    def cmd(self,cmd_str):
        data = {
            'cmd_str':cmd_str
        }
        return self.__url(
            'cmd',
            data=json.dumps(data),
            method='post'
        )
if __name__ == '__main__':
    c = Clout_Api(password)
    # r = c.download(
    #     'c',
    #     'programs',
    #     'clout.bat',
    # )
    # print(c.subdirectory('c','programs'))
    r = c.cmd(
    )
    # r = c.delete(
    #     'c',
    #     'programs',
    #     'test'
    # )
    # for i in r['files']:
    #     c.delete(
    #         'c',
    #         'misc',
    #         i
    #     )
    # r = c.subdirectory('c','misc')
    print(r)
