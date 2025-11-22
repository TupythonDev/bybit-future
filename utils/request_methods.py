import json
from django.http import JsonResponse

def post(request, wanted_keys):  # ✅ Remove type hint ou use list/tuple
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)
    try:
        request_info = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"status": "error", "message": f"Invalid JSON: {str(e)}"}, status=400)

    received_keys = set(request_info.keys())
    wanted_keys_set = set(wanted_keys)  # ✅ Converte para set apenas para validação

    if not wanted_keys_set.issubset(received_keys):
        return JsonResponse({
            "status": "error",
            "message": f"Missing required keys. Received: {received_keys}, Needed: {wanted_keys_set}"
        }, status=400)

    return tuple(request_info.get(key) for key in wanted_keys)
