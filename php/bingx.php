<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import

class bingx extends Exchange {

    public function describe() {
        return $this->deep_extend(parent::describe(), array(
            'id' => 'bingx',
            'name' => 'BingX',
            'countries' => array( 'EU' ),
            'rateLimit' => 100,
            'version' => 'v1',
            'verbose' => true,
            'pro' => true,
            'has' => array(
                'CORS' => true,
                'spot' => true,
                'margin' => null,
                'swap' => false,
                'future' => false,
                'option' => false,
                'cancelOrder' => true,
                'createDepositAddress' => true,
                'createOrder' => true,
                'fetchBalance' => true,
                'fetchDepositAddress' => true,
                'fetchDepositAddresses' => true,
                'fetchFundingHistory' => false,
                'fetchFundingRate' => false,
                'fetchFundingRateHistory' => false,
                'fetchFundingRates' => false,
                'fetchIndexOHLCV' => false,
                'fetchMarkOHLCV' => false,
                'fetchOpenInterestHistory' => false,
                'fetchOrderBook' => true,
                'fetchPremiumIndexOHLCV' => false,
                'fetchTicker' => true,
                'fetchTrades' => true,
                'fetchTradingFee' => false,
                'fetchTradingFees' => false,
                'transfer' => true,
            ),
            'urls' => array(
                'logo' => '',
                'api' => array(
                    'spot' => 'https://open-api.bingx.com/openApi/spot',
                    'swap' => 'https://api-swap-rest.bingbon.pro/api',
                    'contract' => 'https://api.bingbon.com/api/coingecko',
                ),
                'test' => array(
                ),
                'www' => 'https://bingx.com/',
                'doc' => array(
                    'https://bingx-api.github.io/docs',
                ),
                'fees' => array(
                    'https://support.bingx.com/hc/en-001/articles/360027240173',
                ),
                'referral' => '',
            ),
            'api' => array(
                'swap' => array(
                    'v1' => array(
                        'public' => array(
                            'get' => array(
                                'market/getAllContracts' => 1,
                                'market/getLatestPrice' => 1,
                                'market/getMarketDepth' => 1,
                                'market/getMarketTrades' => 1,
                                'market/getLatestFunding' => 1,
                                'market/getHistoryFunding' => 1,
                                'market/getLatestKline' => 1,
                                'market/getHistoryKlines' => 1,
                                'market/getOpenPositions' => 1,
                                'market/getTicker' => 1,
                            ),
                            'post' => array(
                                'common/server/time' => 1,
                            ),
                        ),
                        'private' => array(
                            'post' => array(
                                'user/getBalance' => 1,
                                'user/getPositions' => 1,
                                'user/trade' => 1,
                                'user/oneClickClosePosition' => 1,
                                'user/oneClickCloseAllPositions' => 1,
                                'user/cancelOrder' => 1,
                                'user/batchCancelOrders' => 1,
                                'user/cancelAll' => 1,
                                'user/pendingOrders' => 1,
                                'user/queryOrderStatus' => 1,
                                'user/setMarginMode' => 1,
                                'user/setLeverage' => 1,
                                'user/forceOrders' => 1,
                            ),
                        ),
                    ),
                ),
                'contract' => array(
                    'v1' => array(
                        'public' => array(
                            'get' => array(
                                'derivatives/contracts' => 1,
                                'derivatives/orderbook/{ticker_id}' => 1,
                            ),
                        ),
                    ),
                ),
            ),
            'markets' => array(
                'BTC/EUR' => array( 'id' => 'eur', 'symbol' => 'BTC/EUR', 'base' => 'BTC', 'quote' => 'EUR', 'baseId' => 'btc', 'quoteId' => 'eur', 'type' => 'spot', 'spot' => true ),
            ),
            'fees' => array(
                'trading' => array(
                    'tierBased' => true,
                    'percentage' => true,
                    'maker' => $this->parse_number('0.0002'),
                    'taker' => $this->parse_number('0.0004'),
                ),
            ),
            'precisionMode' => TICK_SIZE,
            'requiredCredentials' => array(
                'apiKey' => true,
                'secret' => true,
            ),
        ));
    }

    public function fetch_contract_markets($params = array ()) {
        $response = $this->swapV1PublicGetMarketGetAllContracts ($params);
        //
        //     {
        //         "code":0,
        //         "msg":"Success",
        //         "data":{
        //             "contracts":array(
        //                 {
        //                     "contractId":"100",
        //                     "symbol":"BTC-USDT",
        //                     "name":"BTC",
        //                     "size":"0.0001",
        //                     "currency":"USDT",
        //                     "asset":"BTC",
        //                     "pricePrecision":2,
        //                     "volumePrecision":4,
        //                     "feeRate":0.0005,
        //                     "tradeMinLimit":1,
        //                     "maxLongLeverage":100,
        //                     "maxShortLeverage":100,
        //                     "status":1
        //                 }
        //             )
        //         }
        //     }
        //
        $result = array();
        $data = $this->safe_value($response, 'data', array());
        $contracts = $this->safe_value($data, 'contracts', array());
        for ($i = 0; $i < count($contracts); $i++) {
            $market = $contracts[$i];
            // should we use contract id id?
            // $contractId = $this->safe_string($market, 'contractId');
            $marketId = $this->safe_string($market, 'symbol');
            $parts = explode('-', $marketId);
            $baseId = $this->safe_string($parts, 0);
            $quoteId = $this->safe_string($parts, 1);
            $settleId = $this->safe_string($market, 'currency');
            $base = $this->safe_currency_code($baseId);
            $quote = $this->safe_currency_code($quoteId);
            $settle = $this->safe_currency_code($settleId);
            $symbol = $base . '/' . $quote . ':' . $settle;
            $status = $this->safe_number($market, 'status');
            $result[] = array(
                'id' => $marketId,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'settle' => $settle,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'settleId' => $settleId,
                'type' => 'swap',
                'spot' => false,
                'margin' => true,
                'swap' => true,
                'future' => false,
                'option' => false,
                'active' => $status === 1,
                'contract' => true,
                'linear' => true,
                'inverse' => null,
                'contractSize' => $this->safe_number($market, 'size'),
                'expiry' => null,
                'expiryDatetime' => null,
                'strike' => null,
                'optionType' => null,
                'precision' => array(
                    'amount' => $this->safe_number($market, 'volumePrecision'),
                    'price' => $this->safe_number($market, 'pricePrecision'),
                ),
                'limits' => array(
                    'leverage' => array(
                        'min' => null,
                        'max' => $this->safe_number($market, 'maxLongLeverage'),
                    ),
                    'amount' => array(
                        'min' => $this->safe_number($market, 'tradeMinLimit'),
                        'max' => null,
                    ),
                    'price' => array(
                        'min' => null,
                        'max' => null,
                    ),
                    'cost' => array(
                        'min' => null,
                        'max' => null,
                    ),
                ),
                'info' => $market,
            );
        }
        return $result;
    }

    public function fetch_markets($params = array ()) {
        /**
         * retrieves data on all markets for bingx
         * @param {array} $params extra parameters specific to the exchange api endpoint
         * @return {[array]} an array of objects representing market data
         */
        // $contract = $this->fetch_contract_markets($params);
        // return $contract;
        return array();
    }

    public function parse_balance($response) {
        $result = array( 'info' => $response );
        $currencies = is_array($this->currencies) ? array_keys($this->currencies) : array();
        for ($i = 0; $i < count($currencies); $i++) {
            $code = $currencies[$i];
            $currency = $this->currency($code);
            $currencyId = $currency['id'];
            $free = 'balance_' . $currencyId;
            if (is_array($response) && array_key_exists($free, $response)) {
                $account = $this->account();
                $used = 'locked_' . $currencyId;
                $account['free'] = $this->safe_string($response, $free);
                $account['used'] = $this->safe_string($response, $used);
                $result[$code] = $account;
            }
        }
        return $this->safe_balance($result);
    }

    public function fetch_balance($params = array ()) {
        /**
         * query for balance and get the amount of funds available for trading or funds locked in orders
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} a ~@link https://docs.ccxt.com/en/latest/manual.html?#balance-structure balance structure~
         */
        // $this->load_markets();
        $response = $this->swapV1PrivatePostUserGetBalance ($params);
        return $this->parse_balance($response);
    }

    public function fetch_order_book($symbol, $limit = null, $params = array ()) {
        /**
         * fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data
         * @param {string} $symbol unified $symbol of the $market to fetch the order book for
         * @param {int|null} $limit the maximum amount of order book entries to return
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} A dictionary of ~@link https://docs.ccxt.com/#/?id=order-book-structure order book structures~ indexed by $market symbols
         */
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'currency' => $market['id'],
        );
        $response = $this->publicGetDataCurrencyDepth (array_merge($request, $params));
        return $this->parse_order_book($response, $market['symbol'], null, 'bids', 'asks', 'price', 'amount');
    }

    public function parse_ticker($ticker, $market = null) {
        //
        // {
        //     "high":"33740.82",
        //     "low":"32185.15",
        //     "volume":"4.7890433",
        //     "bid":"33313.53",
        //     "ask":"33497.97",
        //     "midpoint":"33405.75",
        //     "vwap":"32802.5263553",
        //     "at":1643381654,
        //     "price":"33143.91",
        //     "open":"33116.86",
        //     "variation":"0.0817",
        //     "currency":"EUR",
        //     "trade_id":"ce2f5152-3ac5-412d-9b24-9fa72338474c",
        //     "size":"0.00041087"
        // }
        //
        $symbol = $this->safe_symbol(null, $market);
        $timestamp = $this->safe_timestamp($ticker, 'at');
        $vwap = $this->safe_string($ticker, 'vwap');
        $baseVolume = $this->safe_string($ticker, 'volume');
        $quoteVolume = Precise::string_mul($baseVolume, $vwap);
        $last = $this->safe_string($ticker, 'price');
        return $this->safe_ticker(array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'high' => $this->safe_string($ticker, 'high'),
            'low' => $this->safe_string($ticker, 'low'),
            'bid' => $this->safe_string($ticker, 'bid'),
            'bidVolume' => null,
            'ask' => $this->safe_string($ticker, 'ask'),
            'askVolume' => null,
            'vwap' => $vwap,
            'open' => $this->safe_string($ticker, 'open'),
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => null,
            'percentage' => $this->safe_string($ticker, 'variation'),
            'average' => null,
            'baseVolume' => $baseVolume,
            'quoteVolume' => $quoteVolume,
            'info' => $ticker,
        ), $market);
    }

    public function fetch_ticker($symbol, $params = array ()) {
        /**
         * fetches a price $ticker, a statistical calculation with the information calculated over the past 24 hours for a specific $market
         * @param {string} $symbol unified $symbol of the $market to fetch the $ticker for
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} a ~@link https://docs.ccxt.com/#/?id=$ticker-structure $ticker structure~
         */
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'currency' => $market['id'],
        );
        $ticker = $this->publicGetDataCurrencyTicker (array_merge($request, $params));
        //
        // {
        //     "high":"33740.82",
        //     "low":"32185.15",
        //     "volume":"4.7890433",
        //     "bid":"33313.53",
        //     "ask":"33497.97",
        //     "midpoint":"33405.75",
        //     "vwap":"32802.5263553",
        //     "at":1643381654,
        //     "price":"33143.91",
        //     "open":"33116.86",
        //     "variation":"0.0817",
        //     "currency":"EUR",
        //     "trade_id":"ce2f5152-3ac5-412d-9b24-9fa72338474c",
        //     "size":"0.00041087"
        // }
        //
        return $this->parse_ticker($ticker, $market);
    }

    public function parse_trade($trade, $market = null) {
        $timestamp = $this->safe_timestamp($trade, 'created_at_int');
        $id = $this->safe_string($trade, 'uuid');
        $market = $this->safe_market(null, $market);
        $side = $this->safe_string($trade, 'side');
        $price = $this->safe_string($trade, 'price');
        $amountField = 'traded_' . strtolower($market['base']);
        $amount = $this->safe_string($trade, $amountField);
        return $this->safe_trade(array(
            'info' => $trade,
            'id' => $id,
            'order' => null,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'symbol' => $market['symbol'],
            'type' => null,
            'side' => $side,
            'takerOrMaker' => null,
            'price' => $price,
            'amount' => $amount,
            'cost' => null,
            'fee' => null,
        ), $market);
    }

    public function fetch_trades($symbol, $since = null, $limit = null, $params = array ()) {
        /**
         * get the list of most recent trades for a particular $symbol
         * @param {string} $symbol unified $symbol of the $market to fetch trades for
         * @param {int|null} $since timestamp in ms of the earliest trade to fetch
         * @param {int|null} $limit the maximum amount of trades to fetch
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {[array]} a list of ~@link https://docs.ccxt.com/en/latest/manual.html?#public-trades trade structures~
         */
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'currency' => $market['id'],
        );
        $response = $this->publicGetDataCurrencyTrades (array_merge($request, $params));
        return $this->parse_trades($response, $market, $since, $limit);
    }

    public function create_deposit_address($code, $params = array ()) {
        /**
         * create a currency deposit address
         * @param {string} $code unified currency $code of the currency for the deposit address
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} an ~@link https://docs.ccxt.com/#/?id=address-structure address structure~
         */
        $this->load_markets();
        $response = $this->privatePostUserAddresses ($params);
        //
        //     {
        //         "address" => "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        //         "valid_until" => 1620041926,
        //         "currency" => "BTC",
        //         "label" => "Savings"
        //     }
        //
        return $this->parse_deposit_address($response);
    }

    public function fetch_deposit_address($code, $params = array ()) {
        /**
         * fetch the deposit address for a currency associated with this account
         * @param {string} $code unified currency $code
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} an ~@link https://docs.ccxt.com/#/?id=address-structure address structure~
         */
        $this->load_markets();
        $request = array(
            'address' => $code,
        );
        $response = $this->privateGetUserAddressesAddress (array_merge($request, $params));
        //
        //     {
        //         "address" => "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        //         "valid_until" => 1620041926,
        //         "currency" => "BTC",
        //         "label" => "Savings"
        //     }
        //
        return $this->parse_deposit_address($response);
    }

    public function fetch_deposit_addresses($codes = null, $params = array ()) {
        /**
         * fetch deposit addresses for multiple currencies and chain types
         * @param {[string]|null} $codes list of unified currency $codes, default is null
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} a list of ~@link https://docs.ccxt.com/#/?id=address-structure address structures~
         */
        $this->load_markets();
        $response = $this->privateGetUserAddresses ($params);
        //
        //     array(
        //         {
        //             "address" => "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        //             "valid_until" => 1620041926,
        //             "currency" => "BTC",
        //             "label" => "Savings"
        //         }
        //     )
        //
        return $this->parse_deposit_addresses($response, $codes);
    }

    public function parse_deposit_address($depositAddress, $currency = null) {
        //
        //     {
        //         "address" => "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        //         "valid_until" => 1620041926,
        //         "currency" => "BTC",
        //         "label" => "Savings"
        //     }
        //
        $address = $this->safe_string($depositAddress, 'address');
        $currencyId = $this->safe_string($depositAddress, 'currency');
        return array(
            'info' => $depositAddress,
            'currency' => $this->safe_currency_code($currencyId, $currency),
            'address' => $address,
            'tag' => null,
            'network' => null,
        );
    }

    public function create_order($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        /**
         * create a trade order
         * @param {string} $symbol unified $symbol of the $market to create an order in
         * @param {string} $type 'market' or 'limit'
         * @param {string} $side 'buy' or 'sell'
         * @param {float} $amount how much of currency you want to trade in units of base currency
         * @param {float|null} $price the $price at which the order is to be fullfilled, in units of the quote currency, ignored in $market orders
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} an ~@link https://docs.ccxt.com/#/?id=order-structure order structure~
         */
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'type' => $this->capitalize($type) . 'Order',
            'currency' => $market['id'],
            'direction' => $side,
            'amount' => $amount,
        );
        if ($type !== 'market') {
            $request['price'] = $price;
        }
        $response = $this->privatePostUserOrders (array_merge($request, $params));
        return $this->safe_order(array(
            'info' => $response,
            'id' => $response['uuid'],
        ), $market);
    }

    public function cancel_order($id, $symbol = null, $params = array ()) {
        /**
         * cancels an open order
         * @param {string} $id order $id
         * @param {string|null} $symbol not used by paymium cancelOrder ()
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} An ~@link https://docs.ccxt.com/#/?$id=order-structure order structure~
         */
        $request = array(
            'uuid' => $id,
        );
        return $this->privateDeleteUserOrdersUuidCancel (array_merge($request, $params));
    }

    public function transfer($code, $amount, $fromAccount, $toAccount, $params = array ()) {
        /**
         * transfer $currency internally between wallets on the same account
         * @param {string} $code unified $currency $code
         * @param {float} $amount amount to transfer
         * @param {string} $fromAccount account to transfer from
         * @param {string} $toAccount account to transfer to
         * @param {array} $params extra parameters specific to the paymium api endpoint
         * @return {array} a ~@link https://docs.ccxt.com/#/?id=transfer-structure transfer structure~
         */
        $this->load_markets();
        $currency = $this->currency($code);
        if (mb_strpos($toAccount, '@') === false) {
            throw new ExchangeError($this->id . ' transfer() only allows transfers to an email address');
        }
        if ($code !== 'BTC' && $code !== 'EUR') {
            throw new ExchangeError($this->id . ' transfer() only allows BTC or EUR');
        }
        $request = array(
            'currency' => $currency['id'],
            'amount' => $this->currency_to_precision($code, $amount),
            'email' => $toAccount,
            // 'comment' => 'a small note explaining the transfer'
        );
        $response = $this->privatePostUserEmailTransfers (array_merge($request, $params));
        //
        //     {
        //         "uuid" => "968f4580-e26c-4ad8-8bcd-874d23d55296",
        //         "type" => "Transfer",
        //         "currency" => "BTC",
        //         "currency_amount" => "string",
        //         "created_at" => "2013-10-24T10:34:37.000Z",
        //         "updated_at" => "2013-10-24T10:34:37.000Z",
        //         "amount" => "1.0",
        //         "state" => "executed",
        //         "currency_fee" => "0.0",
        //         "btc_fee" => "0.0",
        //         "comment" => "string",
        //         "traded_btc" => "string",
        //         "traded_currency" => "string",
        //         "direction" => "buy",
        //         "price" => "string",
        //         "account_operations" => array(
        //             {
        //                 "uuid" => "968f4580-e26c-4ad8-8bcd-874d23d55296",
        //                 "amount" => "1.0",
        //                 "currency" => "BTC",
        //                 "created_at" => "2013-10-24T10:34:37.000Z",
        //                 "created_at_int" => 1389094259,
        //                 "name" => "account_operation",
        //                 "address" => "1FPDBXNqSkZMsw1kSkkajcj8berxDQkUoc",
        //                 "tx_hash" => "string",
        //                 "is_trading_account" => true
        //             }
        //         )
        //     }
        //
        return $this->parse_transfer($response, $currency);
    }

    public function parse_transfer($transfer, $currency = null) {
        //
        //     {
        //         "uuid" => "968f4580-e26c-4ad8-8bcd-874d23d55296",
        //         "type" => "Transfer",
        //         "currency" => "BTC",
        //         "currency_amount" => "string",
        //         "created_at" => "2013-10-24T10:34:37.000Z",
        //         "updated_at" => "2013-10-24T10:34:37.000Z",
        //         "amount" => "1.0",
        //         "state" => "executed",
        //         "currency_fee" => "0.0",
        //         "btc_fee" => "0.0",
        //         "comment" => "string",
        //         "traded_btc" => "string",
        //         "traded_currency" => "string",
        //         "direction" => "buy",
        //         "price" => "string",
        //         "account_operations" => array(
        //             {
        //                 "uuid" => "968f4580-e26c-4ad8-8bcd-874d23d55296",
        //                 "amount" => "1.0",
        //                 "currency" => "BTC",
        //                 "created_at" => "2013-10-24T10:34:37.000Z",
        //                 "created_at_int" => 1389094259,
        //                 "name" => "account_operation",
        //                 "address" => "1FPDBXNqSkZMsw1kSkkajcj8berxDQkUoc",
        //                 "tx_hash" => "string",
        //                 "is_trading_account" => true
        //             }
        //         )
        //     }
        //
        $currencyId = $this->safe_string($transfer, 'currency');
        $updatedAt = $this->safe_string($transfer, 'updated_at');
        $timetstamp = $this->parse_date($updatedAt);
        $accountOperations = $this->safe_value($transfer, 'account_operations');
        $firstOperation = $this->safe_value($accountOperations, 0, array());
        $status = $this->safe_string($transfer, 'state');
        return array(
            'info' => $transfer,
            'id' => $this->safe_string($transfer, 'uuid'),
            'timestamp' => $timetstamp,
            'datetime' => $this->iso8601($timetstamp),
            'currency' => $this->safe_currency_code($currencyId, $currency),
            'amount' => $this->safe_number($transfer, 'amount'),
            'fromAccount' => null,
            'toAccount' => $this->safe_string($firstOperation, 'address'),
            'status' => $this->parse_transfer_status($status),
        );
    }

    public function parse_transfer_status($status) {
        $statuses = array(
            'executed' => 'ok',
            // what are the other $statuses?
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function sign($path, $section = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $type = $section[0];
        $version = $section[1];
        $access = $section[2];
        $rawPath = $path;
        $url = $this->implode_hostname($this->urls['api'][$type]);
        $url .= '/' . $version . '/' . $path;
        $path = $this->implode_params($path, $params);
        $params = $this->omit($params, $this->extract_params($path));
        $params = $this->keysort($params);
        if ($access === 'public') {
            if ($params) {
                $url .= '?' . $this->urlencode($params);
            }
        } elseif ($access === 'private') {
            $this->check_required_credentials();
            $params = array_merge($params, array(
                'apiKey' => $this->apiKey,
                'timestamp' => $this->milliseconds() - 0,
            ));
            // ACTUAL SIGNATURE GENERATION
            $paramString = $this->rawencode($params);
            $originString = $method . '/api/' . $version . '/' . $rawPath . $paramString;
            $signature = $this->hmac($this->encode($originString), $this->encode($this->secret), 'sha256', 'base64');
            // ACTUAL SIGNATURE GENERATION
            $params = array_merge($params, array(
                'sign' => $signature,
            ));
            if ($params) {
                $url .= '?' . $this->urlencode($params);
            }
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function handle_errors($httpCode, $reason, $url, $method, $headers, $body, $response, $requestHeaders, $requestBody) {
        if (!$response) {
            return; // fallback to default error handler
        }
        $errorCode = $this->safe_integer($response, 'code');
        if ($errorCode > 0) {
            throw new ExchangeError($this->id . ' ' . $this->json($response));
        }
    }
}
