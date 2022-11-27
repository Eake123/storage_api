from flask_restful.inputs import date, datetime_from_rfc822
from flask_restful import Resource, Api, abort, reqparse,fields,marshal_with
from flask import Flask, request, send_from_directory,render_template,session
import os
import base64
import shutil
from header_check import check_header
from task_scheduler import powershell,cmd_command
app = Flask(__name__)
api = Api(app)
api_get_args = reqparse.RequestParser()
api_get_args.add_argument('root',type=str)
api_get_args.add_argument('folder',type=str,required=False,help='start date required')
api_post_args = reqparse.RequestParser()
api_post_args.add_argument('file', type=str)
api_post_args.add_argument('file_name', type=str)
api_power_args = reqparse.RequestParser()
api_power_args.add_argument('cmd_str', type=str)
api_cmd_args = reqparse.RequestParser()
api_cmd_args.add_argument('cmd_str', type=str)


class File:
    def __init__(self,location) -> None:
        self.location = location
    
    def response(self):
        return {self.location:
        {
            'directory':self.check_type(),
            'size':self.get_size()
        }
        }

    def get_size(self):
        return os.path.getsize(self.location) / (10 ** 6)
    
    def __str__(self) -> str:
        return self.location

    def check_type(self):
        return os.path.isfile(self.location)




class Directory:
    def __init__(self,location) -> None:
        self.location = location
    

    def response(self):
        return {
            'directory':True,
            'size':self.get_size(),
            'init':recursize_search(self.location)
            }
        
    
    
    def get_size(self):
        return os.path.getsize(self.location)
def recursize_search(location):
    file_list = {}
    for file in os.listdir(location):
        file = f'{location}\\{file}'
        print(file)
        file_list.update(File(file).response())
    
    return file_list

    



class drive:
    def __init__(self,kwargs) -> None:
        self.root = kwargs['root']  + ':\\CLOUT_STORAGE'
    

    def get_folder(self,folder):
        return f'{self.root}\\{folder}'

    def subfolder(self,folder=None):
        if folder is None:
            folder = self.root
        else:
            folder = self.get_folder(folder)
        return recursize_search(folder)
    
    def read(self,folder,file_name):
        folder = self.get_folder(folder)
        file_name = f'{folder}\\{file_name}'
        with open(file_name,'rb') as file:
            b = file.read()
            tb = base64.b64encode(b)
            tb_str = tb.decode('utf-8')
        return {
            'file':tb_str
        }
    def download(self,folder,file_name,data):
        try:
            folder = self.get_folder(folder)
            self.make_dir(folder)
            file_name = f'{folder}\\{file_name}'
            print(file_name)
            data = data.encode('utf-8')
            data = base64.b64decode(data)
            # print(data)
            with open(file_name,'wb') as file:
                # data = json.loads(data)
                file.write(data)
            return {
                'Success':True
            }
        except Exception as e:
            return {
                'Success':False,
                'Error': e
                }
    
    def make_dir(self,folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def delete(self,folder,file_name):
        try:
            folder = self.get_folder(folder)
            file_name = f'{folder}\\{file_name}'
            file = File(file_name)
            if file.check_type():

                os.remove(file_name)
            else:
                shutil.rmtree(file_name)
            return {
                'Success':True
            }
        except Exception as e:
            return {
                'Success':False,
                'Error': e
                }




class clout(Resource):
    # @marshal_with(resource_field)
    def get(self):
        if check_header(request.headers):
            get_args = api_get_args.parse_args()
            post_args = api_post_args.parse_args()
            d = drive(get_args)
            return d.read(get_args['folder'],post_args['file_name'])
        else:
            return {
                'ERROR':'Wrong Credentials'
            }

    
    def post(self):
        if check_header(request.headers):
            get_args = api_get_args.parse_args()
            post_args = api_post_args.parse_args()
            d = drive(get_args)
            return d.download(get_args['folder'],post_args['file_name'],post_args['file'])
        else:
            return {
                'ERROR':'Wrong Credentials'
            }


    def delete(self):
        if check_header(request.headers):
            get_args = api_get_args.parse_args()
            post_args = api_post_args.parse_args()
            d = drive(get_args)
            return d.delete(get_args['folder'],post_args['file_name'])
        else:
            return {
                'ERROR':'Wrong Credentials'
            }

class navigation(Resource):
    def get(self):
        if check_header(request.headers):
            args = api_get_args.parse_args()
            d = drive(args)
            return {
                'files':d.subfolder(args['folder'])
            }

        else:
            return {
                'ERROR':'Wrong Credentials'
            }


class ps(Resource):
    def post(self):
        if check_header(request.headers):
            args = api_power_args.parse_args()
            powershell(args['cmd_str'])
        else:
            return {
                'ERROR':'Wrong Credentials'
            }            


class cmd(Resource):
    def post(self):
        if check_header(request.headers):
            args = api_cmd_args.parse_args()
            cmd_command(args['cmd_str'])
        else:
            return {
                'ERROR':'Wrong Credentials'
            }         




api.add_resource(clout,'/clout')
api.add_resource(navigation,'/navigation')
api.add_resource(ps,'/powershell')
api.add_resource(cmd,'/cmd')
if __name__ == '__main__':
    # app.run(port=5000,host=DOMAIN,debug=True)
    app.run(host='0.0.0.0', port=5000)
    
