from flask_restful.inputs import date, datetime_from_rfc822
from flask_restful import Resource, Api, abort, reqparse,fields,marshal_with
from flask import Flask, request, send_from_directory,render_template,session
import werkzeug
import os
import json
import base64
app = Flask(__name__)
api = Api(app)
api_get_args = reqparse.RequestParser()
api_get_args.add_argument('root',type=str)
api_get_args.add_argument('folder',type=str,required=False,help='start date required')
api_post_args = reqparse.RequestParser()
api_post_args.add_argument('file', type=str)
api_post_args.add_argument('file_name', type=str)


# api_get_args.add_argument('elements',type=str,required=False,help='list of elements you want')
# api_get_args.add_argument('just_col',type=str,required=False,help='list of elements you want')

# resource_field = {
#     'root':fields.Raw
# }
class drive(Resource):
    def __init__(self,kwargs) -> None:
        self.root = kwargs['root']  + ':\\CLOUT_STORAGE'
    

    def get_folder(self,folder):
        return f'{self.root}\\{folder}'

    def subfolder(self,folder=None):
        if folder is None:
            folder = self.root
        else:
            folder = self.get_folder(folder)
        return os.listdir(
            folder
        )
    
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
            os.remove(file_name)
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
        get_args = api_get_args.parse_args()
        post_args = api_post_args.parse_args()
        d = drive(get_args)
        return d.read(get_args['folder'],post_args['file_name'])
    
    def post(self):
        get_args = api_get_args.parse_args()
        post_args = api_post_args.parse_args()
        d = drive(get_args)
        return d.download(get_args['folder'],post_args['file_name'],post_args['file'])
    

    def delete(self):
        get_args = api_get_args.parse_args()
        post_args = api_post_args.parse_args()
        d = drive(get_args)
        direct = d.get_folder(get_args['folder'])
        return d.delete(get_args['folder'],post_args['file_name'])

class navigation(Resource):
    def get(self):
        args = api_get_args.parse_args()
        d = drive(args)
        return {
            'files':d.subfolder(args['folder'])
        }


api.add_resource(clout,'/clout')
api.add_resource(navigation,'/navigation')

if __name__ == '__main__':
    # app.run(port=5000,host=DOMAIN,debug=True)
    app.run(host='0.0.0.0', port=5000)
    
