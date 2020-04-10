'''
MIT License

Copyright (c) 2019 Arshdeep Bahga and Vijay Madisetti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import boto3
import botocore

# conn = boto.connect_s3(aws_access_key_id='<enter>',
#      aws_secret_access_key='<enter>')

AWS_ACCESS_KEY_ID='ASIASGKH2PPJDOHY7LSJ'
AWS_SECRET_ACCESS_KEY='pZnUwQleHpT62BG5OfEQPdTj6954MPTp83+60mVx'


conn = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def percent_cb(complete, total):
    print ('.')


# def upload_to_aws(local_file, bucket, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
#                       aws_secret_access_key=SECRET_KEY)
#     try:
#         conn.upload_file(local_file, bucket, s3_file)
#         print("Upload Successful")
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False



def upload_to_s3_bucket_path(bucketname, path, filename):
	
	fullkeyname=os.path.join(path,filename)
	conn.upload_file(fullkeyname,bucketname,filename)

	# key = mybucket.new_key(fullkeyname)
	# key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
	#key.make_public(recursive=False)

def upload_to_s3_bucket_root(bucketname, filename):
	mybucket = conn.Bucket(bucketname)

	exists = True
	try:
		conn.meta.client.head_bucket(Bucket=bucketname)
	except botocore.exceptions.ClientError as e:
		# If a client error is thrown, then check that it was a 404 error.
		# If it was a 404 error, then the bucket does not exist.
		error_code = e.response['Error']['Code']
		if error_code == '404':
			exists = False

	mybucket.upload_file(filename, filename)	
	# key = mybucket.new_key(filename)
	# key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)

def getuserfiles(bucketname,username):
	mybucket = conn.get_bucket(bucketname)
	keys = mybucket.list(username)
	totalsize=0.0
	userfiles = {}
	for key in keys:
		value=[]
		#value.append(key.name)
		filename = key.name
		filename=filename.replace(username+'/media/','')
		value.append(key.last_modified)
		keysize = float(key.size)/1000.0
		value.append(str(keysize))
		userfiles[filename]=value
		totalsize = totalsize + float(key.size)
	totalsize = totalsize/1000000.0
	return userfiles,totalsize

def delete_from_s3(bucketname, username,filename):
	mybucket = conn.get_bucket(bucketname)
	mybucket.delete_key(username+'/media/'+filename)

