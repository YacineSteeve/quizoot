# from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .validators import SchemaValidator
import json


validator = SchemaValidator()


@csrf_exempt
def index(request):
    if request.method == "POST":
        # Get data from request body and parse it as json
        data = request.body
        json_data = json.loads(data.decode("utf8"))

        # Validate data
        validator.validate(json_data)

        # Do something else
        print("Valid question :", json_data)

    return HttpResponse("Done !")
