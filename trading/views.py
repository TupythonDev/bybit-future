import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TradingUser
from .trading_api import TradingApi

def get_balance_view(request):
    users = TradingUser.objects.all()
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.testnet)

        try:
            saldo = session.get_usdt_balance()
            # ordens_abertas = get_open_orders(session, category="linear")

            result.append({
                "id": user.id,
                "username": user.user.username,   # pega username do User
                "is_active": user.is_active,
                "testnet": user.testnet,
                "saldo": saldo,
                # "ordens_abertas": ordens_abertas
            })
        except Exception as e:
            result.append({
                "id": user.id,
                "username": user.user.username,
                "is_active": user.is_active,
                "testnet": user.testnet,
                "error": str(e)
            })

    return JsonResponse({
        "status": "completed",
        "results": result,
        "total_users": len(users),
        "successful_orders": len([r for r in result if "error" in r])
    })

@csrf_exempt
def place_order_view(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    try:
        order_info = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    wanted_keys = {"percent", "category", "symbol", "profit", "max_loss", "side"}
    received_keys = set(order_info.keys())

    if not wanted_keys.issubset(received_keys):
        return JsonResponse({
            "status": "error", 
            "message": f"Missing required keys. Received: {received_keys}, Needed: {wanted_keys}"
        }, status=400)

    users = TradingUser.objects.filter(is_active=True)
    result = []

    # ✅ Unpacking com ordem garantida
    chaves_ordenadas = ["percent", "category", "symbol", "profit", "max_loss", "side"]
    percent, category, symbol, profit, max_loss, side = tuple(order_info.get(chave) for chave in chaves_ordenadas)

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.testnet)
        try:
            order = session.place_order_tp_sl(percent, category, symbol, profit, max_loss, side)
            result.append({
                "user_id": user.user.username,
                "status": "success",
                "order": order
            })
        except Exception as e:
            result.append({
                "user_id": user.user.username,
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({
        "status": "completed",
        "results": result,
        "total_users": len(users),
        "successful_orders": len([r for r in result if r["status"] == "success"])
    })

@csrf_exempt
def close_order_view(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)
    try:
        request_info = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"status": "error", "message": f"Invalid JSON: {str(e)}"}, status=400)

    wanted_keys = {"category", "symbol"}
    received_keys = set(request_info.keys())

    if not wanted_keys.issubset(received_keys):
        return JsonResponse({
            "status": "error", 
            "message": f"Missing required keys. Received: {received_keys}, Needed: {wanted_keys}"
        }, status=400)

    users = TradingUser.objects.filter(is_active=True)
    result = []

    # ✅ Unpacking com ordem garantida
    chaves_ordenadas = ["category", "symbol"]
    category, symbol = tuple(request_info.get(chave) for chave in chaves_ordenadas)

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.testnet)
        try:
            order = session.close_order(category=category, symbol=symbol)
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": f"Order closed successfully:{order}"
            })
        except Exception as e:
            result.append({
                "user": user.user.username,
                "status": "error",
                "message": str(e)
            })
    return JsonResponse({
        "status": "completed",
        "results": result,
        "total_users": len(users),
        "successful_orders": len([r for r in result if r["status"] == "success"])
    })

@csrf_exempt
def switch_position_mode_view(request):
    return JsonResponse({"status": "error", "message": "Request desabilitada no momento."}, status=405)
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)
    try:
        request_info = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"status": "error", "message": f"Invalid JSON: {str(e)}"}, status=400)

    wanted_keys = {"category", "mode"}
    received_keys = set(request_info.keys())

    if not wanted_keys.issubset(received_keys):
        return JsonResponse({
            "status": "error", 
            "message": f"Missing required keys. Received: {received_keys}, Needed: {wanted_keys}"
        }, status=400)

    users = TradingUser.objects.filter(is_active=True)
    result = []

    # ✅ Unpacking com ordem garantida
    chaves_ordenadas = ["category", "mode"]
    category, mode = tuple(request_info.get(chave) for chave in chaves_ordenadas)

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.testnet)
        try:
            switched = session.switch_position_mode(category=category, mode=mode)
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": f"Position mode switched successfully to {"One-Way Mode" if mode == 0 else "Hedge Mode"}",
                "api_message": switched
            })
        except Exception as e:
            result.append({
                "user": user.user.username,
                "status": "error",
                "message": str(e)
            })
    return JsonResponse({
        "status": "completed",
        "results": result,
        "total_users": len(users),
        "successful_orders": len([r for r in result if r["status"] == "success"])
    })

@csrf_exempt
def set_leverage_view(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)
    try:
        request_info = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"status": "error", "message": f"Invalid JSON: {str(e)}"}, status=400)

    wanted_keys = {"leverage", "category", "symbol"}
    received_keys = set(request_info.keys())

    if not wanted_keys.issubset(received_keys):
        return JsonResponse({
            "status": "error", 
            "message": f"Missing required keys. Received: {received_keys}, Needed: {wanted_keys}"
        }, status=400)

    users = TradingUser.objects.filter(is_active=True)
    result = []

    # ✅ Unpacking com ordem garantida
    chaves_ordenadas = ["leverage", "category", "symbol"]
    leverage, category, symbol = tuple(request_info.get(chave) for chave in chaves_ordenadas)

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.testnet)
        try:
            new_leverage = session.set_leverage(leverage=leverage, category=category, symbol=symbol)
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": f"Leverage successfully set to {leverage} for symbol {symbol} in category {category}",
                "api_message": new_leverage
            })
        except Exception as e:
            result.append({
                "user": user.user.username,
                "status": "error",
                "message": str(e)
            })
    return JsonResponse({
        "status": "completed",
        "results": result,
        "total_users": len(users),
        "successful_orders": len([r for r in result if r["status"] == "success"])
    })
