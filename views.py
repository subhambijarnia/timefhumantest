from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import json
import csv
from timefhuman import timefhuman
import re

class Datetimeissue(APIView):
    def get(self, request, *args, **kwargs):
        data = {"Name": request.query_params.get("Name","")}
        json_string1 = json.dumps(data)
        
        # line split the input & make ready for timefhuman
        field_x = json_string1.split('"')[3]
        
        # this line for replace next to upcoming for week days error resolution
        field = field_x.replace("next","upcoming")
        print(field)
        
        # this code check midnight word in imput string
        re_pattern = "midnight"
        field1 = field.lower()
        qqq = 1
        regex = re.compile(re_pattern)
        for m in regex.finditer(field1):
            qqq = m.group()

        # main code "timefhuman" this pass the time
        json_string99=[]
        try:
            qwe = timefhuman(field)
            json_string2 = json.dumps(qwe, sort_keys=True, default=str)
            print(json_string2)
        
            # check total number of timeset
            x = json_string2.split(',')
            num = len(x)
            print(num)
        
            count = 0
            # if midnight word in the input so pass 00:00:00
    
            if (re_pattern == qqq):
                while(count < num):
                    asd = json_string2.split(',')[count]
                    print(asd)
                    yy = str(asd).split('"')[1]
                    print(yy)
                    date = str(yy).split(' ')[0]
                    time = str(yy).split(' ')[1]
                    year = date.split('-')[0]
                    month = str(yy).split('-')[1]
                    day = date.split('-')[2]
                    count = count+1
                
                    data1 ={"Time" : time, "Day" : day, "Month" : month, "Year" : year}
                    print(data1)
                    json_string99.append(json.dumps(data1))
                
            # if midnight word not in input so set condition for 00:00:00 for diff condition
            else:
                while(count < num):
                    asd = json_string2.split(',')[count]
                    print(asd)
                    yy = str(asd).split('"')[1]
                    print(yy)
                    date = str(yy).split(' ')[0]
                    time = str(yy).split(' ')[1]
                    year = date.split('-')[0]
                    month = str(yy).split('-')[1]
                    day = date.split('-')[2]
                    count = count+1

                    if (time == "00:00:00"):
                        data1 ={"Day" : day, "Month" : month, "Year" : year}
                        print(data1)
                        json_string99.append(json.dumps(data1))
                    else:
                        data1 ={"Time" : time, "Day" : day, "Month" : month, "Year" : year}
                        print(data1)
                        json_string99.append(json.dumps(data1))
        
        except:
            error = "Sorry, We are not accept this format of time. Please try again. Thank You "
            json_string99.append(json.dumps(error))

        new_data = {
            "entries":[
                {
                "template_type":"message",
                "message":json_string99,
                "full_width" : False,
                "text_color" : '#fff',
                "background_color":  '#000',
                "script": 'console.log("hello")',
                }
            ]
        }
        return JsonResponse(new_data, status=201)
