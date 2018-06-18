import os

public_key_file_path = './_config/public_key'
private_key_file_path = './_config/private_key'

def get_public_key():
    if os.path.isfile(public_key_file_path):
        fw = open(public_key_file_path, 'r')
        content = fw.read().strip();
        print(content)
        fw.close();
        return content

def get_private_key():
    if os.path.isfile(private_key_file_path):
        fw = open(private_key_file_path, 'r')
        content = fw.read().strip();
        print(content)
        fw.close();
        return content
