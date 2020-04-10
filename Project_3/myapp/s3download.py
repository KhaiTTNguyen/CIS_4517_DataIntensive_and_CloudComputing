import os
import boto3

bucket_name = 'image-processing-khai-nguyen'
s3_file_path= 'directory-in-s3/remote_file.txt'
save_as = 'local_file_name.txt'

s3 = boto3.client('s3')
s3.download_file(bucket_name , s3_file_path, save_as)

# Prints out contents of file
with open(save_as) as f:
print(f.read())