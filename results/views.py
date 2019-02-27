from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
import re
from django.http import HttpResponse
from django.http import JsonResponse



# Create your views here.

def result(usn,sem):
    result_url = 'http://cbcs.fastvturesults.com/result/'+usn+'/'+sem
    r = requests.get(result_url)

    soup = BeautifulSoup(r.text,"html.parser")

    data1= soup.find('span',{'class':'text-muted'})
    name = data1.text #name

    data2 = soup.find('p',{'class':'card-text pt-1'})
    sgpa = data2.text #sgpa

    sgpa=sgpa[7:]



    sub_name_list = []
    sub_code_list = []
    internal_list = []
    external_list = []
    credits_list = []
    total_list = []

    subject_list = []
    final_result_dict = {}

    time = 0




    #=====================Loop for each subject===================
    for subs in soup.find_all('div',{'class':'card custom-card mt-1 mb-1'}):


        if subs.find('div',{'class','card-body custom-card-body'}):
            u2 = subs.find('div',{'class','card-body custom-card-body'})
        if u2.find('div',{'class','row mb-1 text-center'}):
        	u3 = u2.find('div',{'class','row mb-1 text-center'})
        if u3.find('div',{'class','col-12'}):
        	u4 = u3.find('div',{'class','col-12'})
        if u4:
        	sub_name = u4.contents[1]
        	u5 = u4.contents[0]
        	sub_code = u5.text
        if u2.find('div',{'class','row text-center'}):
        	u6 = u2.find('div',{'class','row text-center'})
        if u6:
        	credits = u6.contents[1]
        	credits1 = credits.contents
        	credits2 = credits1[3] #credits
        	credits2 = re.sub('\s+', '', credits2)

        	internal = u6.contents[3]
        	internal1 = internal.contents
        	internal2 = internal1[3] #internal marks
        	internal2 = re.sub('\s+', '', internal2)

        	external = u6.contents[5]
        	external1 = external.contents
        	external2 = external1[3] #external marks
        	external2 = re.sub('\s+', '', external2)

        	total = u6.contents[7]
        	total1 = total.contents
        	total2 = total1[3] #Total marks
        	total2 = re.sub('\s+', '', total2)


        if u4:
        	sub_name_list.append(sub_name)
        	sub_code_list.append(sub_code)

        if u6:
        	internal_list.append(internal2)
        	external_list.append(external2)
        	credits_list.append(credits2)
        	total_list.append(total2)

        if (time == 0):
        	final_result_dict['name']=name
        	final_result_dict['sgpa']=sgpa

        result_obj = {
        	"sub_code":sub_code,
        	"sub_name":sub_name,
        	"internal":internal2,
        	"external":external2,
        	"credits":credits2,
        	"total":total2
        }
        subject_list.append(result_obj)
        time=time+1

    final_result_dict['subjects']=subject_list
    final_result_json = json.dumps(final_result_dict)
    return(final_result_json)



        
			
#Only for POST request			
@csrf_exempt			
def get_result_post(request):
	if request.method == "GET":
		return JsonResponse({'error':'GET method on allowed on this url'})
	if request.method=="POST":
		usn=request.GET.get('usn','')
		sem=request.GET.get('sem','')
		data = result(usn,sem)
		return HttpResponse(data)



#For GET request on a url
def get_result_get(request,usn,sem):
	if request.method=="GET":
		data = result(usn,sem)
		return HttpResponse(data)



def index(request):
    return render(request,'index.html')
	
	
		

    	
    	
