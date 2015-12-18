import hashlib

from Serializer import JSONSerializer


def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

def append_checksum(fname):
    checksum_value=md5(fname)
    f = open(fname,'a')
    f.write('\n')
    f.write(checksum_value)
    f.close()


def check(fkey):
    file_hashvalues = JSONSerializer.getFileMap()
    fname = file_hashvalues[fkey][0]
    checksum_value_1 = md5('Download_Folder/'+fname)
    checksum_value_2 = file_hashvalues[fkey][2]
    if checksum_value_1 == checksum_value_2:
        return "\nChecksum Verified! File not tampered!\n"
    else:
        return "\nChecksum couldn't be verified! Your file is compromised or tampered!\n"
