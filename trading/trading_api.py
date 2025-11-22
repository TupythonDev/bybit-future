from pybit.unified_trading import HTTP

class TradingApi():
    """
    Cria uma sessão HTTP autenticada para a API da Bybit.

    :param api_key: (str) Sua API key gerada na conta da Bybit.
    :param api_secret: (str) Sua API secret gerada na conta da Bybit.
    :param testnet: (bool) Se True, usa o ambiente sandbox/testnet da Bybit.
    """
    def __init__(self, api_key:str, api_secret:str, demo:bool=False) -> None:
        self._session = HTTP(
            testnet=False,
            api_key=api_key,
            api_secret=api_secret,
            demo=demo
        )

    # ============================================================
    # Obtém saldo atual em USDT
    # ============================================================
    def get_usdt_balance(self) -> float:
        """
        Obtém o saldo em USDT da conta (Unified Account).

        :param session: Sessão HTTP criada pelo get_session().
        :return: (float) valor do saldo em USDT.
        """
        try:
            coins = self._session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]["coin"]
            for coin in coins:
                if coin["coin"] == "USDT":
                    return float(coin["walletBalance"])
            raise RuntimeError("USDT balance not found")
        except Exception as e:
            raise RuntimeError(f"Erro ao obter saldo: {e}") from e

    # ============================================================
    # Obtém preço atual de um símbolo
    # ============================================================
    def _get_symbol_price(self, symbol: str):
        """
        Obtém o último preço (lastPrice) de um instrumento de trading.

        :param session: Sessão HTTP autenticada.
        :param symbol: (str) Nome do instrumento, ex: "BTCUSDT".
        :return: (float) último preço (MARKET LAST PRICE).
        """
        try:
            return float(
                self._session.get_tickers(category="linear", symbol=symbol)["result"]["list"][0]["lastPrice"]
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao obter preço de {symbol}: {e}") from e

    # ============================================================
    # Retorna informações do símbolo, como tick_size e qty_step.
    # ============================================================
    def _get_symbol_info(self, symbol:str):
        """
        Retorna informações sobre o símbolo, como tick_size e qty_step.
        
        :param symbol: (str) Nome do ativo, ex: "ETHUSDT".
        :return: (tuple) (tick_size, qty_step) em formato int.
        """
        try:
            symbol_info = self._session.get_instruments_info(category="linear", symbol=symbol)["result"]["list"][0]
            tick_size = 4
            qty_step = str(symbol_info["lotSizeFilter"]["qtyStep"]).split(".")
            qty_step = len(qty_step[1]) if len(qty_step) > 1 else 0
            return tick_size, qty_step
        except Exception as e:
            raise RuntimeError(f"Erro ao obter informações do símbolo {symbol}: {e}") from e

    # ============================================================
    # Calcula tamanho do lote, TP e SL com base em % da conta
    # ============================================================
    def _get_tp_sl(self, percent: float, symbol: str, profit: float, max_loss: float, side: str, leverage:int=1):
        """
        Calcula a quantidade de contratos, preço de Take Profit (TP) e Stop Loss (SL).

        :param session: Sessão HTTP autenticada.
        :param percent: (float) Percentual do saldo disponível que será usado na ordem (ex: 5 → 5% do capital).
        :param symbol: (str) Nome do ativo, ex: "ETHUSDT".
        :param profit: (float) Percentual de lucro desejado (ex: 2 → Take Profit em +2%).
        :param max_loss: (float) Percentual máximo de perda permitido (ex: 1 → Stop Loss em -1%).
        :param side: (str) Direção da ordem, valores aceitos: "Buy" ou "Sell".
        :return: (tuple) (qty, tp, sl) em formato string.
        """
        try:
            balance = self.get_usdt_balance()
            price = self._get_symbol_price(symbol)
            tick_size, qty_step = self._get_symbol_info(symbol)
            qty = round(float((balance * leverage * (percent) / 100) / price), qty_step)
            if qty_step == 0:
                qty = int(qty)
            if side.lower() == "buy":
                tp = round(price * (1 + profit / 100), tick_size)
                sl = round(price * (1 - max_loss / 100), tick_size)
            else:  # "Sell"
                tp = round(price * (1 - profit / 100), tick_size)
                sl = round(price * (1 + max_loss / 100), tick_size)

            return str(qty), str(tp), str(sl), str(round(qty*price, 2))
        except Exception as e:
            raise RuntimeError(f"Erro ao calcular TP e SL: {e}") from e

    # ============================================================
    # Define alavancagem de um par
    # ============================================================
    def set_leverage(self, leverage: str, symbol: str):
        """
        Define a alavancagem (isolada ou cruzada depende da config da conta).

        :param session: Sessão HTTP autenticada.
        :param leverage: (str) Alavancagem para posições Long/Short (ex: "5").
        :param symbol: (str) Nome do ativo, ex: "BTCUSDT".
        :return: resposta da API (dict).
        """
        try:
            return self._session.set_leverage(
                category="linear",
                symbol=symbol,
                buyLeverage=leverage,
                sellLeverage=leverage
            )
        except Exception as e:
            if "not modified" in str(e).lower():
                return
            raise RuntimeError(f"Erro ao setar alavancagem: {e}") from e

    # ============================================================
    # Ativa modo de posição (hedge ou one-way)
    # ============================================================
    def switch_position_mode(self, mode: int):
        """
        Altera o modo de posição:
        - 0 = One-Way Mode (apenas uma direção por vez para o par).
        - 3 = Hedge Mode (permite ter Buy e Sell do mesmo par ao mesmo tempo).

        :param session: Sessão HTTP autenticada.
        :param mode: (int) 0 ou 3.
        :return: resposta da API (dict).
        """
        try:
            return self._session.switch_position_mode(
                category="linear",
                mode=mode
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao mudar modo de posição: {e}") from e

    # ============================================================
    # Coloca ordem com TP/SL automáticos calculados
    # ============================================================
    def place_order_tp_sl(self, percent: float, symbol: str,
                        profit: float, max_loss: float, side: str, leverage: int = 1):
        """
        Cria uma ordem no mercado/limit com Take Profit (TP) e Stop Loss (SL).

        :param session: Sessão HTTP autenticada.
        :param percent: (float) Percentual do saldo a ser usado (ex: 10 → usar 10% da carteira).
        :param symbol: (str) Ativo, ex: "BTCUSDT".
        :param profit: (float) Percentual desejado para Take Profit.
        :param max_loss: (float) Percentual de Stop Loss.
        :param side: (str) "Buy" para Long / "Sell" para Short.
        :param order_type: (str) Tipo de ordem: "Market" ou "Limit".
        :return: resposta da API (dict).
        """
        try:
            qty, tp, sl, amount = self._get_tp_sl(percent, symbol, profit, max_loss, side, leverage)
            self._session.place_order(
                    category="linear",
                    symbol=symbol,
                    side=side,
                    orderType="Market",   # "Market" ou "Limit"
                    qty=qty,
                    takeProfit=tp,
                    stopLoss=sl,
                    timeInForce="GoodTillCancel",
                )
            return {
                "qty": qty,
                "tp": tp,
                "sl": sl,
                "order_amount": amount
            }
        except Exception as e:
            raise RuntimeError(f"Erro ao colocar ordem: {e}") from e

    # ============================================================
    # Retorna informações sobre posições abertas
    # ============================================================
    def get_positions(self) -> dict:
        """
        Retrieves the current positions.

        :return: A dictionary containing position details.
        """
        try:
            orders = self._session.get_positions(category="linear", settleCoin="USDT")["result"]["list"]
            # print(orders)
            positions = {}
            for order in orders:
                if order["side"]:
                    positions[order["symbol"]] = {
                    "leverage": order["leverage"],
                    "side": order["side"],
                    "avg_price": order["avgPrice"],
                    "liq_price": order["liqPrice"],
                    "tp": order["takeProfit"],
                    "sl": order["stopLoss"],
                    "qty": order["size"],
                    "value": order["positionValue"],
                    "rPnL": order["curRealisedPnl"],
                    "uPnL": order["unrealisedPnl"],
                    "market_price": order["markPrice"]
                }
            if not positions:
                return "Não há posições abertas."
            return positions
        except Exception as e:
            raise RuntimeError(f"Erro ao obter posições: {e}") from e
    # ============================================================
    # Fecha ordem/posição aberta existente
    # ============================================================
    def close_order(self, symbol:str):
        """
        Fecha posição atual de um determinado símbolo enviando ordem oposta.

        :param session: Sessão HTTP autenticada.
        :param symbol: (str) Ativo, ex: "BTCUSDT".
        :return: resposta da API (dict).
        """
        try:
            order = self.get_positions().get(symbol, False)
            if not order:
                raise ValueError(f"Não há posição para {symbol}")
            order_side = "Buy" if order["side"].lower() == "sell" else "Sell"
            self._session.place_order(
                category="linear",
                symbol=symbol,
                side=order_side,
                orderType="Market",
                qty=order["qty"],
                reduceOnly=True
            )
            return order
        except Exception as e:
            raise RuntimeError(f"Erro ao fechar ordem: {e}") from e

    # ============================================================
    # Muda o take profit e stop loss para uma posição aberta
    # ============================================================
    def change_tp_sl(self, symbol: str, tp: str | None, sl: str | None) -> dict:
        """
        Modifies the take profit (TP) and stop loss (SL) for an open position.
        :param symbol: (str) Asset, e.g., "BTCUSDT".
        :param tp: (float) New take profit value.
        :param sl: (float) New stop loss value.
        :return: resposta da API (dict).
        """
        try:
            return self._session.set_trading_stop(
                category="linear",
                symbol=symbol,
                takeProfit=tp,
                stopLoss=sl,
                tpTriggerBy="LastPrice",
                slTriggerBy="LastPrice"
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao configurar TP e SL: {e}") from e
