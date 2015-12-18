#Including the required libraries and dropbox SDK

import datetime
import os
import time
import dropbox
import checksum
import deleteTempFiles
import encryption
from Serializer import JSONSerializer

def encryptFunction():
    # Get your app key and secret from the Dropbox developer's console
    app_key = ''
    app_secret = ''

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()

    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)

    # Linking your dropbox account
    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    datestring = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print "Enter File Name:"
    fname = raw_input()
    try:
        checksum_value = checksum.md5('Upload_Folder/'+fname)
    except:
        print "file not found"
        exit()
    # generating random cryptographic private key

    privatekey=''
    ran=map(ord,os.urandom(10))
    for num in range(len(ran)):
        privatekey = privatekey+(str(ran[num]))
    print "Generating Private Key.....\n"

    # Serializing the filename, its hash value, private key and checksum to JSON
    hash_value=str(hash(fname+st))
    file_hashvalues = JSONSerializer.getFileMap()
    file_hashvalues[hash_value+'.txt']=[fname,privatekey,checksum_value, datestring]
    JSONSerializer.saveFileMap(file_hashvalues)

    # Encrypting the File
    try:
        in_file = open('Upload_Folder/'+fname, 'rb+')
    except:
        print "File Not Found."
        exit()
    out_file=open('Temp_Files/out_file.txt','wb+')
    encryption.encrypt(in_file, out_file, privatekey)
    print "Encrypting your file....\n"
    out_file.close()
    out_file= open('Temp_Files/out_file.txt', 'rb+')

    # Uploading the files to DropBox
    print "Uploading Encryted File to Dropbox....\n"
    response = client.put_file('/encryptedFiles/'+hash_value+'.txt', out_file)
    print 'Uploaded! '

    # deleting Temporary Files
    deleteTempFiles.deleteFiles()