# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
import hashlib
from ccxt.base.errors import InvalidNonce
from ccxt.base.errors import AuthenticationError


class blofin(ccxt.async_support.blofin):

    def describe(self):
        return self.deep_extend(super(blofin, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': False,
                'watchMyTrades': False,
                'watchOHLCV': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchTicker': True,
                'watchTickers': True,
                'watchTrades': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://openapi.blofin.com/ws/public',
                        'private': 'wss://openapi.blofin.com/ws/private',
                    },
                },
                'test': {
                    'ws': {
                        'public': 'wss://openapi.blofin.com/ws/public',
                        'private': 'wss://openapi.blofin.com/ws/private',
                    },
                },
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'options': {
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'requestId': {},
            },
            'streaming': {
                'ping': self.ping,
                'keepAlive': 10000,
            },
        })

    def request_id(self, url):
        options = self.safe_value(self.options, 'requestId', {})
        previousValue = self.safe_integer(options, url, 0)
        newValue = self.sum(previousValue, 1)
        self.options['requestId'][url] = newValue
        return newValue

    async def subscribe(self, access, channel, symbol, params={}):
        await self.load_markets()
        url = self.urls['api']['ws'][access]
        messageHash = channel
        firstArgument = {
            'channel': channel,
        }
        if symbol is not None:
            market = self.market(symbol)
            messageHash += ':' + market['id']
            firstArgument['instId'] = market['id']
        request = {
            'op': 'subscribe',
            'args': [
                self.deep_extend(firstArgument, params),
            ],
        }
        return await self.watch(url, messageHash, request, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        symbol = self.symbol(symbol)
        trades = await self.subscribe('public', 'trades', symbol, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        arg = self.safe_value(message, 'arg', {})
        channel = self.safe_string(arg, 'channel')
        data = self.safe_value(message, 'data', [])
        tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
        for i in range(0, len(data)):
            trade = self.parse_trade(data[i])
            symbol = trade['symbol']
            marketId = self.safe_string(trade['info'], 'instId')
            messageHash = channel + ':' + marketId
            stored = self.safe_value(self.trades, symbol)
            if stored is None:
                stored = ArrayCache(tradesLimit)
                self.trades[symbol] = stored
            stored.append(trade)
            client.resolve(stored, messageHash)
        return message

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the okx api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        return await self.subscribe('public', 'tickers', symbol, params)

    def handle_ticker(self, client, message):
        arg = self.safe_value(message, 'arg', {})
        channel = self.safe_string(arg, 'channel')
        data = self.safe_value(message, 'data', [])
        for i in range(0, len(data)):
            ticker = self.parse_ticker(data[i])
            symbol = ticker['symbol']
            marketId = self.safe_string(ticker['info'], 'instId')
            messageHash = channel + ':' + marketId
            self.tickers[symbol] = ticker
            client.resolve(ticker, messageHash)
        return message

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        symbol = self.symbol(symbol)
        interval = self.safe_string(self.timeframes, timeframe, timeframe)
        name = 'candle' + interval
        ohlcv = await self.subscribe('public', name, symbol, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        arg = self.safe_value(message, 'arg', {})
        channel = self.safe_string(arg, 'channel')
        data = self.safe_value(message, 'data', [])
        marketId = self.safe_string(arg, 'instId')
        market = self.safe_market(marketId)
        symbol = market['id']
        interval = channel.replace('candle', '')
        # use a reverse lookup in a static map instead
        timeframe = self.find_timeframe(interval)
        for i in range(0, len(data)):
            parsed = self.parse_ohlcv(data[i], market)
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
            stored = self.safe_value(self.ohlcvs[symbol], timeframe)
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCacheByTimestamp(limit)
                self.ohlcvs[symbol][timeframe] = stored
            stored.append(parsed)
            messageHash = channel + ':' + marketId
            client.resolve(stored, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the okx api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        options = self.safe_value(self.options, 'watchOrderBook', {})
        #
        # bbo-tbt
        # 1. Newly added channel that sends tick-by-tick Level 1 data
        # 2. All API users can subscribe
        # 3. Public depth channel, verification not required
        #
        # books-l2-tbt
        # 1. Only users who're VIP5 and above can subscribe
        # 2. Identity verification required before subscription
        #
        # books50-l2-tbt
        # 1. Only users who're VIP4 and above can subscribe
        # 2. Identity verification required before subscription
        #
        # books
        # 1. All API users can subscribe
        # 2. Public depth channel, verification not required
        #
        # books5
        # 1. All API users can subscribe
        # 2. Public depth channel, verification not required
        # 3. Data feeds will be delivered every 100ms(vs. every 200ms now)
        #
        depth = self.safe_string(options, 'depth', 'books')
        if (depth == 'books-l2-tbt') or (depth == 'books50-l2-tbt'):
            await self.authenticate({'access': 'public'})
        orderbook = await self.subscribe('public', depth, symbol, params)
        return orderbook.limit()

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book_message(self, client, message, orderbook, messageHash):
        asks = self.safe_value(message, 'asks', [])
        bids = self.safe_value(message, 'bids', [])
        storedAsks = orderbook['asks']
        storedBids = orderbook['bids']
        self.handle_deltas(storedAsks, asks)
        self.handle_deltas(storedBids, bids)
        checksum = self.safe_value(self.options, 'checksum', True)
        if checksum:
            asksLength = len(storedAsks)
            bidsLength = len(storedBids)
            payloadArray = []
            for i in range(0, 25):
                if i < bidsLength:
                    payloadArray.append(self.number_to_string(storedBids[i][0]))
                    payloadArray.append(self.number_to_string(storedBids[i][1]))
                if i < asksLength:
                    payloadArray.append(self.number_to_string(storedAsks[i][0]))
                    payloadArray.append(self.number_to_string(storedAsks[i][1]))
            payload = ':'.join(payloadArray)
            responseChecksum = self.safe_integer(message, 'checksum')
            localChecksum = self.crc32(payload, True)
            if responseChecksum != localChecksum:
                error = InvalidNonce(self.id + ' invalid checksum')
                client.reject(error, messageHash)
        timestamp = self.safe_integer(message, 'ts')
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    def handle_order_book(self, client, message):
        arg = self.safe_value(message, 'arg', {})
        channel = self.safe_string(arg, 'channel')
        action = self.safe_string(message, 'action')
        data = self.safe_value(message, 'data', [])
        marketId = self.safe_string(arg, 'instId')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        depths = {
            'bbo-tbt': 1,
            'books': 400,
            'books5': 5,
            'books-l2-tbt': 400,
            'books50-l2-tbt': 50,
        }
        limit = self.safe_integer(depths, channel)
        messageHash = channel + ':' + marketId
        if action == 'snapshot':
            for i in range(0, len(data)):
                update = data[i]
                orderbook = self.order_book({}, limit)
                self.orderbooks[symbol] = orderbook
                orderbook['symbol'] = symbol
                self.handle_order_book_message(client, update, orderbook, messageHash)
                client.resolve(orderbook, messageHash)
        elif action == 'update':
            if symbol in self.orderbooks:
                orderbook = self.orderbooks[symbol]
                for i in range(0, len(data)):
                    update = data[i]
                    self.handle_order_book_message(client, update, orderbook, messageHash)
                    client.resolve(orderbook, messageHash)
        elif (channel == 'books5') or (channel == 'bbo-tbt'):
            orderbook = self.safe_value(self.orderbooks, symbol)
            if orderbook is None:
                orderbook = self.order_book({}, limit)
            self.orderbooks[symbol] = orderbook
            for i in range(0, len(data)):
                update = data[i]
                timestamp = self.safe_integer(update, 'ts')
                snapshot = self.parse_order_book(update, symbol, timestamp, 'bids', 'asks', 0, 1)
                orderbook.reset(snapshot)
                client.resolve(orderbook, messageHash)
        return message

    def check_required_uid(self):
        # checkRequiredUid(error = True) {
        return True
        # if not self.uid:
        #     if error:
        #         raise AuthenticationError(self.id + ' requires `uid` credential')
        #     else:
        #         return False
        #     }
        # }
        # return True

    def authenticate(self, params={}):
        self.check_required_credentials()
        url = self.urls['api']['ws']['private'] + '/' + self.uid
        client = self.client(url)
        messageHash = 'authenticated'
        event = 'auth'
        future = self.safe_value(client.subscriptions, messageHash)
        if future is None:
            ts = str(self.nonce())
            auth = '|' + ts
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256)
            request = {
                'event': event,
                'params': {
                    'apikey': self.apiKey,
                    'sign': signature,
                    'timestamp': ts,
                },
            }
            message = self.extend(request, params)
            future = self.watch(url, messageHash, message)
            client.subscriptions[messageHash] = future
        return future

    async def watch_private(self, messageHash, message, params={}):
        await self.authenticate(params)
        url = self.urls['api']['ws']['private'] + '/' + self.uid
        requestId = self.request_id(url)
        subscribe = {
            'id': requestId,
        }
        request = self.extend(subscribe, message)
        return await self.watch(url, messageHash, request, messageHash, subscribe)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        topic = 'executionreport'
        messageHash = topic
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash += ':' + symbol
        request = {
            'event': 'subscribe',
            'topic': topic,
        }
        message = self.extend(request, params)
        orders = await self.watch_private(messageHash, message)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def parse_ws_order(self, order, market=None):
        return self.parse_order(order, market)

    def handle_order_update(self, client, message):
        #
        #     {
        #         topic: 'executionreport',
        #         ts: 1657515556799,
        #         data: {
        #             symbol: 'PERP_BTC_USDT',
        #             clientOrderId: 0,
        #             orderId: 52952826,
        #             type: 'LIMIT',
        #             side: 'SELL',
        #             quantity: 0.01,
        #             price: 22000,
        #             tradeId: 0,
        #             executedPrice: 0,
        #             executedQuantity: 0,
        #             fee: 0,
        #             feeAsset: 'USDT',
        #             totalExecutedQuantity: 0,
        #             status: 'NEW',
        #             reason: '',
        #             orderTag: 'default',
        #             totalFee: 0,
        #             visible: 0.01,
        #             timestamp: 1657515556799,
        #             reduceOnly: False,
        #             maker: False
        #         }
        #     }
        #
        order = self.safe_value(message, 'data')
        self.handle_order(client, order)

    def handle_order(self, client, message):
        topic = 'executionreport'
        parsed = self.parse_ws_order(message)
        symbol = self.safe_string(parsed, 'symbol')
        orderId = self.safe_string(parsed, 'id')
        if symbol is not None:
            if self.orders is None:
                limit = self.safe_integer(self.options, 'ordersLimit', 1000)
                self.orders = ArrayCacheBySymbolById(limit)
            cachedOrders = self.orders
            orders = self.safe_value(cachedOrders.hashmap, symbol, {})
            order = self.safe_value(orders, orderId)
            if order is not None:
                fee = self.safe_value(order, 'fee')
                if fee is not None:
                    parsed['fee'] = fee
                fees = self.safe_value(order, 'fees')
                if fees is not None:
                    parsed['fees'] = fees
                parsed['trades'] = self.safe_value(order, 'trades')
                parsed['timestamp'] = self.safe_integer(order, 'timestamp')
                parsed['datetime'] = self.safe_string(order, 'datetime')
            cachedOrders.append(parsed)
            client.resolve(self.orders, topic)
            messageHashSymbol = topic + ':' + symbol
            client.resolve(self.orders, messageHashSymbol)

    def handle_message(self, client, message):
        if not self.handle_error_message(client, message):
            return
        #
        #     {event: 'subscribe', arg: {channel: 'tickers', instId: 'BTC-USDT'}}
        #     {event: 'login', msg: '', code: '0'}
        #
        #     {
        #         arg: {channel: 'tickers', instId: 'BTC-USDT'},
        #         data: [
        #             {
        #                 instType: 'SPOT',
        #                 instId: 'BTC-USDT',
        #                 last: '31500.1',
        #                 lastSz: '0.00001754',
        #                 askPx: '31500.1',
        #                 askSz: '0.00998144',
        #                 bidPx: '31500',
        #                 bidSz: '3.05652439',
        #                 open24h: '31697',
        #                 high24h: '32248',
        #                 low24h: '31165.6',
        #                 sodUtc0: '31385.5',
        #                 sodUtc8: '32134.9',
        #                 volCcy24h: '503403597.38138519',
        #                 vol24h: '15937.10781721',
        #                 ts: '1626526618762'
        #             }
        #         ]
        #     }
        #
        #     {event: 'error', msg: 'Illegal request: {"op":"subscribe","args":["spot/ticker:BTC-USDT"]}', code: '60012'}
        #     {event: 'error', msg: "channel:ticker,instId:BTC-USDT doesn't exist", code: '60018'}
        #     {event: 'error', msg: 'Invalid OK_ACCESS_KEY', code: '60005'}
        #     {
        #         event: 'error',
        #         msg: 'Illegal request: {"op":"login","args":["de89b035-b233-44b2-9a13-0ccdd00bda0e","7KUcc8YzQhnxBE3K","1626691289","H57N99mBt5NvW8U19FITrPdOxycAERFMaapQWRqLaSE="]}',
        #         code: '60012'
        #     }
        #
        #
        #
        if message == 'pong':
            return self.handle_pong(client, message)
        # table = self.safe_string(message, 'table')
        # if table is None:
        arg = self.safe_value(message, 'arg', {})
        console.log(message)
        channel = self.safe_string(arg, 'channel')
        methods = {
            'bbo-tbt': self.handle_order_book,  # newly added channel that sends tick-by-tick Level 1 data, all API users can subscribe, public depth channel, verification not required
            'books': self.handle_order_book,  # all API users can subscribe, public depth channel, verification not required
            'books5': self.handle_order_book,  # all API users can subscribe, public depth channel, verification not required, data feeds will be delivered every 100ms(vs. every 200ms now)
            'books50-l2-tbt': self.handle_order_book,  # only users who're VIP4 and above can subscribe, identity verification required before subscription
            'books-l2-tbt': self.handle_order_book,  # only users who're VIP5 and above can subscribe, identity verification required before subscription
            'tickers': self.handle_ticker,
            'trades': self.handle_trades,
        }
        method = self.safe_value(methods, channel)
        if method is None:
            if channel.find('candle') == 0:
                self.handle_ohlcv(client, message)
            else:
                return message
        else:
            return method(client, message)

    def ping(self, client):
        # okex does not support built-in ws protocol-level ping-pong
        # instead it requires custom text-based ping-pong
        return 'ping'

    def handle_pong(self, client, message):
        client.lastPong = self.milliseconds()
        return message

    def handle_error_message(self, client, message):
        #
        #     {event: 'error', msg: 'Illegal request: {"op":"subscribe","args":["spot/ticker:BTC-USDT"]}', code: '60012'}
        #     {event: 'error', msg: "channel:ticker,instId:BTC-USDT doesn't exist", code: '60018'}
        #
        errorCode = self.safe_integer(message, 'code')
        try:
            if errorCode:
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
                messageString = self.safe_value_2(message, 'message', 'msg')
                if messageString is not None:
                    self.throw_broadly_matched_exception(self.exceptions['broad'], messageString, feedback)
        except Exception as e:
            if isinstance(e, AuthenticationError):
                messageHash = 'authenticated'
                client.reject(e, messageHash)
                if messageHash in client.subscriptions:
                    del client.subscriptions[messageHash]
                return False
        return message

    def handle_subscribe(self, client, message):
        #
        #     {
        #         id: '666888',
        #         event: 'subscribe',
        #         success: True,
        #         ts: 1657117712212
        #     }
        #
        return message

    def handle_auth(self, client, message):
        #
        #     {
        #         event: 'auth',
        #         success: True,
        #         ts: 1657463158812
        #     }
        #
        messageHash = 'authenticated'
        success = self.safe_value(message, 'success')
        if success:
            client.resolve(message, messageHash)
        else:
            error = AuthenticationError(self.json(message))
            client.reject(error, messageHash)
            # allows further authentication attempts
            if messageHash in client.subscriptions:
                del client.subscriptions['authenticated']
