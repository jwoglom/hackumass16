from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

import tempfile
from binascii import a2b_base64
from clarifai.client import ClarifaiApi

def index_view(request):
    return render(request, "index.html", {})

def vidtest_view(request):
    return render(request, "vidtest.html", {})

def api_view(request):
    if request.method == "POST":
        file = None
        if "uri" in request.POST:
            uri_data = request.POST.get("uri")
            b64_data = uri_data.split("data:image/png,base64;")
            if len(b64_data) > 1:
                b64_data = b64_data[1]
                bin_data = a2b_base64(b64_data)
                file = tempfile.TemporaryFile()
                file.write(bin_data)
        elif "file" in request.FILES:
            file = request.FILES["file"]
        
        if file:
            clarifai_api = ClarifaiApi()
            # clarifai_api.tag_image_urls(url)
            json_resp = clarifai_api.tag(file)

            return JsonResponse(json_resp)

    return JsonResponse({"error": "InvalidRequest"})