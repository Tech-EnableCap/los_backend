from flask import Flask,request
from flask_cors import CORS,cross_origin
import urllib
import json
from flask import jsonify
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

app=Flask(__name__)
CORS(app)

tok="1000.4014637be1f083aa61143aaabf4b53b5.d7c9017123981c3444656cd9eb76dd34"

@app.route('/',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form1():
	msg={}
	form1_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Customer_Details';
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Document_Upload_Form';
	#tok="1000.51bcb0ff69349a91457fc15718004786.ec259eaee8b1a643f9587d4ec65a61a8"
	if(request):
		print(request.data)
		req=request.data
		req=json.loads(req)
		if 'uid' in request.headers:
			uid=request.headers['uid'];
			postreq=urllib.request.Request("https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Customer_Details/"+uid,method="PATCH")
		else:
			postreq=urllib.request.Request(form1_url,method="POST")
			postreq1=urllib.request.Request(form2_url,method="POST")
		postreq.add_header('Content-Type','application/json')
		postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
		req=json.dumps(req)
		req=req.encode()
		r=urllib.request.urlopen(postreq,data=req)
		content=r.read()
		content=json.loads(content)
		msg["success"]=content
		postreq1.add_header('Content-Type','application/json')
		postreq1.add_header('Authorization','Zoho-oauthtoken '+tok)
		r=urllib.request.urlopen(postreq1,data=req)
		content=r.read()
		content=json.loads(content)
		msg["success1"]=content
	else:
		msg["error"]="no data"

	return jsonify({"msg":msg})

@app.route('/getUserform1',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def getUserform1():
	msg={}
	form1_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Customer_Details/'
	#tok="1000.51bcb0ff69349a91457fc15718004786.ec259eaee8b1a643f9587d4ec65a61a8"
	if 'uid' in request.headers:
		uid=request.headers['uid'];
		postreq=urllib.request.Request(form1_url+"/"+uid,method="GET")
		postreq.add_header('Content-Type','application/json')
		postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
		r=urllib.request.urlopen(postreq)
		content=r.read()
		content=json.loads(content)
		msg["success"]=content
		print(msg)
	else:
		msg["error"]="no data"
	return jsonify({"msg":msg})

@app.route('/form2',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form2():
	print("jjjjj")
	msg={}
	url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Customer_Details/"
	if(request):
		req=request.data
		req=json.loads(req)
		print(req)
		if 'uid' in request.headers:
			uid=request.headers['uid']
			postreq=urllib.request.Request(url+"/"+uid,method="PATCH")
			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			req=json.dumps(req)
			req=req.encode()
			r=urllib.request.urlopen(postreq,data=req)
			content=r.read()
			content=json.loads(content)
			msg["success"]=content
		else:
			msg["error"]="no header"
	else:
		msg["error"]="no data"

	return jsonify({"msg":msg})

@app.route('/form4',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form4():
	msg={}
	url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Document_Upload_Form_Report/"
	field1="selfie_img"
	field2="pan_card_img"
	field3="aadhar_frnt_img"
	field4="aadhar_back_img"
	if(request):
		image_keys=list(request.files.keys());
		req_files=[]
		for i in image_keys:
			req_files.append(request.files[i])

		if 'uid' in request.headers:
			uid=request.headers['uid']
			urls={
					"image1":url+uid+"/"+field1+"/upload",
				  	"image2":url+uid+"/"+field2+"/upload",
				  	"image3":url+uid+"/"+field3+"/upload",
					"image4":url+uid+"/"+field4+"/upload"
			}

			sorted_urls=[urls[i] for i in image_keys]

			data_list=[]
			for i in req_files:
				data_list.append({"file":i.read()})
				
			header={
				'Authorization':'Zoho-oauthtoken '+tok
			}
			for i in range(len(data_list)):
				requests.post(sorted_urls[i],files=data_list[i],headers=header)

			msg["success"]="successfully uploaded"
			print(msg)
		else:
			msg["error"]="no header"
	else:
		msg["error"]="no data"

	return jsonify({"msg":msg})

@app.route('/getUserdocs',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def get_docs():
	msg={}
	url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Document_Upload_Form_Report/"
	field1="selfie_img"
	field2="pan_card_img"
	field3="aadhar_frnt_img"
	field4="aadhar_back_img"
	try:
		if 'uid' in request.headers:
			uid=request.headers['uid']
			#postreq=urllib.request.Request(url+uid+"/"+field1+"/download",method="GET")
			#postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			#r=urllib.request.urlopen(postreq)
			#content=r.read()
			#content=json.loads(content)
			header={
					'Authorization':'Zoho-oauthtoken '+tok
			}
			url1=url+"/"+uid
			r=requests.get(url1,headers=header)
			msg["success"]=json.loads(r.text)
			print(msg)
		else:
			msg["error"]="no header"

	except Exception as e:
			msg["error"]=str(e)

	return jsonify({"msg":msg})


if __name__=='__main__':
   app.run(host='0.0.0.0',port=5000)