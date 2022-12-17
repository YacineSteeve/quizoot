import json

from django.http import HttpResponse

from ..validators import SchemaValidator

validator = SchemaValidator("quizzes")


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
