# Created: 
# Last edit: Alex Saurber 06/17/20 11:04 PM
# in order for this to work, you must create credentials for the google drive from which you want to
# pull the file. This is done through the google drive api dashboard. You will only need read-only access.
# Put the credentials.json and token.json files into the same directory as this script
# First run of the script will open your browser to let you log in and verify the credentials. After
# they are verified, keep them and you will not have to authenticate them ever again.

import io
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools

# I don't actually know what this does anymore or if it is even required...this is why you comment as you code
obj = lambda: None
auths = {"auth_host_name":'localhost', 'noauth_local_webserver':'store_true', 'auth_host_port':[8080, 8090], 'logging_level':'ERROR'}
for k, v in auths.items():
    setattr(obj, k, v)
    
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# path to credentials folder. leaving this in the root dir for now
credpath = ''

# authorization boilerplate code
# ask for read only access from the drive api, and get/store credentials
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
store = file.Storage(resource_path(os.path.join(credpath,'token.json')))
creds = store.get()

# The following will give you a link if token.json does not exist, the link allows the user to give this app permission
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(resource_path(os.path.join(credpath,'credentials.json')), SCOPES)
    creds = tools.run_flow(flow, store, obj)

# if you get the shareable link, the link contains this id, replace the file_id below
# example: 
file_id = ''

# next line will show an error because the discovery object doesn't exist exactly until it is created with the google-client API call. trust me it works
request = discovery.build('drive', 'v3', http=creds.authorize(Http())).files().get_media(fileId=file_id)

# figure out where the liveries folder for dcs is. Ex: C:\Users\You\Saved Games\DCS.openbeta\Liveries
filepath = os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'Saved Games','DCS.openbeta','Liveries')
filename = 'examplezip.zip'
fullpath = os.path.join(filepath,filename)

# replace the filename and extension in the first field below
fh = io.FileIO(filename, mode='w')
downloader = MediaIoBaseDownload(fh, request)
done = False

# download the file and close the file handler
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))
fh.close()

# move the zip file - this lets us move it regardless of the drive the script and folder are on.
# other utilities require they be on the same drive
import shutil
shutil.move('examplezip.zip',fullpath)

# zipfile module to unzip the .zip file into the final directory we chose
from zipfile import ZipFile
ZipFile(fullpath).extractall(filepath)

# delete the .zip file
os.unlink(fullpath)