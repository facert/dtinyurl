import json
import logging
import html
from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.utils import gen_tiny_url, get_tiny_url_by_code
# Create your views here.

url_validator = URLValidator()


@csrf_exempt
def tiny_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        raw_url = data.get("url")
        if not raw_url:
            return JsonResponse({"msg": "url is empty"})
        try:
            url_validator(raw_url)
        except ValidationError as e:
            logging.error(e)
            return JsonResponse({"msg": "url validation error"})
        raw_url = html.escape(raw_url)
        return JsonResponse({"msg": "ok",
                             "data": gen_tiny_url(raw_url)
                             })
    else:
        return render(request, "tiny.html")


def redirect_to(request, tiny_code):
    return redirect(get_tiny_url_by_code(tiny_code))

