def list_files(client, files=None, cursor=None):
     if files is None:
        files = {}
     file_list=[];
     has_more = True

     while has_more:
         result = client.delta(cursor)
         cursor = result['cursor']
         has_more = result['has_more']

     for lowercase_path, metadata in result['entries']:
         if metadata is not None and lowercase_path.startswith('/encryptedfiles/'):
            files[lowercase_path] = metadata
            index = len(lowercase_path.split('/'))-1;
            file_list.append(str(lowercase_path.split('/')[index]))

         else:
     # no metadata indicates a deletion
     # remove if present
            files.pop(lowercase_path, None)

     # in case this was a directory, delete everything under it
     for other in files.keys():
        if other.startswith(lowercase_path + '/'):
            del files[other]

     return file_list