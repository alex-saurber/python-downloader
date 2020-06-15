import io
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools
obj = lambda: None
auths = {"auth_host_name":'localhost', 'noauth_local_webserver':'store_true', 'auth_host_port':[8080, 8090], 'logging_level':'ERROR'}
for k, v in auths.items():
    setattr(obj, k, v)
    
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#path to credentials folder. leaving this in the root dir for now
credpath = ''

# authorization boilerplate code
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
store = file.Storage(resource_path(os.path.join(credpath,'token.json')))
creds = store.get()
# The following will give you a link if token.json does not exist, the link allows the user to give this app permission
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(resource_path(os.path.join(credpath,'credentials.json')), SCOPES)
    creds = tools.run_flow(flow, store, obj)


# DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
# if you get the shareable link, the link contains this id, replace the file_id below
file_id = ''

request = discovery.build('drive', 'v3', http=creds.authorize(Http())).files().get_media(fileId=file_id)

filepath = os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'Saved Games','DCS.openbeta','Liveries')
filename = 'examplezip.zip'
fullpath = os.path.join(filepath,filename)


# replace the filename and extension in the first field below
fh = io.FileIO(filename, mode='w')
downloader = MediaIoBaseDownload(fh, request)
done = False

while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))

# print('done')
fh.close()

import shutil
shutil.move('examplezip.zip',fullpath)
# os.chdir(filepath)

from zipfile import ZipFile
ZipFile(fullpath).extractall(filepath)

os.unlink(fullpath)

# package into .exe with pyinstaller in terminal:
# pyinstaller --onefile -w --add-data="/creds/*" gdrivedownloader.py
# pyinstaller -F -w --hidden-import io --hidden-import os --hidden-import sys --hidden-import googleapiclient --hidden-import oauth2client --hidden-import shutil --hidden-import zipfile gdrivedownloader.spec