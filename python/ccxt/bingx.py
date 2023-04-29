# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.decimal_to_precision import TICK_SIZE


class bingx(Exchange):

    def describe(self):
        return self.deep_extend(super(bingx, self).describe(), {
            'id': 'bingx',
            'name': 'BingX',
            'countries': ['EU'],
            'rateLimit': 100,
            'version': 'v1',
            'verbose': True,
            'pro': True,
            'has': {
                'CORS': True,
                'spot': True,
                'margin': None,
                'swap': False,
                'future': False,
                'option': False,
                'cancelOrder': True,
                'createDepositAddress': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': False,
                'fetchDepositAddresses': False,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchMarkOHLCV': False,
                'fetchOHLCV': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrderBook': True,
                'fetchPositions': True,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'transfer': False,
            },
            'urls': {
                'logo': '',
                'api': {
                    'swap': 'https://api-swap-rest.bingbon.pro/api',
                    'swap2': 'https://open-api.bingx.com',
                },
                'test': {
                },
                'www': 'https://bingx.com/',
                'doc': [
                    'https://bingx-api.github.io/docs',
                ],
                'fees': [
                    'https://support.bingx.com/hc/en-001/articles/360027240173',
                ],
                'referral': '',
            },
            'api': {
                'swap': {
                    'v1': {
                        'public': {
                            'get': {
                                'market/getAllContracts': 1,
                                'market/getLatestPrice': 1,
                                'market/getMarketDepth': 1,
                                'market/getMarketTrades': 1,
                                'market/getLatestFunding': 1,
                                'market/getHistoryFunding': 1,
                                'market/getLatestKline': 1,
                                'market/getHistoryKlines': 1,
                                'market/getOpenPositions': 1,
                                'market/getTicker': 1,
                            },
                            'post': {
                                'common/server/time': 1,
                            },
                        },
                        'private': {
                            'post': {
                                'user/getBalance': 1,
                                'user/getPositions': 1,
                                'user/trade': 1,
                                'user/oneClickClosePosition': 1,
                                'user/oneClickCloseAllPositions': 1,
                                'user/cancelOrder': 1,
                                'user/batchCancelOrders': 1,
                                'user/cancelAll': 1,
                                'user/pendingOrders': 1,
                                'user/pendingStopOrders': 1,
                                'user/queryOrderStatus': 1,
                                'user/setMarginMode': 1,
                                'user/setLeverage': 1,
                                'user/forceOrders': 1,
                                'user/auth/userDataStream': 1,
                            },
                            'put': {
                                'user/auth/userDataStream': 1,
                            },
                        },
                    },
                },
                'swap2': {
                    'openApi': {
                        'public': {
                            'get': {
                                'swap/v2/quote/klines': 1,
                            },
                        },
                        'private': {
                            'get': {
                                'swap/v2/trade/openOrders': 1,
                            },
                            'put': {
                                'user/auth/userDataStream': 1,
                            },
                            'post': {
                                'user/auth/userDataStream': 1,
                                'swap/v2/trade/order': 1,
                            },
                            'delete': {
                                'swap/v2/trade/order': 1,
                            },
                        },
                    },
                },
            },
            'markets': {
                'BTC/EUR': {'id': 'eur', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'btc', 'quoteId': 'eur', 'type': 'spot', 'spot': True},
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': self.parse_number('0.0002'),
                    'taker': self.parse_number('0.0004'),
                },
            },
            'precisionMode': TICK_SIZE,
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'timeframes': {
                '1m': '1',
                '3m': '3',
                '5m': '5',
                '15m': '15',
                '30m': '30',
                '1h': '60',
                '2h': '120',
                '4h': '240',
                '6h': '360',
                '12h': '720',
                '1d': '1D',
                '1w': '1W',
                '1M': '1M',
            },
            'options': {
                'listenKeyRefreshRate': 1200000,  # 20 mins
            },
        })

    def fetch_contract_markets(self, params={}):
        response = self.swapV1PublicGetMarketGetAllContracts(params)
        #
        #     {
        #         "code":0,
        #         "msg":"Success",
        #         "data":{
        #             "contracts":[
        #                 {
        #                     "contractId":"100",
        #                     "symbol":"BTC-USDT",
        #                     "name":"BTC",
        #                     "size":"0.0001",
        #                     "currency":"USDT",
        #                     "asset":"BTC",
        #                     "pricePrecision":2,
        #                     "volumePrecision":4,
        #                     "feeRate":0.0005,
        #                     "tradeMinLimit":1,
        #                     "maxLongLeverage":100,
        #                     "maxShortLeverage":100,
        #                     "status":1
        #                 }
        #             ]
        #         }
        #     }
        #
        result = []
        data = self.safe_value(response, 'data', {})
        contracts = self.safe_value(data, 'contracts', [])
        for i in range(0, len(contracts)):
            market = contracts[i]
            # should we use contract id id?
            # contractId = self.safe_string(market, 'contractId')
            marketId = self.safe_string(market, 'symbol')
            parts = marketId.split('-')
            baseId = self.safe_string(parts, 0)
            quoteId = self.safe_string(parts, 1)
            settleId = self.safe_string(market, 'currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            settle = self.safe_currency_code(settleId)
            symbol = base + '/' + quote + ':' + settle
            status = self.safe_number(market, 'status')
            result.append({
                'id': marketId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'settle': settle,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': settleId,
                'type': 'swap',
                'spot': False,
                'margin': True,
                'swap': True,
                'future': False,
                'option': False,
                'active': status == 1,
                'contract': True,
                'linear': True,
                'inverse': None,
                'contractSize': self.safe_number(market, 'size'),
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.safe_number(market, 'volumePrecision'),
                    'price': self.safe_number(market, 'pricePrecision'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': self.safe_number(market, 'maxLongLeverage'),
                    },
                    'amount': {
                        'min': self.safe_number(market, 'tradeMinLimit'),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for bingx
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        contract = self.fetch_contract_markets(params)
        return contract

    def parse_balance(self, response):
        result = {'info': response}
        data = self.safe_value(response, 'data', {})
        dataAccount = self.safe_value(data, 'account', {})
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            code = currencies[i]
            account = self.account()
            if self.safe_string(dataAccount, 'currency', '') == code:
                account['free'] = self.safe_string(dataAccount, 'availableMArgin')
                account['used'] = self.safe_string(dataAccount, 'usedMargin')
                account['total'] = self.safe_string(dataAccount, 'balance')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the bingx api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        # self.load_markets()
        response = self.swapV1PrivatePostUserGetBalance(params)
        return self.parse_balance(response)

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = self.publicGetDataCurrencyDepth(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'], None, 'bids', 'asks', 'price', 'amount')

    def parse_ticker(self, ticker, market=None):
        #
        # {
        #   "symbol": "BTC-USDT",
        #   "priceChange": "10.00",
        #   "priceChangePercent": "10",
        #   "lastPrice": "5738.23",
        #   "lastVolume": "31.21",
        #   "highPrice": "5938.23",
        #   "lowPrice": "5238.23",
        #   "volume": "23211231.13",
        #   "dayVolume": "213124412412.47",
        #   "openPrice": "5828.32"
        # }
        #
        symbol = self.safe_symbol(None, market)
        timestamp = self.milliseconds()
        baseVolume = self.safe_string(ticker, 'volume')
        last = self.safe_string(ticker, 'lastPrice')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'highPrice'),
            'low': self.safe_string(ticker, 'lowPrice'),
            'bid': self.safe_string(ticker, 'lastPrice'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'lastPrice'),
            'askVolume': None,
            'open': self.safe_string(ticker, 'openPrice'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_string(ticker, 'priceChangePercent'),
            'average': None,
            'baseVolume': baseVolume,
            'info': ticker,
        }, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        ticker = self.swapV1PublicGetMarketGetTicker(self.extend(request, params))
        #
        # {
        #   "symbol": "BTC-USDT",
        #   "priceChange": "10.00",
        #   "priceChangePercent": "10",
        #   "lastPrice": "5738.23",
        #   "lastVolume": "31.21",
        #   "highPrice": "5938.23",
        #   "lowPrice": "5238.23",
        #   "volume": "23211231.13",
        #   "dayVolume": "213124412412.47",
        #   "openPrice": "5828.32"
        # }
        #
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'created_at_int')
        id = self.safe_string(trade, 'uuid')
        market = self.safe_market(None, market)
        side = self.safe_string(trade, 'side')
        price = self.safe_string(trade, 'price')
        amountField = 'traded_' + market['base'].lower()
        amount = self.safe_string(trade, amountField)
        return self.safe_trade({
            'info': trade,
            'id': id,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': None,
        }, market)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        return []
        # """
        #
        #
        # get the list of most recent trades for a particular symbol
        # :param str symbol: unified symbol of the market to fetch trades for
        # :param int|None since: timestamp in ms of the earliest trade to fetch
        # :param int|None limit: the maximum amount of trades to fetch
        # :param dict params: extra parameters specific to the paymium api endpoint
        # :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        # """
        # self.load_markets()
        # market = self.market(symbol)
        # request = {
        #     'currency': market['id'],
        # }
        # response = self.publicGetDataCurrencyTrades(self.extend(request, params))
        # return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'type': self.capitalize(type) + 'Order',
            'currency': market['id'],
            'direction': side,
            'amount': amount,
        }
        if type != 'market':
            request['price'] = price
        response = self.privatePostUserOrders(self.extend(request, params))
        return self.safe_order({
            'info': response,
            'id': response['uuid'],
        }, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bitget api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        idComponents = id.split(':')
        formattedId = idComponents[0]
        request = {
            'symbol': market['id'],
            'orderId': formattedId,
        }
        response = self.swap2OpenApiPrivateDeleteSwapV2TradeOrder(request)
        return self.parse_order(response, market)

    def fetch_positions(self, symbols=None, params={}):
        """
        fetch all open positions
        :param [str]|None symbols: list of unified market symbols
        :param dict params: extra parameters specific to the bybit api endpoint
        :returns [dict]: a list of `position structure <https://docs.ccxt.com/#/?id=position-structure>`
        """
        response = self.swapV1PrivatePostUserGetPositions()
        data = self.safe_value(response, 'data', {})
        positions = self.safe_value(data, 'positions', [])
        result = []
        for i in range(0, len(positions)):
            result.append(self.parse_position(positions[i]))
        return result

    def parse_position(self, position, market=None):
        #
        #
        # {
        #     "positionId": "1650546544279240704",
        #     "symbol": "BTC-USDT",
        #     "currency": "",
        #     "volume": 0.001,
        #     "availableVolume": 0.001,
        #     "positionSide": "short",
        #     "marginMode": "cross",
        #     "avgPrice": 27124.5,
        #     "liquidatedPrice": 0.0,
        #     "margin": 2.9386,
        #     "leverage": 5.0,
        #     "pnlRate": -45.83,
        #     "unrealisedPNL": -2.4863,
        #     "realisedPNL": 0.0126
        # }
        #
        marketId = self.safe_string(position, 'symbol')
        market = self.safe_market(marketId, market)
        timestamp = self.safe_integer(position, 'cTime')
        marginMode = self.safe_string_lower(position, 'marginMode')
        hedged = True
        side = self.safe_string_lower(position, 'positionSide')
        contracts = self.safe_float(position, 'volume') / self.safe_number(market, 'contractSize')
        liquidation = self.safe_number(position, 'liquidatedPrice')
        if side == 'short':
            contracts = -1 * contracts
        if liquidation == 0:
            liquidation = None
        initialMargin = self.safe_number(position, 'margin')
        return {
            'info': position,
            'id': market['symbol'] + ':' + side,
            'symbol': market['symbol'],
            'notional': None,
            'marginMode': marginMode,
            'liquidationPrice': liquidation,
            'entryPrice': self.safe_number(position, 'avgPrice'),
            'unrealizedPnl': self.safe_number(position, 'unrealizedPL'),
            'percentage': None,
            'contracts': contracts,
            'contractSize': self.safe_number(market, 'contractSize'),
            'side': side,
            'hedged': hedged,
            'timestamp': timestamp,
            'markPrice': self.safe_number(position, 'markPrice'),
            'datetime': self.iso8601(timestamp),
            'maintenanceMargin': None,
            'maintenanceMarginPercentage': None,
            'collateral': self.safe_number(position, 'margin'),
            'initialMargin': initialMargin,
            'initialMarginPercentage': None,
            'leverage': self.safe_number(position, 'leverage'),
            'marginRatio': None,
        }

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        see https://bybit-exchange.github.io/docs/v5/market/kline
        see https://bybit-exchange.github.io/docs/v5/market/mark-kline
        see https://bybit-exchange.github.io/docs/v5/market/index-kline
        see https://bybit-exchange.github.io/docs/v5/market/preimum-index-kline
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the bybit api endpoint
        :returns [[int]]: A list of candles ordered, open, high, low, close, volume
        """
        self.check_required_symbol('fetchOHLCV', symbol)
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is None:
            limit = 200  # default is 200 when requested with `since`
        if since is not None:
            request['startTime'] = since
        klineType = self.safe_string(self.timeframes, timeframe, timeframe)
        request['interval'] = timeframe
        if limit is not None:
            # request['limit'] = limit  # max 1000, default 1000
            if klineType == '1':
                request['endTime'] = since + limit * 60 * 1000
            elif klineType == '3':
                request['endTime'] = since + limit * 3 * 60 * 1000
            elif klineType == '5':
                request['endTime'] = since + limit * 5 * 60 * 1000
            elif klineType == '15':
                request['endTime'] = since + limit * 15 * 60 * 1000
            elif klineType == '30':
                request['endTime'] = since + limit * 30 * 60 * 1000
            elif klineType == '60':
                request['endTime'] = since + limit * 60 * 60 * 1000
            elif klineType == '120':
                request['endTime'] = since + limit * 120 * 60 * 1000
            elif klineType == '240':
                request['endTime'] = since + limit * 240 * 60 * 1000
            elif klineType == '360':
                request['endTime'] = since + limit * 360 * 60 * 1000
            elif klineType == '720':
                request['endTime'] = since + limit * 720 * 60 * 1000
            elif klineType == '1D':
                request['endTime'] = since + limit * 24 * 60 * 60 * 1000
            elif klineType == '1W':
                request['endTime'] = since + limit * 7 * 24 * 60 * 60 * 1000
            elif klineType == '1M':
                request['endTime'] = since + limit * 30 * 24 * 60 * 60 * 1000
            else:
                request['endTime'] = since + limit * 60 * 1000
        response = self.swap2OpenApiPublicGetSwapV2QuoteKlines(self.extend(request, params))
        ohlcvs = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(ohlcvs, market, timeframe, since, limit)

    def parse_ohlcvs(self, ohlcvs, market=None, timeframe='1m', since=None, limit=None):
        results = []
        for i in range(0, len(ohlcvs)):
            results.append(self.parse_ohlcv(ohlcvs[i], market))
        sorted = self.sort_by(results, 0)
        tail = (since is None)
        return self.filter_by_since_limit(sorted, since, limit, 0, tail)

    def parse_ohlcv(self, ohlcv, market=None):
        return [
            self.safe_integer(ohlcv, 'time'),  # timestamp
            self.safe_number(ohlcv, 'open'),  # open
            self.safe_number(ohlcv, 'high'),  # high
            self.safe_number(ohlcv, 'low'),  # low
            self.safe_number(ohlcv, 'close'),  # close
            self.safe_number(ohlcv, 'volume'),  # volume
        ]

    def parse_order_status(self, status):
        statuses = {
            'pending': 'open',
            'new': 'open',
        }
        return self.safe_string(statuses, status, status)

    def parse_stop_trigger(self, status):
        statuses = {
            'market_price': 'mark',
            'fill_price': 'last',
            'index_price': 'index',
        }
        return self.safe_string(statuses, status, status)

    def parse_order_type(self, type):
        types = {
            'limit': 'limit',
            'market': 'market',
            'stop_market': 'stop',
            'take_profit_market': 'stop',
            'trigger_limit': 'stopLimit',
            'trigger_market': 'stopLimit',
        }
        return self.safe_string_lower(types, type, type)

    def parse_order(self, order, market=None):
        # {
        #     "code": 0,
        #     "msg": "",
        #     "data": {
        #       "orders": [
        #         {
        #           "symbol": "BTC-USDT",
        #           "orderId": 1651880171474731000,
        #           "side": "SELL",
        #           "positionSide": "LONG",
        #           "type": "TAKE_PROFIT_MARKET",
        #           "origQty": "0.0020",
        #           "price": "0.0",
        #           "executedQty": "0.0000",
        #           "avgPrice": "0.0",
        #           "cumQuote": "0",
        #           "stopPrice": "35000.0",
        #           "profit": "0.0",
        #           "commission": "0.0",
        #           "status": "NEW",
        #           "time": 1682673897986,
        #           "updateTime": 1682673897986
        #         },
        #         {
        #           "symbol": "BTC-USDT",
        #           "orderId": 1651880171445371000,
        #           "side": "SELL",
        #           "positionSide": "LONG",
        #           "type": "STOP_MARKET",
        #           "origQty": "0.0020",
        #           "price": "0.0",
        #           "executedQty": "0.0000",
        #           "avgPrice": "28259.0",
        #           "cumQuote": "0",
        #           "stopPrice": "27000.0",
        #           "profit": "0.0",
        #           "commission": "0.0",
        #           "status": "NEW",
        #           "time": 1682673897979,
        #           "updateTime": 1682673897979
        #         },
        #         {
        #           "symbol": "BTC-USDT",
        #           "orderId": 1651287406772699100,
        #           "side": "BUY",
        #           "positionSide": "LONG",
        #           "type": "LIMIT",
        #           "origQty": "0.0001",
        #           "price": "25000.0",
        #           "executedQty": "0.0000",
        #           "avgPrice": "0.0",
        #           "cumQuote": "0",
        #           "stopPrice": "",
        #           "profit": "0.0",
        #           "commission": "0.0",
        #           "status": "PENDING",
        #           "time": 1682532572000,
        #           "updateTime": 1682532571000
        #         },
        #         {
        #           "symbol": "BTC-USDT",
        #           "orderId": 1651006482122227700,
        #           "side": "BUY",
        #           "positionSide": "LONG",
        #           "type": "LIMIT",
        #           "origQty": "0.0001",
        #           "price": "25000.0",
        #           "executedQty": "0.0000",
        #           "avgPrice": "0.0",
        #           "cumQuote": "0",
        #           "stopPrice": "",
        #           "profit": "0.0",
        #           "commission": "0.0",
        #           "status": "PENDING",
        #           "time": 1682465594000,
        #           "updateTime": 1682465594000
        #         }
        #       ]
        #     }
        #   }
        marketId = self.safe_string(order, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        id = self.safe_string(order, 'orderId')
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'origQty')
        filled = self.safe_string(order, 'executedQty')
        cost = self.safe_string(order, 'executedQty')
        average = self.safe_string(order, 'avgPrice')
        type = self.parse_order_type(self.safe_string_lower(order, 'type'))
        timestamp = self.safe_integer(order, 'time')
        rawStopTrigger = self.safe_string(order, 'stopPrice')
        trigger = self.parse_stop_trigger(rawStopTrigger)
        side = self.safe_string_lower(order, 'side')
        reduce = self.safe_value(order, 'reduceOnly', False)
        close = reduce
        planType = self.safe_string_lower(order, 'type')
        if planType == 'stop_market' or planType == 'take_profit_market':
            reduce = True
            close = True
        if side and side.split('_')[0] == 'close':
            reduce = True
            close = True
        # order type LIMIT, MARKET, STOP_MARKET, TAKE_PROFIT_MARKET, TRIGGER_LIMIT, TRIGGER_MARKET
        # if rawStopTrigger:
        #     if type == 'market':
        #         type = 'stop'
        #     else:
        #         type = 'stopLimit'
        #     }
        # else:
        #     if type == 'market':
        #         type = 'market'
        #     else:
        #         type = 'limit'
        #     }
        # }
        clientOrderId = self.safe_string(order, 'orderId')
        fee = self.safe_string(order, 'comission')
        rawStatus = self.safe_string_lower(order, 'status')
        status = self.parse_order_status(rawStatus)
        lastTradeTimestamp = self.safe_integer(order, 'updateTime')
        timeInForce = self.safe_string(order, 'timeInForce')
        postOnly = timeInForce == 'PostOnly'
        stopPrice = self.safe_number(order, 'stopPrice')
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'timeInForce': 'GTC',
            'postOnly': postOnly,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': fee,
            'trades': None,
            'reduce': reduce,  # TEALSTREET
            'close': close,  # TEALSTREET
            'trigger': trigger,  # TEALSTREET
        }, market)

    def fetch_open_orders_v2(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the bybit api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        response = self.swap2OpenApiPrivateGetSwapV2TradeOpenOrders()
        data = self.safe_value(response, 'data', {})
        orders = self.safe_value(data, 'orders', [])
        result = []
        for i in range(0, len(orders)):
            result.append(self.parse_order(orders[i]))
        return result

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_open_orders_v2(symbol, since, limit, params)

    def sign(self, path, section='public', method='GET', params={}, headers=None, body=None):
        type = section[0]
        version = section[1]
        access = section[2]
        rawPath = path
        url = self.implode_hostname(self.urls['api'][type])
        url += '/' + version + '/' + path
        path = self.implode_params(path, params)
        params = self.omit(params, self.extract_params(path))
        params = self.keysort(params)
        if access == 'private':
            self.check_required_credentials()
            isOpenApi = url.find('/v2/') >= 0
            isUserDataStreamEp = url.find('userDataStream') >= 0
            if isOpenApi or isUserDataStreamEp:
                params = self.extend(params, {
                    'timestamp': self.milliseconds() - 0,
                })
                params = self.keysort(params)
                paramString = self.rawencode(params)
                signature = self.hmac(self.encode(paramString), self.encode(self.secret), hashlib.sha256)
                params = self.extend(params, {
                    'signature': signature,
                })
                headers = {
                    'X-BX-APIKEY': self.apiKey,
                }
            else:
                params = self.extend(params, {
                    'apiKey': self.apiKey,
                    'timestamp': self.milliseconds() - 0,
                })
                params = self.keysort(params)
                # ACTUAL SIGNATURE GENERATION
                paramString = self.rawencode(params)
                originString = method + '/api/' + version + '/' + rawPath + paramString
                signature = self.hmac(self.encode(originString), self.encode(self.secret), hashlib.sha256, 'base64')
                # ACTUAL SIGNATURE GENERATION
                params = self.extend(params, {
                    'sign': signature,
                })
        if params:
            url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            return  # fallback to default error handler
        errorCode = self.safe_integer(response, 'code')
        if errorCode is not None and errorCode > 0:
            raise ExchangeError(self.id + ' ' + self.json(response))
