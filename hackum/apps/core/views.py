from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse

import time
import tempfile
import json
import numpy as np
from threading import Thread
from binascii import a2b_base64
from clarifai.client import ClarifaiApi
from .jqueue import JQueue

from functools import reduce

global queue
global statResult

queue = JQueue()
statResult = JQueue()

def index_view(request):
    return render(request, "index.html", {})

def vidtest_view(request):
    return render(request, "vidtest.html", {})

def api_view(request, tags=""):
    #return HttpResponse("""{"results": [{"local_id": "", "docid_str": "8317466b40dd933e9eb8c72e5ac0bc5b", "docid": 174249718541730833606777867238536952923, "result": {"tag": {"concept_ids": ["ai_Pf2b7clG", "ai_6lhccv44", "ai_dxSG2s86", "ai_TJ9wFfK5", "ai_bBXFkGB1", "ai_VPmHr5bm", "ai_l8TKp2h5", "ai_7WNVdPhm", "ai_86sS08Pw", "ai_8H8gb4Z2", "ai_SVshtN54", "ai_Hq72S9X5", "ai_62K34TR4", "ai_p9bzR7fH", "ai_dngMN46t", "ai_ggQlMG6W", "ai_GkhKcPVj", "ai_2D3NBTV7", "ai_fKppxwrj", "ai_971KsJkn"], "classes": ["indoors", "business", "man", "portrait", "auto racing", "adult", "people", "competition", "wear", "serious", "one", "election", "technology", "education", "fashion", "industry", "airport", "championship", "soccer", "track"], "probs": [0.9916660785675049, 0.970708966255188, 0.9623082876205444, 0.9480817317962646, 0.9227888584136963, 0.9192773699760437, 0.9189565181732178, 0.8990598320960999, 0.8369446992874146, 0.831376314163208, 0.828432559967041, 0.8234387040138245, 0.81510329246521, 0.8128798007965088, 0.8095601797103882, 0.7979507446289062, 0.7976885437965393, 0.7952430248260498, 0.7913222908973694, 0.7839663028717041]}}, "status_code": "OK", "status_msg": "OK"}], "status_msg": "All images in request have completed successfully. ", "meta": {"tag": {"model": "general-v1.3", "config": null, "timestamp": 1475940923.318772}}, "status_code": "OK"}""", content_type='text/json')
    if request.GET.get("time"):
        return HttpResponse(time.time())

    if request.method == "POST":
        file = None
        t0 = time.time()
        if "uri" in request.POST:
            uri_data = request.POST.get("uri")
            b64_data = uri_data.split("data:image/jpeg,base64;")
            if len(b64_data) > 1:
                b64_data = b64_data[1]
                bin_data = a2b_base64(b64_data)
                file = tempfile.TemporaryFile()
                file.write(bin_data)
        elif "file" in request.FILES:
            file = request.FILES["file"]

        if file:
            print(time.time(), "loadAPI")
            clarifai_api = ClarifaiApi()
            # clarifai_api.tag_image_urls(url)
            print(time.time(), "sendAPI")
            if(tags == ""):
                json_resp = clarifai_api.tag(file)
            else:
                json_resp = clarifai_api.tag(file, select_classes=tags)
            queue.push(json_resp)
            print(queue.size())
            print(time.time(), "doneAPI")

            t1 = time.time()

            json_resp["timing"] = [t0, t1]

            return JsonResponse(json_resp)

    return JsonResponse({"error": "InvalidRequest"})

def process_file_b64(b64):
    print(time.time(), "loadAPI")
    clarifai_api = ClarifaiApi()
    print(time.time(), "sendAPI")
    data = {'encoded_data': b64}
    json_resp = clarifai_api._base64_encoded_data_op(data, 'tag')
    print(time.time(), "doneAPI")

    return json_resp

# json object -> Iterator[Tag, Prob]
def getKeywords(data):
    status = data["results"][0]["status_code"]
    if (status == 'OK'):
        tags = data["results"][0]["result"]["tag"]
        return (set(tags["classes"]), dict(zip(tags["classes"], tags["probs"])))
    else:
        print("Warning: Status was not OK")
        return iter(())

# List[Json] -> Map[Key, (Mean, Std)]
def calculate(queue):
    eps = 2
    if(queue.size() > eps):
        mapped = list(map(getKeywords, queue.toList()))
        intersectKeys = reduce(lambda x,y: x & y, map(lambda x: x[0], mapped))
        probsDict = map(lambda k: (k,np.array([l[1][k] for l in mapped])), intersectKeys)
        queue.pop()
        return dict(map(lambda k: (k[0], (np.mean(k[1]), np.std(k[1]))), probsDict))
    else:
        return None

def top():
    global queue
    global statResult
    while(True):
        res = calculate(queue)
        if(res != None):
            statResult.push(res)
            print(res)
        time.sleep(0.05)

calcThread = Thread(target=top)
calcThread.start()
