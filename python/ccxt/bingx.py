# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


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
                'createDepositAddress': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchDepositAddresses': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchMarkOHLCV': False,
                'fetchOpenInterestHistory': False,
                'fetchOrderBook': True,
                'fetchPositions': True,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'transfer': True,
            },
            'urls': {
                'logo': '',
                'api': {
                    'spot': 'https://open-api.bingx.com/openApi/spot',
                    'swap': 'https://api-swap-rest.bingbon.pro/api',
                    'contract': 'https://api.bingbon.com/api/coingecko',
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
                                'user/queryOrderStatus': 1,
                                'user/setMarginMode': 1,
                                'user/setLeverage': 1,
                                'user/forceOrders': 1,
                            },
                        },
                    },
                },
                'contract': {
                    'v1': {
                        'public': {
                            'get': {
                                'derivatives/contracts': 1,
                                'derivatives/orderbook/{ticker_id}': 1,
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
        :param dict params: extra parameters specific to the paymium api endpoint
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

    def create_deposit_address(self, code, params={}):
        """
        create a currency deposit address
        :param str code: unified currency code of the currency for the deposit address
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/#/?id=address-structure>`
        """
        self.load_markets()
        response = self.privatePostUserAddresses(params)
        #
        #     {
        #         "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #         "valid_until": 1620041926,
        #         "currency": "BTC",
        #         "label": "Savings"
        #     }
        #
        return self.parse_deposit_address(response)

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/#/?id=address-structure>`
        """
        self.load_markets()
        request = {
            'address': code,
        }
        response = self.privateGetUserAddressesAddress(self.extend(request, params))
        #
        #     {
        #         "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #         "valid_until": 1620041926,
        #         "currency": "BTC",
        #         "label": "Savings"
        #     }
        #
        return self.parse_deposit_address(response)

    def fetch_deposit_addresses(self, codes=None, params={}):
        """
        fetch deposit addresses for multiple currencies and chain types
        :param [str]|None codes: list of unified currency codes, default is None
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a list of `address structures <https://docs.ccxt.com/#/?id=address-structure>`
        """
        self.load_markets()
        response = self.privateGetUserAddresses(params)
        #
        #     [
        #         {
        #             "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #             "valid_until": 1620041926,
        #             "currency": "BTC",
        #             "label": "Savings"
        #         }
        #     ]
        #
        return self.parse_deposit_addresses(response, codes)

    def parse_deposit_address(self, depositAddress, currency=None):
        #
        #     {
        #         "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #         "valid_until": 1620041926,
        #         "currency": "BTC",
        #         "label": "Savings"
        #     }
        #
        address = self.safe_string(depositAddress, 'address')
        currencyId = self.safe_string(depositAddress, 'currency')
        return {
            'info': depositAddress,
            'currency': self.safe_currency_code(currencyId, currency),
            'address': address,
            'tag': None,
            'network': None,
        }

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
        :param str|None symbol: not used by paymium cancelOrder()
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        request = {
            'uuid': id,
        }
        return self.privateDeleteUserOrdersUuidCancel(self.extend(request, params))

    def transfer(self, code, amount, fromAccount, toAccount, params={}):
        """
        transfer currency internally between wallets on the same account
        :param str code: unified currency code
        :param float amount: amount to transfer
        :param str fromAccount: account to transfer from
        :param str toAccount: account to transfer to
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a `transfer structure <https://docs.ccxt.com/#/?id=transfer-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        if toAccount.find('@') < 0:
            raise ExchangeError(self.id + ' transfer() only allows transfers to an email address')
        if code != 'BTC' and code != 'EUR':
            raise ExchangeError(self.id + ' transfer() only allows BTC or EUR')
        request = {
            'currency': currency['id'],
            'amount': self.currency_to_precision(code, amount),
            'email': toAccount,
            # 'comment': 'a small note explaining the transfer'
        }
        response = self.privatePostUserEmailTransfers(self.extend(request, params))
        #
        #     {
        #         "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #         "type": "Transfer",
        #         "currency": "BTC",
        #         "currency_amount": "string",
        #         "created_at": "2013-10-24T10:34:37.000Z",
        #         "updated_at": "2013-10-24T10:34:37.000Z",
        #         "amount": "1.0",
        #         "state": "executed",
        #         "currency_fee": "0.0",
        #         "btc_fee": "0.0",
        #         "comment": "string",
        #         "traded_btc": "string",
        #         "traded_currency": "string",
        #         "direction": "buy",
        #         "price": "string",
        #         "account_operations": [
        #             {
        #                 "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #                 "amount": "1.0",
        #                 "currency": "BTC",
        #                 "created_at": "2013-10-24T10:34:37.000Z",
        #                 "created_at_int": 1389094259,
        #                 "name": "account_operation",
        #                 "address": "1FPDBXNqSkZMsw1kSkkajcj8berxDQkUoc",
        #                 "tx_hash": "string",
        #                 "is_trading_account": True
        #             }
        #         ]
        #     }
        #
        return self.parse_transfer(response, currency)

    def parse_transfer(self, transfer, currency=None):
        #
        #     {
        #         "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #         "type": "Transfer",
        #         "currency": "BTC",
        #         "currency_amount": "string",
        #         "created_at": "2013-10-24T10:34:37.000Z",
        #         "updated_at": "2013-10-24T10:34:37.000Z",
        #         "amount": "1.0",
        #         "state": "executed",
        #         "currency_fee": "0.0",
        #         "btc_fee": "0.0",
        #         "comment": "string",
        #         "traded_btc": "string",
        #         "traded_currency": "string",
        #         "direction": "buy",
        #         "price": "string",
        #         "account_operations": [
        #             {
        #                 "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #                 "amount": "1.0",
        #                 "currency": "BTC",
        #                 "created_at": "2013-10-24T10:34:37.000Z",
        #                 "created_at_int": 1389094259,
        #                 "name": "account_operation",
        #                 "address": "1FPDBXNqSkZMsw1kSkkajcj8berxDQkUoc",
        #                 "tx_hash": "string",
        #                 "is_trading_account": True
        #             }
        #         ]
        #     }
        #
        currencyId = self.safe_string(transfer, 'currency')
        updatedAt = self.safe_string(transfer, 'updated_at')
        timetstamp = self.parse_date(updatedAt)
        accountOperations = self.safe_value(transfer, 'account_operations')
        firstOperation = self.safe_value(accountOperations, 0, {})
        status = self.safe_string(transfer, 'state')
        return {
            'info': transfer,
            'id': self.safe_string(transfer, 'uuid'),
            'timestamp': timetstamp,
            'datetime': self.iso8601(timetstamp),
            'currency': self.safe_currency_code(currencyId, currency),
            'amount': self.safe_number(transfer, 'amount'),
            'fromAccount': None,
            'toAccount': self.safe_string(firstOperation, 'address'),
            'status': self.parse_transfer_status(status),
        }

    def parse_transfer_status(self, status):
        statuses = {
            'executed': 'ok',
            # what are the other statuses?
        }
        return self.safe_string(statuses, status, status)

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
        # linear swap
        #
        #     {
        #         "positionIdx": 0,
        #         "riskId": "11",
        #         "symbol": "ETHUSDT",
        #         "side": "Buy",
        #         "size": "0.10",
        #         "positionValue": "119.845",
        #         "entryPrice": "1198.45",
        #         "tradeMode": 1,
        #         "autoAddMargin": 0,
        #         "leverage": "4.2",
        #         "positionBalance": "28.58931118",
        #         "liqPrice": "919.10",
        #         "bustPrice": "913.15",
        #         "takeProfit": "0.00",
        #         "stopLoss": "0.00",
        #         "trailingStop": "0.00",
        #         "unrealisedPnl": "0.083",
        #         "createdTime": "1669097244192",
        #         "updatedTime": "1669413126190",
        #         "tpSlMode": "Full",
        #         "riskLimitValue": "900000",
        #         "activePrice": "0.00"
        #     }
        #
        # usdc
        #    {
        #       "symbol":"BTCPERP",
        #       "leverage":"1.00",
        #       "occClosingFee":"0.0000",
        #       "liqPrice":"",
        #       "positionValue":"30.8100",
        #       "takeProfit":"0.0",
        #       "riskId":"10001",
        #       "trailingStop":"0.0000",
        #       "unrealisedPnl":"0.0000",
        #       "createdAt":"1652451795305",
        #       "markPrice":"30809.41",
        #       "cumRealisedPnl":"0.0000",
        #       "positionMM":"0.1541",
        #       "positionIM":"30.8100",
        #       "updatedAt":"1652451795305",
        #       "tpSLMode":"UNKNOWN",
        #       "side":"Buy",
        #       "bustPrice":"",
        #       "deleverageIndicator":"0",
        #       "entryPrice":"30810.0",
        #       "size":"0.001",
        #       "sessionRPL":"0.0000",
        #       "positionStatus":"NORMAL",
        #       "sessionUPL":"-0.0006",
        #       "stopLoss":"0.0",
        #       "orderMargin":"0.0000",
        #       "sessionAvgPrice":"30810.0"
        #    }
        #
        # unified margin
        #
        #     {
        #         "symbol": "ETHUSDT",
        #         "leverage": "10",
        #         "updatedTime": 1657711949945,
        #         "side": "Buy",
        #         "positionValue": "536.92500000",
        #         "takeProfit": "",
        #         "tpslMode": "Full",
        #         "riskId": 11,
        #         "trailingStop": "",
        #         "entryPrice": "1073.85000000",
        #         "unrealisedPnl": "",
        #         "markPrice": "1080.65000000",
        #         "size": "0.5000",
        #         "positionStatus": "normal",
        #         "stopLoss": "",
        #         "cumRealisedPnl": "-0.32215500",
        #         "positionMM": "2.97456450",
        #         "createdTime": 1657711949928,
        #         "positionIdx": 0,
        #         "positionIM": "53.98243950"
        #     }
        #
        # unified account
        #
        #     {
        #         "symbol": "XRPUSDT",
        #         "leverage": "10",
        #         "avgPrice": "0.3615",
        #         "liqPrice": "0.0001",
        #         "riskLimitValue": "200000",
        #         "takeProfit": "",
        #         "positionValue": "36.15",
        #         "tpslMode": "Full",
        #         "riskId": 41,
        #         "trailingStop": "0",
        #         "unrealisedPnl": "-1.83",
        #         "markPrice": "0.3432",
        #         "cumRealisedPnl": "0.48805876",
        #         "positionMM": "0.381021",
        #         "createdTime": "1672121182216",
        #         "positionIdx": 0,
        #         "positionIM": "3.634521",
        #         "updatedTime": "1672279322668",
        #         "side": "Buy",
        #         "bustPrice": "",
        #         "size": "100",
        #         "positionStatus": "Normal",
        #         "stopLoss": "",
        #         "tradeMode": 0
        #     }
        #
        contract = self.safe_string(position, 'symbol')
        market = self.safe_market(contract)
        size = Precise.string_abs(self.safe_string(position, 'volume'))
        side = self.safe_string(position, 'positionSide')
        if side is not None:
            if side == 'Long':
                side = 'long'
            elif side == 'Short':
                side = 'short'
            else:
                side = None
        notional = self.safe_string(position, 'volume')
        realizedPnl = self.omit_zero(self.safe_string(position, 'realisedPNL'))
        unrealisedPnl = self.omit_zero(self.safe_string(position, 'unrealisedPNL'))
        initialMarginString = self.safe_string(position, 'margin')
        maintenanceMarginString = self.safe_string(position, 'margin')
        timestamp = self.parse8601(self.safe_string(position, 'updated_at'))
        if timestamp is None:
            timestamp = self.safe_integer(position, 'updatedAt')
        # default to cross of USDC margined positions
        marginMode = self.safe_string(position, 'marginMode', 'Isolated') == 'isolated' if 'Isolated' else 'cross'
        mode = 'hedged'
        collateralString = self.safe_string(position, 'positionBalance')
        entryPrice = self.omit_zero(self.safe_string_2(position, 'avgPrice', ''))
        liquidationPrice = self.omit_zero(self.safe_string(position, 'liqPrice'))
        leverage = self.safe_string(position, 'leverage')
        if liquidationPrice is not None:
            if market['settle'] == 'USDC':
                #  (Entry price - Liq price) * Contracts + Maintenance Margin + (unrealised pnl) = Collateral
                difference = Precise.string_abs(Precise.string_sub(entryPrice, liquidationPrice))
                collateralString = Precise.string_add(Precise.string_add(Precise.string_mul(difference, size), maintenanceMarginString), unrealisedPnl)
            else:
                bustPrice = self.safe_string(position, 'bustPrice')
                if market['linear']:
                    # derived from the following formulas
                    #  (Entry price - Bust price) * Contracts = Collateral
                    #  (Entry price - Liq price) * Contracts = Collateral - Maintenance Margin
                    # Maintenance Margin = (Bust price - Liq price) x Contracts
                    maintenanceMarginPriceDifference = Precise.string_abs(Precise.string_sub(liquidationPrice, bustPrice))
                    maintenanceMarginString = Precise.string_mul(maintenanceMarginPriceDifference, size)
                    # Initial Margin = Contracts x Entry Price / Leverage
                    if entryPrice is not None:
                        initialMarginString = Precise.string_div(Precise.string_mul(size, entryPrice), leverage)
                else:
                    # Contracts * (1 / Entry price - 1 / Bust price) = Collateral
                    # Contracts * (1 / Entry price - 1 / Liq price) = Collateral - Maintenance Margin
                    # Maintenance Margin = Contracts * (1 / Liq price - 1 / Bust price)
                    # Maintenance Margin = Contracts * (Bust price - Liq price) / (Liq price x Bust price)
                    difference = Precise.string_abs(Precise.string_sub(bustPrice, liquidationPrice))
                    multiply = Precise.string_mul(bustPrice, liquidationPrice)
                    maintenanceMarginString = Precise.string_div(Precise.string_mul(size, difference), multiply)
                    # Initial Margin = Leverage x Contracts / EntryPrice
                    if entryPrice is not None:
                        initialMarginString = Precise.string_div(size, Precise.string_mul(entryPrice, leverage))
        maintenanceMarginPercentage = Precise.string_div(maintenanceMarginString, notional)
        percentage = Precise.string_mul(Precise.string_div(unrealisedPnl, initialMarginString), '100')
        marginRatio = Precise.string_div(maintenanceMarginString, collateralString, 4)
        # /TEALSTREET
        status = True
        if size == '0':
            status = False
        # \TEALSTREET
        return {
            'info': position,
            # /TEALSTREET
            'id': market['symbol'] + ':' + side,
            # \TEALSTREET
            'mode': mode,
            'symbol': market['symbol'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'initialMargin': self.parse_number(initialMarginString),
            'initialMarginPercentage': self.parse_number(Precise.string_div(initialMarginString, notional)),
            'maintenanceMargin': self.parse_number(maintenanceMarginString),
            'maintenanceMarginPercentage': self.parse_number(maintenanceMarginPercentage),
            'entryPrice': self.parse_number(entryPrice),
            'notional': self.parse_number(notional),
            'leverage': self.parse_number(leverage),
            'unrealizedPnl': self.parse_number(unrealisedPnl),
            'pnl':  self.parse_number(realizedPnl) + self.parse_number(unrealisedPnl),
            'contracts': self.parse_number(size) / self.safe_number(market, 'contractSize'),  # in USD for inverse swaps
            'contractSize': self.safe_number(market, 'contractSize'),
            'marginRatio': self.parse_number(marginRatio),
            'liquidationPrice': self.parse_number(liquidationPrice),
            'markPrice': self.safe_number(position, 'markPrice'),
            'collateral': self.parse_number(collateralString),
            'marginMode': marginMode,
            # /TEALSTREET
            'isolated': marginMode == 'isolated',
            'hedged': mode == 'hedged',
            'price': self.parse_number(entryPrice),
            'status': status,
            'tradeMode': mode,
            'active': status,
            # \TEALSTREET
            'side': side,
            'percentage': self.parse_number(percentage),
        }

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
        if access == 'public':
            if params:
                url += '?' + self.urlencode(params)
        elif access == 'private':
            self.check_required_credentials()
            params = self.extend(params, {
                'apiKey': self.apiKey,
                'timestamp': self.milliseconds() - 0,
            })
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
        if errorCode > 0:
            raise ExchangeError(self.id + ' ' + self.json(response))
