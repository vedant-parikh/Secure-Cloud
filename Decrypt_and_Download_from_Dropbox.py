# Include the Dropbox SDK and required libraries
import dropbox
import checksum
import decryption
import deleteTempFiles
import list_files
from Serializer import JSONSerializer

def decryptFunction():
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

    # Getting the list of files and listing them for the user
    folder_metadata = client.metadata('/encryptedFiles/')
    print 'metadata: ', folder_metadata
    files = list_files.list_files(client)
    print '\n'
    print "Listing dropbox files below..."
    file_hashvalues = JSONSerializer.getFileMap()
    for file in files:
        print file +'  -->  '+ file_hashvalues[file][0]

    # Getting the filename the user wish to download
    final_filename=''
    print "Enter the filename in shown in hash format:"
    file_value =raw_input()

    # Getting the required values from the dictionary
    try:
        privatekey = str(file_hashvalues[file_value][1])
        f, metadata = client.get_file_and_metadata('encryptedFiles/'+file_value)
        out = open('Temp_Files/Encrypted_download.txt', 'wb+')
        out2 = open('Download_Folder/'+str(file_hashvalues[file_value][0]), 'wb+')
        out.write(f.read())
        out.close()
        out = open('Temp_Files/Encrypted_download.txt', 'rb+')
    except:
        print "File Not Found"
        exit()

    # Downloading and decrypting the file.
    decryption.decrypt(out, out2, privatekey)
    out2.close()
    print "Decrypting and Downloading the file from the server..."
    print "Checking checksum of the file for it's integrity..."
    print "file downloaded to Download_Folder"
    print checksum.check(file_value)

    # deleting Temporary Files
    deleteTempFiles.deleteFiles()