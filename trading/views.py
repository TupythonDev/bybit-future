# pylint: disable=no-member, unreachable

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.request_methods import post
from .models import TradingUser, Leverage
from .trading_api import TradingApi

def get_balance_view(request):
    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "Only GET allowed"}, status=405)

    users = TradingUser.objects.all()
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)

        try:
            balance = session.get_usdt_balance()

            result.append({
                "id": user.id,
                "username": user.user.username,   # pega username do User
                "is_active": user.is_active,
                "demo": user.demo,
                "saldo": balance,
            })
        except Exception as e:
            result.append({
                "id": user.id,
                "username": user.user.username,
                "is_active": user.is_active,
                "demo": user.demo,
                "error": str(e)
            })

    return JsonResponse({
        "status": "completed",
        "results": result,
        "total_users": len(users),
        "successful_orders": len([r for r in result if not "error" in r])
    })

@csrf_exempt
def place_order_view(request):
    wanted_keys = ["percent", "symbol", "profit", "max_loss", "side"]
    percent, symbol, profit, max_loss, side = post(request, wanted_keys)
    users = TradingUser.objects.filter(is_active=True)
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)
        try:
            leverage = Leverage.objects.get(user=user.user, symbol=symbol)
            order = session.place_order_tp_sl(percent, symbol, profit, max_loss, side, leverage.leverage)
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": order
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
def close_order_view(request):
    wanted_keys = ["symbol"]
    symbol = post(request, wanted_keys)[0]

    users = TradingUser.objects.filter(is_active=True)
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)
        try:
            order = session.close_order(symbol=symbol)
            order["PnL"] = order.pop("uPnL")
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": "Order closed successfully.",
                "details": order
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

    wanted_keys = ["mode"]
    mode = post(request, wanted_keys)

    users = TradingUser.objects.filter(is_active=True)
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)
        try:
            switched = session.switch_position_mode(mode=mode)
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": f"Position mode switched successfully to {"One-Way Mode" if mode == 0 else "Hedge Mode"}",
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
    wanted_keys = ["leverage", "symbol"]
    leverage, symbol = post(request, wanted_keys)

    users = TradingUser.objects.all()
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)
        try:
            session.set_leverage(leverage=leverage, symbol=symbol)
            Leverage.objects.update_or_create(
                user = user.user,
                symbol = symbol,
                defaults = {"leverage": leverage}
            )
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": f"Leverage successfully set to {leverage} for symbol {symbol}",
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
def update_tp_sl_view(request):
    wanted_keys = ["symbol", "tp", "sl"]
    symbol, tp, sl = post(request, wanted_keys)

    users = TradingUser.objects.filter(is_active=True)
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)
        try:
            session.change_tp_sl(symbol=symbol, tp=tp, sl=sl)
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": f"TP/SL successfully updated to TP: {tp}, SL: {sl} for symbol {symbol}",
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

def get_positions_view(request):
    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "Only GET allowed"}, status=405)

    users = TradingUser.objects.all()
    result = []

    for user in users:
        session = TradingApi(user.api_key, user.api_secret, user.demo)
        try:
            position = session.get_positions()
            result.append({
                "user": user.user.username,
                "status": "success",
                "message": position
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
