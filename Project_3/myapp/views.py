from django.shortcuts import render
from django.template import RequestContext
from myapp.forms import UploadFileForm
from PIL import Image, ImageOps,ImageFilter
import io
import pathlib
import boto3
from myapp.s3upload import upload_to_s3_bucket_path

def applyfilter(filename, preset):
	inputfile = '/home/ec2-user/Documents/CIS_4517/Project_3/Test/Testing_AWS/media/' + filename

	f=filename.split('.')
	outputfilename = f[0] + '-out.jpg'

	outputfile = '/home/ec2-user/Documents/CIS_4517/Project_3/Test/Testing_AWS/myapp/static/output/' + outputfilename

	im = Image.open(pathlib.Path(inputfile))
	if preset=='gray':
		im = ImageOps.grayscale(im)

	if preset=='edge':
		im = ImageOps.grayscale(im)
		im = im.filter(ImageFilter.FIND_EDGES)

	if preset=='poster':
		im = ImageOps.posterize(im,3)

	if preset=='solar':
		im = ImageOps.solarize(im, threshold=80) 

	if preset=='blur':
		im = im.filter(ImageFilter.BLUR)
	
	if preset=='sepia':
		sepia = []
		r, g, b = (239, 224, 185)
		for i in range(255):
			sepia.extend((r*i//255, g*i//255, b*i//255))
		im = im.convert("L")
		im.putpalette(sepia)
		im = im.convert("RGB")

	im.save(outputfile)
	return outputfilename

def handle_uploaded_file(f,preset):
	uploadfilename='media/' + f.name
	with open(uploadfilename, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	outputfilename=applyfilter(f.name, preset)
	return outputfilename


def home(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
				preset=request.POST['preset']
				outputfilename = handle_uploaded_file(request.FILES['myfilefield'],preset)
				context_instance=RequestContext(request)
			
				# # upload to S3
				# path = '/home/ec2-user/Documents/CIS_4517/Project_3/Test/Testing_AWS/myapp/static/output/'

				# #conn =  boto3.resource('s3')
				# upload_to_s3_bucket_path('khai-nguyen-bucket', path, outputfilename)

				return render(request,'myapp/process.html',{'outputfilename': outputfilename}, context_instance )
	else:
		form = UploadFileForm() 
		context_instance=RequestContext(request)
		return render(request,'myapp/index.html',{'form': form}, context_instance)


def process(request):
	return render(request,'myapp/process.html', {})


