from app.config import HTTP

def get_usdt_balance(session:HTTP) -> float:
    try:
        return float(
            session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]["coin"][0]["walletBalance"]
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao obter saldo: {e}") from e

def get_symbol_price(category:str, symbol:str, session:HTTP):
    try:
        return float(
            session.get_tickers(category=category, symbol=symbol)["result"]["list"][0]["lastPrice"]
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao obter preço de {symbol}: {e}") from e

def _get_tp_sl(session:HTTP, percent:float, category:str, symbol:str, profit:float, max_loss:float, side:str):
    try:
        balance = get_usdt_balance(session)
        price = get_symbol_price(category, symbol, session)
        qty = int((balance*(percent)/100)/price)
        if side == "Buy":
            tp = round(price * (1 + profit/100), 4)
            sl = round(price * (1 - max_loss/100), 4)
        else:
            tp = round(price * (1 - profit/100), 4)
            sl = round(price * (1 + max_loss/100), 4)
        return str(qty), str(tp), str(sl)
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular TP e SL: {e}") from e

def set_leverage(buy_leverage, sell_leverage, category, symbol, session:HTTP):
    try:
        res = session.set_leverage(
            category=category,
            symbol=symbol,
            buyLeverage=buy_leverage,
            sellLeverage=sell_leverage
        )
        return res
    except Exception as e:
        raise RuntimeError(f"Erro ao setar alavancagem: {e}") from e

def switch_position_mode(category, mode, session:HTTP):
    try:
        res = session.switch_position_mode(
            category=category,
            mode=mode
        )
        return res
    except Exception as e:
        raise RuntimeError(f"Erro ao mudar modo de posição: {e}") from e

def place_order_tp_sl(session:HTTP, order:dict):
    try:
        qty, tp, sl = _get_tp_sl(session, order["percent"], order["category"], order["symbol"], order["profit"], order["max_loss"], order["side"])
        return session.place_order(
            category=order["category"],
            symbol=order["symbol"],
            side=order["side"],
            orderType=order["type"],
            qty=qty,
            takeProfit=tp,
            stopLoss=sl,
            timeInForce="GoodTillCancel"
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao colocar ordem: {e}") from e
