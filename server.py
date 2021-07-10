from flask import Flask,request
from flask_cors import CORS,cross_origin
import urllib
import json
from flask import jsonify
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import datetime
import io
import numpy as np

app=Flask(__name__)
CORS(app)


def reset_token():
	msg={}
	url="https://accounts.zoho.in/oauth/v2/token?refresh_token=1000.c52f98f0b53406b53f31ad282e108231.3126f3a60765551a172ac6bf8ccd0958&client_id=1000.56DQOAOUHX4K674MVBZF4POP66JXUC&client_secret=61d4bf7bde5b49ff2b24a62a9972dbf64cf6a5f413&grant_type=refresh_token"
	try:
		#postreq=urllib.request.Request(url,method="POST")
		r=requests.post(url)
		content=json.loads(r.text)
		#r=urllib.request.urlopen(postreq)
		#content=r.read()
		#content=json.loads(content)
		msg["success"]=content["access_token"]
	except Exception as e:
		msg["error"]=str(e)
	return msg

@app.route('/',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form1():
	msg={}
	form1_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Customer_Details_Table';
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Document_Upload_Form';
	form3_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Loan_Details';
	try:
		if(request):
			#print(request.data)
			req=request.data
			req=json.loads(req)

			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]

			if 'uid' in request.headers:
				uid=request.headers['uid'];
				postreq=urllib.request.Request("https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Customer_Details_Table_Report/"+uid,method="PATCH")
			else:
				postreq=urllib.request.Request(form1_url,method="POST")
				postreq1=urllib.request.Request(form2_url,method="POST")
				postreq2=urllib.request.Request(form3_url,method="POST")
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

			postreq2.add_header('Content-Type','application/json')
			postreq2.add_header('Authorization','Zoho-oauthtoken '+tok)
			r=urllib.request.urlopen(postreq2,data=req)
			content=r.read()
			content=json.loads(content)
			msg["success2"]=content
		else:
			msg["error"]="no data"
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})

@app.route('/getUserform1',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def getUserform1():
	msg={}
	form1_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Customer_Details_Table_Report/'
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details/'
	try:
		if 'uid' in request.headers or 'lid' in request.headers:
		
			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]


			if('uid' in request.headers):
				uid=request.headers['uid']
				postreq=urllib.request.Request(form1_url+"/"+uid,method="GET")
			if('lid' in request.headers):
				lid=request.headers['lid']
				postreq=urllib.request.Request(form2_url+"/"+lid,method="GET")

			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			r=urllib.request.urlopen(postreq)
			content=r.read()
			content=json.loads(content)
			msg["success"]=content
			#print(msg)
		else:
			msg["error"]="no data"
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})

@app.route('/form2',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form2():
	msg={}
	tok=None;
	url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Customer_Details_Table_Report"
	url2="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details"
	try:
		if(request):
			req=request.data
			req=json.loads(req)

			if 'uid' in request.headers or 'lid' in request.headers:

				if "dob" in req["data"]:
					date=datetime.datetime.strptime(req["data"]["dob"],"%d-%b-%Y")
					#print(date)
					if(date>=datetime.datetime.now()):
						msg["date_err"]="invalid dob"
						#print(msg)
						return jsonify({"msg":msg})
					else:
						date_gap=datetime.datetime.now()-date
						if (date_gap.days/365)<18:
							msg["date_err"]="must be 18 years old"
							return jsonify({"msg":msg})

				if 'Course_Tenure' in req["data"] and 'Loan_Tenure' in req["data"] and 'Financing_Requirement' in req["data"] and 'Course_Fee_Amount' in req["data"]:
					if(int(req["data"]["Loan_Tenure"])>int(req["data"]["Course_Tenure"])):
						msg["tenure_err"]="loan tenure must not be greater than course tenure"
						return jsonify({"msg":msg})
					if(int(req["data"]["Financing_Requirement"])>int(req["data"]["Course_Fee_Amount"])):
						msg["amt_err"]="financing required must not be greater than course fee amount"
						return jsonify({"msg":msg})

				if 'month_sal' in req["data"] and 'tot_work_exp' in req["data"] and 'cur_job_yrs' in req["data"]:
					if(int(req["data"]["month_sal"])<=0):
						msg["sal_err"]="please put valid monthly salary amount"
						return jsonify({"msg":msg})
					if(int(float(req["data"]["cur_job_yrs"]))>int(float(req["data"]["tot_work_exp"]))):
						msg["exp_err"]="number of years in current job must be less of equal to total work experience"
						return jsonify({"msg":msg})

				with open("cred.json","r") as cred:
					cred_dict=json.load(cred)
				d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
				updated_time=d+datetime.timedelta(minutes=50)
				cur_time=datetime.datetime.now()
				if(cur_time>updated_time):
					token=reset_token()
					if "success" in token:
						tok=token["success"]
						up_dict={
							"token":tok,
							"time":str(cur_time)
						}
						with open("cred.json","w") as cred:
							json.dump(up_dict,cred)
					else:
						tok=cred_dict["token"]
				else:
					tok=cred_dict["token"]


				if 'uid' in request.headers:
					uid=request.headers['uid']
					postreq=urllib.request.Request(url+"/"+uid,method="PATCH")
					postreq.add_header('Content-Type','application/json')
					postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
					req=json.dumps(req)
					req=req.encode()
					#print(req)
					r=urllib.request.urlopen(postreq,data=req)
					content=r.read()
					content=json.loads(content)
					msg["success"]=content

				if 'lid' in request.headers:
					lid=request.headers['lid']
					postreq1=urllib.request.Request(url2+"/"+lid,method="PATCH")
					postreq1.add_header('Content-Type','application/json')
					postreq1.add_header('Authorization','Zoho-oauthtoken '+tok)
					req=json.dumps(req)
					req=req.encode()
					r1=urllib.request.urlopen(postreq1,data=req)
					content1=r1.read()
					content1=json.loads(content1)
					#print(content1)
					msg["success"]=content1
				
			else:
				msg["error"]="no header"
		else:
			msg["error"]="no data"

	except Exception as e:
		msg["error"]=str(e)


	return jsonify({"msg":msg})

@app.route('/form4',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form4():
	msg={}
	url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Document_Upload_Form_Report/"
	field_type_1=["selfie_img","pan_card_img","aadhar_frnt_img","aadhar_back_img"]
	field_type_2=["doc"+str(i+1) for i in range(20)]
	all_fields=field_type_1+field_type_2
	urls={}
	try:
		if(request):
			image_keys=list(request.files.keys());
			req_files=[]
			for i in image_keys:
				req_files.append(request.files[i])

			print(req_files)

			if 'uid' in request.headers:

				with open("cred.json","r") as cred:
					cred_dict=json.load(cred)
				d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
				updated_time=d+datetime.timedelta(minutes=50)
				cur_time=datetime.datetime.now()
				if(cur_time>updated_time):
					token=reset_token()
					if "success" in token:
						tok=token["success"]
						up_dict={
							"token":tok,
							"time":str(cur_time)
						}
						with open("cred.json","w") as cred:
							json.dump(up_dict,cred)
					else:
						tok=cred_dict["token"]
				else:
					tok=cred_dict["token"]
					
				uid=request.headers['uid']
				for i,j in enumerate(all_fields):
					urls["image"+str(i)]=url+uid+"/"+j+"/upload"

					'''
				urls={
						"image1":url+uid+"/"+field1+"/upload",
					  	"image2":url+uid+"/"+field2+"/upload",
					  	"image3":url+uid+"/"+field3+"/upload",
						"image4":url+uid+"/"+field4+"/upload",
						"image5":url+uid+"/"+field5+"/upload",
						"image6":url+uid+"/"+field6+"/upload",
						"image7":url+uid+"/"+field7+"/upload",
						"image8":url+uid+"/"+field8+"/upload",
						"image9":url+uid+"/"+field9+"/upload",
						"image10":url+uid+"/"+field10+"/upload"

				}
				'''

				sorted_urls=[urls[i] for i in image_keys]

				data_list=[]
				for i in req_files:
					data_list.append({"file":i.read()})
					
				header={
					'Authorization':'Zoho-oauthtoken '+tok
				}

				'''
				img=Image.open(req_files[0])
				img = np.array(img)
				print(img.shape)
				img2=img
				imgg=np.vstack((img,img2))
				print(imgg.shape)
				imm=Image.fromarray(imgg,"RGB")
				buf = io.BytesIO()
				imm.save(buf, format='JPEG')
				byte_im = buf.getvalue()
				r=requests.post(sorted_urls[0],files={"file":byte_im},headers=header)
				'''

				#imm.save('abc.jpg')
				#print(imm)
				#print(imgg.shape)


				#for i in range(len(data_list)):
					#requests.post(sorted_urls[i],files=data_list[i],headers=header)
				

				#print(json.loads(r.text))
				#msg["error"]="successfully uploaded"

				#print(msg)
			else:
				msg["error"]="no header"
		else:
			msg["error"]="no data"

	except Exception as e:
		msg["error"]=str(e)


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

			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]
			
			
			url1=url+"/"+uid
			header={
				'Authorization':'Zoho-oauthtoken '+tok
			}
			r=requests.get(url1,headers=header)
			msg["success"]=json.loads(r.text)
			'''
			if 'description' in msg["success"].keys():
				if msg["success"]["description"]=="INVALID_OAUTHTOKEN":
					tok=reset_token()
					if "success" in tok:
						token=tok["success"]
						header={
								'Authorization':'Zoho-oauthtoken '+token
						}
						r=requests.get(url1,headers=header)
						msg["success"]=json.loads(r.text)
					else:
						msg["error"]=tok["error"]
			'''
		else:
			msg["error"]="no header"

	except Exception as e:
			msg["error"]=str(e)

	return jsonify({"msg":msg})


@app.route('/test',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def test_token():
	with open("cred.json","r") as cred:
		cred_dict=json.load(cred)
	d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
	updated_time=d+datetime.timedelta(minutes=50)
	cur_time=datetime.datetime.now()
	if(cur_time>updated_time):
		token=reset_token()
		if "success" in token:
			tok=token["success"]
		else:
			tok=cred_dict["token"]
		up_dict={
			"token":tok,
			"time":str(cur_time)
		}
		with open("cred.json","w") as cred:
			json.dump(up_dict,cred)

	with open("cred.json","r") as cred:
		cred_dict=json.load(cred)

	return jsonify({"msg":cred_dict})


@app.route('/coappidentification',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form_another():
	msg={}
	form1_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Customer_Details_Table';
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/form/Document_Upload_Form';
	form3_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details';
	try:
		if(request):
			#print(request.data)
			req=request.data
			req=json.loads(req)
			print(req)
			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]

			if 'uid' in request.headers:
				uid=request.headers['uid'];
				postreq=urllib.request.Request("https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Customer_Details_Table_Report/"+uid,method="PATCH")
			else:
				postreq=urllib.request.Request(form1_url,method="POST")
				postreq1=urllib.request.Request(form2_url,method="POST")
				postreq2=urllib.request.Request(form3_url,method="PATCH")

			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			req1=json.dumps(req["content1"])
			req1=req1.encode()
			#print(req["content1"])
			r=urllib.request.urlopen(postreq,data=req1)
			content=r.read()
			content=json.loads(content)
			msg["success"]=content

			postreq1.add_header('Content-Type','application/json')
			postreq1.add_header('Authorization','Zoho-oauthtoken '+tok)
			r=urllib.request.urlopen(postreq1,data=req1)
			content=r.read()
			content=json.loads(content)
			msg["success1"]=content

			postreq2.add_header('Content-Type','application/json')
			postreq2.add_header('Authorization','Zoho-oauthtoken '+tok)
			req2=json.dumps(req["content2"])
			req2=req2.encode()
			r=urllib.request.urlopen(postreq2,data=req2)
			content=r.read()
			content=json.loads(content)
			msg["success2"]=content
		else:
			msg["error"]="no data"
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})


@app.route('/coapppersonal',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def init_form_another_another():
	msg={}
	form1_url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Customer_Details_Table_Report/"
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details';
	try:
		if(request):
			#print(request.data)
			req=request.data
			req=json.loads(req)
			print(req)
			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]

			uid=request.headers['uid'];

			if "dob" in req["content1"]["data"]:
				date=datetime.datetime.strptime(req["content1"]["data"]["dob"],"%d-%b-%Y")
				#print(date)
				if(date>=datetime.datetime.now()):
					msg["date_err"]="invalid dob"
					#print(msg)
					return jsonify({"msg":msg})
				else:
					date_gap=datetime.datetime.now()-date
					if (date_gap.days/365)<18:
						msg["date_err"]="must be 18 years old"
						return jsonify({"msg":msg})

			postreq=urllib.request.Request(form1_url+uid,method="PATCH")
			postreq2=urllib.request.Request(form2_url,method="PATCH")


			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			req1=json.dumps(req["content1"])
			req1=req1.encode()
			#print(req["content1"])
			r=urllib.request.urlopen(postreq,data=req1)
			content=r.read()
			content=json.loads(content)
			msg["success"]=content


			postreq2.add_header('Content-Type','application/json')
			postreq2.add_header('Authorization','Zoho-oauthtoken '+tok)
			req2=json.dumps(req["content2"])
			req2=req2.encode()
			r=urllib.request.urlopen(postreq2,data=req2)
			content=r.read()
			content=json.loads(content)
			msg["success2"]=content
		else:
			msg["error"]="no data"
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})


@app.route('/getUserformcoapp',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def getUserform_another():
	msg={}
	form1_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/Customer_Details_Table_Report/'
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details/'
	try:
		if 'uid' in request.headers or 'lid' in request.headers:

			uid=request.headers['uid']
			lid=request.headers['lid']
		
			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]



			postreq=urllib.request.Request(form1_url+"/"+uid,method="GET")
			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			r=urllib.request.urlopen(postreq)
			content=r.read()
			content=json.loads(content)
			msg["success"]=content


			postreq=urllib.request.Request(form2_url+"/"+lid,method="GET")
			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			r=urllib.request.urlopen(postreq)
			content=r.read()
			content=json.loads(content)
			msg["success2"]=content

			
			#print(msg)
		else:
			msg["error"]="no data"
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})


@app.route('/getloandetails',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def getUserform_loan():
	msg={}
	form2_url='https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details/'
	try:
		if 'lid' in request.headers:

			lid=request.headers['lid']
		
			with open("cred.json","r") as cred:
				cred_dict=json.load(cred)
			d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
			updated_time=d+datetime.timedelta(minutes=50)
			cur_time=datetime.datetime.now()
			if(cur_time>updated_time):
				token=reset_token()
				if "success" in token:
					tok=token["success"]
					up_dict={
						"token":tok,
						"time":str(cur_time)
					}
					with open("cred.json","w") as cred:
						json.dump(up_dict,cred)
				else:
					tok=cred_dict["token"]
			else:
				tok=cred_dict["token"]


			postreq=urllib.request.Request(form2_url+"/"+lid,method="GET")
			postreq.add_header('Content-Type','application/json')
			postreq.add_header('Authorization','Zoho-oauthtoken '+tok)
			r=urllib.request.urlopen(postreq)
			content=r.read()
			content=json.loads(content)
			msg["success"]=content

			
			#print(msg)
		else:
			msg["error"]="no data"
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})


@app.route('/getstatusetails',methods=["GET"])
@cross_origin(origin='*',supports_credentials=True)
def getloanStatus():
	msg={}
	form2_url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details?Loan ID=="
	try:
		lid=request.headers['id']
		print(lid)
		with open("cred.json","r") as cred:
			cred_dict=json.load(cred)
		d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
		updated_time=d+datetime.timedelta(minutes=50)
		cur_time=datetime.datetime.now()
		if(cur_time>updated_time):
			token=reset_token()
			if "success" in token:
				tok=token["success"]
				up_dict={
					"token":tok,
					"time":str(cur_time)
				}
				with open("cred.json","w") as cred:
					json.dump(up_dict,cred)
			else:
				tok=cred_dict["token"]
		else:
			tok=cred_dict["token"]

		header={
			'Authorization':'Zoho-oauthtoken '+tok
		}
		r=requests.get(form2_url+lid,headers=header)
		content=json.loads(r.text)
		msg["success"]=content
		print(msg)

			
			#print(msg)
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})


@app.route('/getapplicant',methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def getapplicantData():
	msg={}
	form1_url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details?Loan ID=="
	form2_url="https://creator.zoho.in/api/v2/tech_enablecap/enablecap-loan-origination-system/report/All_Loan_Details?Applicant Phone="
	try:
		req=request.data
		req=json.loads(req)
		print(req)
		with open("cred.json","r") as cred:
			cred_dict=json.load(cred)
		d=datetime.datetime.strptime(cred_dict["time"],"%Y-%m-%d %H:%M:%S.%f")
		updated_time=d+datetime.timedelta(minutes=50)
		cur_time=datetime.datetime.now()
		if(cur_time>updated_time):
			token=reset_token()
			if "success" in token:
				tok=token["success"]
				up_dict={
					"token":tok,
					"time":str(cur_time)
				}
				with open("cred.json","w") as cred:
					json.dump(up_dict,cred)
			else:
				tok=cred_dict["token"]
		else:
			tok=cred_dict["token"]

		header={
			'Authorization':'Zoho-oauthtoken '+tok
		}
		if(req["data"]["lid"]!=""):
			r=requests.get(form1_url+req["data"]["lid"],headers=header)
		else:
			r=requests.get(form2_url+req["data"]["phone"],headers=header)
		content=json.loads(r.text)
		msg["success"]=content
		print(msg)

			
			#print(msg)
	except Exception as e:
		msg["error"]=str(e)

	return jsonify({"msg":msg})



if __name__=='__main__':
   app.run(host='0.0.0.0',port=5000)