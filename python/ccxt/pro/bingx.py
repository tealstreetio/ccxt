# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import AuthenticationError


class bingx(ccxt.async_support.bingx):

    def describe(self):
        return self.deep_extend(super(bingx, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': False,
                'watchMyTrades': False,
                'watchOHLCV': False,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchTrades': True,
                'watchPosition': None,
            },
            'urls': {
                'api': {
                    'ws': 'wss://ws-market-swap.we-api.com/ws',
                    'ws2': 'wss://open-api-swap.bingx.com/swap-market',
                },
            },
            'options': {
                'spot': {
                    'timeframes': {
                        '1m': '1m',
                        '3m': '3m',
                        '5m': '5m',
                        '15m': '15m',
                        '30m': '30m',
                        '1h': '1h',
                        '2h': '2h',
                        '4h': '4h',
                        '6h': '6h',
                        '12h': '12h',
                        '1d': '1d',
                        '1w': '1w',
                        '1M': '1M',
                    },
                },
                'contract': {
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
                        '1d': 'D',
                        '1w': 'W',
                        '1M': 'M',
                    },
                },
            },
            'streaming': {
                'ping': self.ping,
                'keepAlive': 20000,
            },
            'exceptions': {
                'ws': {
                    'exact': {
                    },
                },
            },
        })

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return requestId

    def clean_params(self, params):
        params = self.omit(params, ['type', 'subType', 'settle', 'defaultSettle', 'unifiedMargin'])
        return params

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        see https://bingx-exchange.github.io/docs/v5/websocket/public/orderbook
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return.
        :param dict params: extra parameters specific to the bingx api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']
        params = self.clean_params(params)
        messageHash = 'orderbook' + ':' + symbol
        if limit is None:
            limit = 100
        else:
            if (limit != 5) and (limit != 10) and (limit != 20) and (limit != 50) and (limit != 100):
                raise BadRequest(self.id + ' watchOrderBook() can only use limit 1, 50, 200 and 500.')
        topics = ['market.depth.' + market['id'] + '.step0.level' + str(limit)]
        orderbook = await self.watch_topics(url, messageHash, topics, params)
        return orderbook.limit()

    def handle_order_book(self, client, message):
        data = self.safe_value(message, 'data', {})
        dataType = self.safe_value(message, 'dataType', '')
        parts = dataType.split('.')
        marketId = self.safe_string(parts, 2)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        latestTrade = self.safe_value(data, 'latestTrade', {})
        timestamp = self.safe_integer(latestTrade, 'rawTs')
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            orderbook = self.order_book()
        asks = self.safe_value(data, 'asks', [])
        bids = self.safe_value(data, 'bids', [])
        self.handle_deltas(orderbook['asks'], asks)
        self.handle_deltas(orderbook['bids'], bids)
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        messageHash = 'orderbook' + ':' + symbol
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        bidAsk = self.parse_bid_ask(delta, 'price', 'volume')
        bookside.storeArray(bidAsk)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        watches information on multiple trades made in a market
        see https://bingx-exchange.github.io/docs/v5/websocket/public/trade
        :param str symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bingx api endpoint
        :returns [dict]: a list of [order structures]{@link https://docs.ccxt.com/#/?id=order-structure
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']
        params = self.clean_params(params)
        messageHash = 'trade:' + symbol
        topic = 'market.trade.detail.' + market['id']
        trades = await self.watch_topics(url, messageHash, [topic], params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        # since BingX always returns duplicate set of klines via ws, and we are not sending since from
        # ts client, emulate it
        tradesSince = None
        if self.options['tradesSince'] is not None:
            tradesSince = self.options['tradesSince']
        newTrades = self.filter_by_since_limit(trades, tradesSince, limit, 'timestamp', True)
        self.options = self.extend(self.options, {'tradesSince': self.milliseconds() - 0})
        return newTrades

    def handle_trades(self, client, message):
        #
        #     {
        #         "topic": "publicTrade.BTCUSDT",
        #         "type": "snapshot",
        #         "ts": 1672304486868,
        #         "data": [
        #             {
        #                 "T": 1672304486865,
        #                 "s": "BTCUSDT",
        #                 "S": "Buy",
        #                 "v": "0.001",
        #                 "p": "16578.50",
        #                 "L": "PlusTick",
        #                 "i": "20f43950-d8dd-5b31-9112-a178eb6023af",
        #                 "BT": False
        #             }
        #         ]
        #     }
        #
        data = self.safe_value(message, 'data', {})
        topic = self.safe_string(message, 'dataType')
        trades = []
        if self.is_array(data.trades):
            trades = data.trades.reverse()
        parts = topic.split('.')
        marketId = self.safe_string(parts, 3)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        for j in range(0, len(trades)):
            parsed = self.parse_ws_trade(trades[j], market)
            stored.append(parsed)
        messageHash = 'trade' + ':' + symbol
        client.resolve(stored, messageHash)

    def parse_ws_trade(self, trade, market=None):
        #
        # public
        #    {
        # makerSide
        # "Ask"
        # price
        # "27563.5"
        # time
        # "03:06:43"
        # volume
        # "0.2312"
        #     }
        #
        symbol = market['symbol']
        timestamp = self.safe_integer(trade, 'rawTs')
        id = '' + timestamp
        m = self.safe_value(trade, 'makerSide')
        side = 'Bid' if m else 'Ask'
        price = self.safe_string(trade, 'price')
        amount = self.safe_float(trade, 'volume')
        return self.safe_trade({
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': None,
            'side': side,
            'takerOrMaker': 'taker',
            'price': price,
            'amount': amount * market['contractSize'],
            'cost': None,
            'fee': None,
        }, market)

    def get_private_type(self, url):
        if url.find('spot') >= 0:
            return 'spot'
        elif url.find('v5/private') >= 0:
            return 'unified'
        else:
            return 'usdc'

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on multiple orders made by the user
        see https://bingx-exchange.github.io/docs/v5/websocket/private/order
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bingx api endpoint
        :returns [dict]: a list of [order structures]{@link https://docs.ccxt.com/#/?id=order-structure
        """
        await self.load_markets()
        messageHash = 'orders'
        if symbol is not None:
            symbol = self.symbol(symbol)
            messageHash += ':' + symbol
        url = self.urls['api']['ws']
        await self.authenticate()
        topicsByMarket = {
            'spot': ['order', 'stopOrder'],
            'unified': ['order'],
            'usdc': ['user.openapi.perp.order'],
        }
        topics = self.safe_value(topicsByMarket, self.get_private_type(url))
        orders = await self.watch_topics(url, messageHash, topics, params)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_order(self, client, message, subscription=None):
        #
        #     spot
        #     {
        #         "type": "snapshot",
        #         "topic": "order",
        #         "ts": "1662348310441",
        #         "data": [
        #             {
        #                 "e": "order",
        #                 "E": "1662348310441",
        #                 "s": "BTCUSDT",
        #                 "c": "spotx008",
        #                 "S": "BUY",
        #                 "o": "MARKET_OF_QUOTE",
        #                 "f": "GTC",
        #                 "q": "20",
        #                 "p": "0",
        #                 "X": "CANCELED",
        #                 "i": "1238261807653647872",
        #                 "M": "1238225004531834368",
        #                 "l": "0.001007",
        #                 "z": "0.001007",
        #                 "L": "19842.02",
        #                 "n": "0",
        #                 "N": "BTC",
        #                 "u": True,
        #                 "w": True,
        #                 "m": False,
        #                 "O": "1662348310368",
        #                 "Z": "19.98091414",
        #                 "A": "0",
        #                 "C": False,
        #                 "v": "0",
        #                 "d": "NO_LIQ",
        #                 "t": "2100000000002220938"
        #             }
        #         ]
        #     }
        # unified
        #     {
        #         "id": "5923240c6880ab-c59f-420b-9adb-3639adc9dd90",
        #         "topic": "order",
        #         "creationTime": 1672364262474,
        #         "data": [
        #             {
        #                 "symbol": "ETH-30DEC22-1400-C",
        #                 "orderId": "5cf98598-39a7-459e-97bf-76ca765ee020",
        #                 "side": "Sell",
        #                 "orderType": "Market",
        #                 "cancelType": "UNKNOWN",
        #                 "price": "72.5",
        #                 "qty": "1",
        #                 "orderIv": "",
        #                 "timeInForce": "IOC",
        #                 "orderStatus": "Filled",
        #                 "orderLinkId": "",
        #                 "lastPriceOnCreated": "",
        #                 "reduceOnly": False,
        #                 "leavesQty": "",
        #                 "leavesValue": "",
        #                 "cumExecQty": "1",
        #                 "cumExecValue": "75",
        #                 "avgPrice": "75",
        #                 "blockTradeId": "",
        #                 "positionIdx": 0,
        #                 "cumExecFee": "0.358635",
        #                 "createdTime": "1672364262444",
        #                 "updatedTime": "1672364262457",
        #                 "rejectReason": "EC_NoError",
        #                 "stopOrderType": "",
        #                 "triggerPrice": "",
        #                 "takeProfit": "",
        #                 "stopLoss": "",
        #                 "tpTriggerBy": "",
        #                 "slTriggerBy": "",
        #                 "triggerDirection": 0,
        #                 "triggerBy": "",
        #                 "closeOnTrigger": False,
        #                 "category": "option"
        #             }
        #         ]
        #     }
        #
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        rawOrders = []
        parser = None
        parser = 'parseContractOrder'
        rawOrders = self.safe_value(message, 'data', [])
        rawOrders = self.safe_value(rawOrders, 'result', rawOrders)
        symbols = {}
        for i in range(0, len(rawOrders)):
            parsed = getattr(self, parser)(rawOrders[i])
            symbol = parsed['symbol']
            symbols[symbol] = True
            orders.append(parsed)
        symbolsArray = list(symbols.keys())
        for i in range(0, len(symbolsArray)):
            messageHash = 'orders:' + symbolsArray[i]
            client.resolve(orders, messageHash)
        messageHash = 'orders'
        client.resolve(orders, messageHash)

    async def watch_topics(self, url, messageHash, topics=[], params={}):
        request = {
            'id': '' + self.request_id(),
            'reqType': 'sub',
            'dataType': topics[0],
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def authenticate(self, params={}):
        # self.check_required_credentials()
        # messageHash = 'authenticated'
        # url = self.urls['api']['ws']
        # client = self.client(url)
        # future = self.safe_value(client.subscriptions, messageHash)
        # if future is None:
        #     request = {
        #         'reqType': 'req',
        #         'id': self.uuid(),
        #         'dataType': 'account.user.auth',
        #         'data': {
        #             'token': self.apiKey + '.' + self.secret,
        #             'platformId': '30',
        #         },
        #     }
        #     message = self.extend(request, params)
        #     future = self.watch(url, messageHash, message)
        #     client.subscriptions[messageHash] = future
        # }
        # return future
        time = self.milliseconds()
        lastAuthenticatedTime = self.safe_integer(self.options, 'lastAuthenticatedTime', 0)
        listenKeyRefreshRate = self.safe_integer(self.options, 'listenKeyRefreshRate', 1200000)
        delay = self.sum(listenKeyRefreshRate, 10000)
        if time - lastAuthenticatedTime > delay:
            method = 'swap2OpenApiPrivatePostUserAuthUserDataStream'
            response = await getattr(self, method)(params)
            self.options = self.extend(self.options, {
                'listenKey': self.safe_string(response, 'listenKey'),
                'lastAuthenticatedTime': time,
            })
            self.delay(listenKeyRefreshRate, self.keep_alive_listen_key, params)

    async def keep_alive_listen_key(self, params={}):
        listenKey = self.safe_string(self.options, 'listenKey')
        if listenKey is None:
            # A network error happened: we can't renew a listen key that does not exist.
            return
        method = 'swap2OpenApiPrivatePutUserAuthUserDataStream'
        request = {
            'listenKey': listenKey,
        }
        time = self.milliseconds()
        sendParams = self.omit(params, 'type')
        try:
            await getattr(self, method)(self.extend(request, sendParams))
        except Exception as error:
            url = self.urls['api']['ws2'] + '?' + self.options['listenKey']
            client = self.client(url)
            messageHashes = list(client.futures.keys())
            for i in range(0, len(messageHashes)):
                messageHash = messageHashes[i]
                client.reject(error, messageHash)
            self.options = self.extend(self.options, {
                'listenKey': None,
                'lastAuthenticatedTime': 0,
            })
            return
        self.options = self.extend(self.options, {
            'listenKey': listenKey,
            'lastAuthenticatedTime': time,
        })
        # whether or not to schedule another listenKey keepAlive request
        listenKeyRefreshRate = self.safe_integer(self.options, 'listenKeyRefreshRate', 1200000)
        return self.delay(listenKeyRefreshRate, self.keep_alive_listen_key, params)

    def handle_error_message(self, client, message):
        #
        #   {
        #       success: False,
        #       ret_msg: 'error:invalid op',
        #       conn_id: '5e079fdd-9c7f-404d-9dbf-969d650838b5',
        #       request: {op: '', args: null}
        #   }
        #
        # auth error
        #
        #   {
        #       success: False,
        #       ret_msg: 'error:USVC1111',
        #       conn_id: 'e73770fb-a0dc-45bd-8028-140e20958090',
        #       request: {
        #         op: 'auth',
        #         args: [
        #           '9rFT6uR4uz9Imkw4Wx',
        #           '1653405853543',
        #           '542e71bd85597b4db0290f0ce2d13ed1fd4bb5df3188716c1e9cc69a879f7889'
        #         ]
        #   }
        #
        #   {code: '-10009', desc: 'Invalid period!'}
        #
        code = self.safe_integer(message, 'code')
        try:
            if code != 0:
                feedback = self.id + ' ' + self.json(message)
                raise ExchangeError(feedback)
            success = self.safe_value(message, 'success')
            if success is not None and not success:
                ret_msg = self.safe_string(message, 'ret_msg')
                request = self.safe_value(message, 'request', {})
                op = self.safe_string(request, 'op')
                if op == 'auth':
                    raise AuthenticationError('Authentication failed: ' + ret_msg)
                else:
                    raise ExchangeError(self.id + ' ' + ret_msg)
            return False
        except Exception as error:
            if isinstance(error, AuthenticationError):
                messageHash = 'authenticated'
                client.reject(error, messageHash)
                if messageHash in client.subscriptions:
                    del client.subscriptions[messageHash]
            else:
                client.reject(error)
            return True

    def handle_message(self, client, message):
        # pong
        if message == 'Ping' or self.safe_string(message, 'ping', '') != '':
            return self.send_pong(client, message)
        if message == 'Pong' or self.safe_string(message, 'pong', '') != '':
            return self.handle_pong(client, message)
        if self.handle_error_message(client, message):
            return
        # event = self.safe_string(message, 'event')
        # if event == 'sub':
        #     self.handle_subscription_status(client, message)
        #     return
        # }
        topic = self.safe_string(message, 'dataType', '')
        methods = {
            # 'market.depth.': self.handle_order_book,
            # 'order': self.handle_order,
            # 'stopOrder': self.handle_order,
            # 'trade': self.handle_trades,
            # 'publicTrade': self.handle_trades,
            'market.depth.': self.handle_order_book,
            'market.trade.detail.': self.handle_trades,
            'market.contracts': self.handle_ticker,
            # 'wallet': self.handleBalance,
            # 'outboundAccountInfo': self.handleBalance,
            # 'execution': self.handleMyTrades,
            # 'ticketInfo': self.handleMyTrades,
            # 'user.openapi.perp.trade': self.handleMyTrades,
        }
        keys = list(methods.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            if topic.find(keys[i]) >= 0:
                method = methods[key]
                method(client, message)
                return
        # unified auth acknowledgement
        # type = self.safe_string(message, 'type')
        # if (op == 'auth') or (type == 'AUTH_RESP'):
        #     self.handle_authenticate(client, message)
        # }

    def ping(self, client):
        self.client(self.urls['api']['ws']).send('Ping')
        return {
            'ping': self.uuid(),
            'time': self.iso8601(self.milliseconds()),
        }  # XD

    def send_pong(self, client, message):
        self.client(self.urls['api']['ws']).send('Pong')
        self.client(self.urls['api']['ws']).send(self.json({
            'ping': self.uuid(),
            'time': self.iso8601(self.milliseconds()),
        }))

    def handle_authenticate(self, client, message):
        #
        #    {
        #        success: True,
        #        ret_msg: '',
        #        op: 'auth',
        #        conn_id: 'ce3dpomvha7dha97tvp0-2xh'
        #    }
        #
        success = self.safe_value(message, 'success')
        messageHash = 'authenticated'
        if success:
            client.resolve(message, messageHash)
        else:
            error = AuthenticationError(self.id + ' ' + self.json(message))
            client.reject(error, messageHash)
            if messageHash in client.subscriptions:
                del client.subscriptions[messageHash]
        return message

    def handle_subscription_status(self, client, message):
        #
        #    {
        #        topic: 'kline',
        #        event: 'sub',
        #        params: {
        #          symbol: 'LTCUSDT',
        #          binary: 'false',
        #          klineType: '1m',
        #          symbolName: 'LTCUSDT'
        #        },
        #        code: '0',
        #        msg: 'Success'
        #    }
        #
        return message

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        see https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
        see https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the bybit api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'ticker:' + market['symbol']
        url = self.urls['api']['ws']
        params = self.clean_params(params)
        topics = ['market.contracts']
        return await self.watch_topics(url, messageHash, topics, params)

    def handle_ticker(self, client, message):
        data = self.safe_value(message, 'data', {})
        contracts = self.safe_value(data, 'contracts', [])
        for i in range(0, len(contracts)):
            symbol = None
            parsed = None
            parsed = self.parse_ticker(contracts[i])
            symbol = parsed['symbol']
            timestamp = self.milliseconds() - 0
            parsed['timestamp'] = timestamp
            parsed['datetime'] = self.iso8601(timestamp)
            self.tickers[symbol] = parsed
            messageHash = 'ticker:' + symbol
            client.resolve(self.tickers[symbol], messageHash)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds() - 0
        marketId = self.safe_string(ticker, 'symbol')
        market = self.safe_market(marketId)
        symbol = self.safe_symbol(marketId)
        last = self.safe_string(ticker, 'indexPrice')
        open = self.safe_string(ticker, 'open')
        percentage = self.safe_string(ticker, 'changePercentage')
        # quoteVolume = self.safe_string(ticker, 'volume2')
        # baseVolume = self.safe_string(ticker, 'volume')
        bid = self.safe_string(ticker, 'indexPrice')
        ask = self.safe_string(ticker, 'indexPrice')
        high = self.safe_string(ticker, 'high')
        low = self.safe_string(ticker, 'low')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': high,
            'low': low,
            'bid': bid,
            'bidVolume': self.safe_string_2(ticker, 'bidSize', 'bid1Size'),
            'ask': ask,
            'askVolume': self.safe_string_2(ticker, 'askSize', 'ask1Size'),
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': percentage,
            'average': None,
            'baseVolume': '0',
            'quoteVolume': '0',
            'info': ticker,
        }, market)
