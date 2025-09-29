from pybit.unified_trading import HTTP

class TradingApi():
    """
    Cria uma sessão HTTP autenticada para a API da Bybit.

    :param api_key: (str) Sua API key gerada na conta da Bybit.
    :param api_secret: (str) Sua API secret gerada na conta da Bybit.
    :param testnet: (bool) Se True, usa o ambiente sandbox/testnet da Bybit.
    """
    def __init__(self, api_key:str, api_secret:str, testnet:bool=False) -> None:
        self._session = HTTP(
            testnet="testnet" if testnet else testnet,
            api_key=api_key,
            api_secret=api_secret,
            demo=testnet
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
            return self._session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]["coin"]
            # return float(
            #     self._session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]["coin"]
            # )
        except Exception as e:
            raise RuntimeError(f"Erro ao obter saldo: {e}") from e


    # ============================================================
    # Obtém preço atual de um símbolo
    # ============================================================
    def _get_symbol_price(self, category: str, symbol: str):
        """
        Obtém o último preço (lastPrice) de um instrumento de trading.

        :param session: Sessão HTTP autenticada.
        :param category: (str) Categoria do mercado:\n
                        - "spot"    → mercado à vista
                        - "linear"  → contratos perpétuos USDT
                        - "inverse" → contratos perpétuos inversos
                        - "option"  → opções
        :param symbol: (str) Nome do instrumento, ex: "BTCUSDT".
        :return: (float) último preço (MARKET LAST PRICE).
        """
        try:
            return float(
                self._session.get_tickers(category=category, symbol=symbol)["result"]["list"][0]["lastPrice"]
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao obter preço de {symbol}: {e}") from e


    # ============================================================
    # Calcula tamanho do lote, TP e SL com base em % da conta
    # ============================================================
    def _get_tp_sl(self, percent: float, category: str, symbol: str, profit: float, max_loss: float, side: str):
        """
        Calcula a quantidade de contratos, preço de Take Profit (TP) e Stop Loss (SL).

        :param session: Sessão HTTP autenticada.
        :param percent: (float) Percentual do saldo disponível que será usado na ordem (ex: 5 → 5% do capital).
        :param category: (str) Tipo de mercado (spot/linear/inverse/option).
        :param symbol: (str) Nome do ativo, ex: "ETHUSDT".
        :param profit: (float) Percentual de lucro desejado (ex: 2 → Take Profit em +2%).
        :param max_loss: (float) Percentual máximo de perda permitido (ex: 1 → Stop Loss em -1%).
        :param side: (str) Direção da ordem, valores aceitos: "Buy" ou "Sell".
        :return: (tuple) (qty, tp, sl) em formato string.
        """
        try:
            balance = self.get_usdt_balance()
            price = self._get_symbol_price(category, symbol)
            qty = int((balance * (percent) / 100) / price)

            if side.lower() == "buy":
                tp = round(price * (1 + profit / 100), 4)
                sl = round(price * (1 - max_loss / 100), 4)
            else:  # "Sell"
                tp = round(price * (1 - profit / 100), 4)
                sl = round(price * (1 + max_loss / 100), 4)

            return str(qty), str(tp), str(sl)
        except Exception as e:
            raise RuntimeError(f"Erro ao calcular TP e SL: {e}") from e


    # ============================================================
    # Define alavancagem de um par
    # ============================================================
    def set_leverage(self, leverage: str, category: str, symbol: str):
        """
        Define a alavancagem (isolada ou cruzada depende da config da conta).

        :param session: Sessão HTTP autenticada.
        :param leverage: (str) Alavancagem para posições Long/Short (ex: "5").
        :param category: (str) Tipo de mercado ("linear"/"inverse").
        :param symbol: (str) Nome do ativo, ex: "BTCUSDT".
        :return: resposta da API (dict).
        """
        try:
            return self._session.set_leverage(
                category=category,
                symbol=symbol,
                buyLeverage=leverage,
                sellLeverage=leverage
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao setar alavancagem: {e}") from e


    # ============================================================
    # Ativa modo de posição (hedge ou one-way)
    # ============================================================
    def switch_position_mode(self, category: str, mode: int):
        """
        Altera o modo de posição:
        - 0 = One-Way Mode (apenas uma direção por vez para o par).
        - 3 = Hedge Mode (permite ter Buy e Sell do mesmo par ao mesmo tempo).

        :param session: Sessão HTTP autenticada.
        :param category: (str) Tipo de mercado ("linear"/"inverse").
        :param mode: (int) 0 ou 3.
        :return: resposta da API (dict).
        """
        try:
            return self._session.switch_position_mode(
                category=category,
                mode=mode
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao mudar modo de posição: {e}") from e


    # ============================================================
    # Coloca ordem com TP/SL automáticos calculados
    # ============================================================
    def place_order_tp_sl(self, percent: float, category: str, symbol: str,
                        profit: float, max_loss: float, side: str):
        """
        Cria uma ordem no mercado/limit com Take Profit (TP) e Stop Loss (SL).

        :param session: Sessão HTTP autenticada.
        :param percent: (float) Percentual do saldo a ser usado (ex: 10 → usar 10% da carteira).
        :param category: (str) Tipo de mercado ("linear"/"inverse"/"spot").
        :param symbol: (str) Ativo, ex: "BTCUSDT".
        :param profit: (float) Percentual desejado para Take Profit.
        :param max_loss: (float) Percentual de Stop Loss.
        :param side: (str) "Buy" para Long / "Sell" para Short.
        :param order_type: (str) Tipo de ordem: "Market" ou "Limit".
        :return: resposta da API (dict).
        """
        try:
            qty, tp, sl = self._get_tp_sl(percent, category, symbol, profit, max_loss, side)
            return self._session.place_order(
                category=category,
                symbol=symbol,
                side=side,
                orderType="Market",   # "Market" ou "Limit"
                qty=qty,
                takeProfit=tp,
                stopLoss=sl,
                timeInForce="GoodTillCancel",
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao colocar ordem: {e}") from e


    # ============================================================
    # Fecha ordem/posição aberta existente
    # ============================================================
    def close_order(self, category:str, symbol:str):
        """
        Fecha posição atual de um determinado símbolo enviando ordem oposta.

        :param session: Sessão HTTP autenticada.
        :param category: (str) Tipo de mercado ("linear"/"inverse"/"spot").
        :param symbol: (str) Ativo, ex: "BTCUSDT".
        :return: resposta da API (dict).
        """
        try:
            order = self._session.get_positions(category=category, symbol=symbol)["result"]["list"][0]
            print(order)
            if not order["side"]:
                raise ValueError("Não tem posição aberta para o símbolo especificado.")
        except Exception as e:
            raise RuntimeError(f"Erro ao obter posição: {e}") from e
        order_side = "Buy" if order["side"].lower() == "sell" else "Sell"
        try:
            return self._session.place_order(
                category="linear",
                symbol=symbol,
                side=order_side,
                orderType="Market",
                qty=order["size"],
                reduceOnly=True
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao fechar ordem: {e}") from e
