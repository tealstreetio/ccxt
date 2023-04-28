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
                'createDepositAddress' => false,
                'createOrder' => true,
                'fetchBalance' => true,
                'fetchDepositAddress' => false,
                'fetchDepositAddresses' => false,
                'fetchFundingHistory' => false,
                'fetchFundingRate' => false,
                'fetchFundingRateHistory' => false,
                'fetchFundingRates' => false,
                'fetchIndexOHLCV' => false,
                'fetchMarkOHLCV' => false,
                'fetchOHLCV' => true,
                'fetchOpenInterestHistory' => false,
                'fetchOpenOrders' => true,
                'fetchOrderBook' => true,
                'fetchPositions' => true,
                'fetchPremiumIndexOHLCV' => false,
                'fetchTicker' => true,
                'fetchTrades' => true,
                'fetchTradingFee' => false,
                'fetchTradingFees' => false,
                'transfer' => false,
            ),
            'urls' => array(
                'logo' => '',
                'api' => array(
                    'swap' => 'https://api-swap-rest.bingbon.pro/api',
                    'swap2' => 'https://open-api.bingx.com',
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
                                'user/pendingStopOrders' => 1,
                                'user/queryOrderStatus' => 1,
                                'user/setMarginMode' => 1,
                                'user/setLeverage' => 1,
                                'user/forceOrders' => 1,
                                'user/auth/userDataStream' => 1,
                            ),
                            'put' => array(
                                'user/auth/userDataStream' => 1,
                            ),
                        ),
                    ),
                ),
                'swap2' => array(
                    'openApi' => array(
                        'public' => array(
                            'get' => array(
                                'swap/v2/quote/klines' => 1,
                            ),
                        ),
                        'private' => array(
                            'get' => array(
                                'swap/v2/trade/openOrders' => 1,
                            ),
                            'put' => array(
                                'user/auth/userDataStream' => 1,
                            ),
                            'post' => array(
                                'user/auth/userDataStream' => 1,
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
            'timeframes' => array(
                '1m' => '1',
                '3m' => '3',
                '5m' => '5',
                '15m' => '15',
                '30m' => '30',
                '1h' => '60',
                '2h' => '120',
                '4h' => '240',
                '6h' => '360',
                '12h' => '720',
                '1d' => '1D',
                '1w' => '1W',
                '1M' => '1M',
            ),
            'options' => array(
                'listenKeyRefreshRate' => 1200000, // 20 mins
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
        $contract = $this->fetch_contract_markets($params);
        return $contract;
    }

    public function parse_balance($response) {
        $result = array( 'info' => $response );
        $data = $this->safe_value($response, 'data', array());
        $dataAccount = $this->safe_value($data, 'account', array());
        $currencies = is_array($this->currencies) ? array_keys($this->currencies) : array();
        for ($i = 0; $i < count($currencies); $i++) {
            $code = $currencies[$i];
            $account = $this->account();
            if ($this->safe_string($dataAccount, 'currency', '') === $code) {
                $account['free'] = $this->safe_string($dataAccount, 'availableMArgin');
                $account['used'] = $this->safe_string($dataAccount, 'usedMargin');
                $account['total'] = $this->safe_string($dataAccount, 'balance');
            }
            $result[$code] = $account;
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
        //   "symbol" => "BTC-USDT",
        //   "priceChange" => "10.00",
        //   "priceChangePercent" => "10",
        //   "lastPrice" => "5738.23",
        //   "lastVolume" => "31.21",
        //   "highPrice" => "5938.23",
        //   "lowPrice" => "5238.23",
        //   "volume" => "23211231.13",
        //   "dayVolume" => "213124412412.47",
        //   "openPrice" => "5828.32"
        // }
        //
        $symbol = $this->safe_symbol(null, $market);
        $timestamp = $this->milliseconds();
        $baseVolume = $this->safe_string($ticker, 'volume');
        $last = $this->safe_string($ticker, 'lastPrice');
        return $this->safe_ticker(array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'high' => $this->safe_string($ticker, 'highPrice'),
            'low' => $this->safe_string($ticker, 'lowPrice'),
            'bid' => $this->safe_string($ticker, 'lastPrice'),
            'bidVolume' => null,
            'ask' => $this->safe_string($ticker, 'lastPrice'),
            'askVolume' => null,
            'open' => $this->safe_string($ticker, 'openPrice'),
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => null,
            'percentage' => $this->safe_string($ticker, 'priceChangePercent'),
            'average' => null,
            'baseVolume' => $baseVolume,
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
            'symbol' => $market['id'],
        );
        $ticker = $this->swapV1PublicGetMarketGetTicker (array_merge($request, $params));
        //
        // {
        //   "symbol" => "BTC-USDT",
        //   "priceChange" => "10.00",
        //   "priceChangePercent" => "10",
        //   "lastPrice" => "5738.23",
        //   "lastVolume" => "31.21",
        //   "highPrice" => "5938.23",
        //   "lowPrice" => "5238.23",
        //   "volume" => "23211231.13",
        //   "dayVolume" => "213124412412.47",
        //   "openPrice" => "5828.32"
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
        return array();
        // /**
        //
        //
        //  * get the list of most recent trades for a particular $symbol
        //  * @param {string} $symbol unified $symbol of the $market to fetch trades for
        //  * @param {int|null} $since timestamp in ms of the earliest trade to fetch
        //  * @param {int|null} $limit the maximum amount of trades to fetch
        //  * @param {array} $params extra parameters specific to the paymium api endpoint
        //  * @return {[array]} a list of ~@link https://docs.ccxt.com/en/latest/manual.html?#public-trades trade structures~
        //  */
        // $this->load_markets();
        // $market = $this->market($symbol);
        // $request = array(
        //     'currency' => $market['id'],
        // );
        // $response = $this->publicGetDataCurrencyTrades (array_merge($request, $params));
        // return $this->parse_trades($response, $market, $since, $limit);
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

    public function fetch_positions($symbols = null, $params = array ()) {
        /**
         * fetch all open $positions
         * @param {[string]|null} $symbols list of unified market $symbols
         * @param {array} $params extra parameters specific to the bybit api endpoint
         * @return {[array]} a list of ~@link https://docs.ccxt.com/#/?id=position-structure position structure~
         */
        $response = $this->swapV1PrivatePostUserGetPositions ();
        $data = $this->safe_value($response, 'data', array());
        $positions = $this->safe_value($data, 'positions', array());
        $result = array();
        for ($i = 0; $i < count($positions); $i++) {
            $result[] = $this->parse_position($positions[$i]);
        }
        return $result;
    }

    public function parse_position($position, $market = null) {
        //
        //
        // {
        //     "positionId" => "1650546544279240704",
        //     "symbol" => "BTC-USDT",
        //     "currency" => "",
        //     "volume" => 0.001,
        //     "availableVolume" => 0.001,
        //     "positionSide" => "short",
        //     "marginMode" => "cross",
        //     "avgPrice" => 27124.5,
        //     "liquidatedPrice" => 0.0,
        //     "margin" => 2.9386,
        //     "leverage" => 5.0,
        //     "pnlRate" => -45.83,
        //     "unrealisedPNL" => -2.4863,
        //     "realisedPNL" => 0.0126
        // }
        //
        $marketId = $this->safe_string($position, 'symbol');
        $market = $this->safe_market($marketId, $market);
        $timestamp = $this->safe_integer($position, 'cTime');
        $marginMode = $this->safe_string_lower($position, 'marginMode');
        $hedged = true;
        $side = $this->safe_string_lower($position, 'positionSide');
        $contracts = $this->safe_float($position, 'volume') / $this->safe_number($market, 'contractSize');
        $liquidation = $this->safe_number($position, 'liquidatedPrice');
        if ($side === 'short') {
            $contracts = -1 * $contracts;
        }
        if ($liquidation === 0) {
            $liquidation = null;
        }
        $initialMargin = $this->safe_number($position, 'margin');
        return array(
            'info' => $position,
            'id' => $market['symbol'] . ':' . $side,
            'symbol' => $market['symbol'],
            'notional' => null,
            'marginMode' => $marginMode,
            'liquidationPrice' => $liquidation,
            'entryPrice' => $this->safe_number($position, 'avgPrice'),
            'unrealizedPnl' => $this->safe_number($position, 'unrealizedPL'),
            'percentage' => null,
            'contracts' => $contracts,
            'contractSize' => $this->safe_number($market, 'contractSize'),
            'side' => $side,
            'hedged' => $hedged,
            'timestamp' => $timestamp,
            'markPrice' => $this->safe_number($position, 'markPrice'),
            'datetime' => $this->iso8601($timestamp),
            'maintenanceMargin' => null,
            'maintenanceMarginPercentage' => null,
            'collateral' => $this->safe_number($position, 'margin'),
            'initialMargin' => $initialMargin,
            'initialMarginPercentage' => null,
            'leverage' => $this->safe_number($position, 'leverage'),
            'marginRatio' => null,
        );
    }

    public function fetch_ohlcv($symbol, $timeframe = '1m', $since = null, $limit = null, $params = array ()) {
        /**
         * fetches historical candlestick data containing the open, high, low, and close price, and the volume of a $market
         * @see https://bybit-exchange.github.io/docs/v5/market/kline
         * @see https://bybit-exchange.github.io/docs/v5/market/mark-kline
         * @see https://bybit-exchange.github.io/docs/v5/market/index-kline
         * @see https://bybit-exchange.github.io/docs/v5/market/preimum-index-kline
         * @param {string} $symbol unified $symbol of the $market to fetch OHLCV data for
         * @param {string} $timeframe the length of time each candle represents
         * @param {int|null} $since timestamp in ms of the earliest candle to fetch
         * @param {int|null} $limit the maximum amount of candles to fetch
         * @param {array} $params extra parameters specific to the bybit api endpoint
         * @return {[[int]]} A list of candles ordered, open, high, low, close, volume
         */
        $this->check_required_symbol('fetchOHLCV', $symbol);
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'symbol' => $market['id'],
        );
        if ($limit === null) {
            $limit = 200; // default is 200 when requested with `$since`
        }
        if ($since !== null) {
            $request['startTime'] = $since;
        }
        $klineType = $this->safe_string($this->timeframes, $timeframe, $timeframe);
        $request['interval'] = $timeframe;
        if ($limit !== null) {
            // $request['limit'] = $limit; // max 1000, default 1000
            if ($klineType === '1') {
                $request['endTime'] = $since . $limit * 60 * 1000;
            } elseif ($klineType === '3') {
                $request['endTime'] = $since . $limit * 3 * 60 * 1000;
            } elseif ($klineType === '5') {
                $request['endTime'] = $since . $limit * 5 * 60 * 1000;
            } elseif ($klineType === '15') {
                $request['endTime'] = $since . $limit * 15 * 60 * 1000;
            } elseif ($klineType === '30') {
                $request['endTime'] = $since . $limit * 30 * 60 * 1000;
            } elseif ($klineType === '60') {
                $request['endTime'] = $since . $limit * 60 * 60 * 1000;
            } elseif ($klineType === '120') {
                $request['endTime'] = $since . $limit * 120 * 60 * 1000;
            } elseif ($klineType === '240') {
                $request['endTime'] = $since . $limit * 240 * 60 * 1000;
            } elseif ($klineType === '360') {
                $request['endTime'] = $since . $limit * 360 * 60 * 1000;
            } elseif ($klineType === '720') {
                $request['endTime'] = $since . $limit * 720 * 60 * 1000;
            } elseif ($klineType === '1D') {
                $request['endTime'] = $since . $limit * 24 * 60 * 60 * 1000;
            } elseif ($klineType === '1W') {
                $request['endTime'] = $since . $limit * 7 * 24 * 60 * 60 * 1000;
            } elseif ($klineType === '1M') {
                $request['endTime'] = $since . $limit * 30 * 24 * 60 * 60 * 1000;
            } else {
                $request['endTime'] = $since . $limit * 60 * 1000;
            }
        }
        $response = $this->swap2OpenApiPublicGetSwapV2QuoteKlines (array_merge($request, $params));
        $ohlcvs = $this->safe_value($response, 'data', array());
        return $this->parse_ohlcvs($ohlcvs, $market, $timeframe, $since, $limit);
    }

    public function parse_ohlcvs($ohlcvs, $market = null, $timeframe = '1m', $since = null, $limit = null) {
        $results = array();
        for ($i = 0; $i < count($ohlcvs); $i++) {
            $results[] = $this->parse_ohlcv($ohlcvs[$i], $market);
        }
        $sorted = $this->sort_by($results, 0);
        $tail = ($since === null);
        return $this->filter_by_since_limit($sorted, $since, $limit, 0, $tail);
    }

    public function parse_ohlcv($ohlcv, $market = null) {
        return array(
            $this->safe_integer($ohlcv, 'time'), // timestamp
            $this->safe_number($ohlcv, 'open'), // open
            $this->safe_number($ohlcv, 'high'), // high
            $this->safe_number($ohlcv, 'low'), // low
            $this->safe_number($ohlcv, 'close'), // close
            $this->safe_number($ohlcv, 'volume'), // volume
        );
    }

    public function parse_order_status($status) {
        $statuses = array(
            'pending' => 'open',
            'new' => 'open',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_stop_trigger($status) {
        $statuses = array(
            'market_price' => 'mark',
            'fill_price' => 'last',
            'index_price' => 'index',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_order_type($type) {
        $types = array(
            'limit' => 'limit',
            'market' => 'market',
            'stop_market' => 'stop',
            'take_profit_market' => 'stop',
            'trigger_limit' => 'stopLimit',
            'trigger_market' => 'stopLimit',
        );
        return $this->safe_string_lower($types, $type, $type);
    }

    public function parse_order($order, $market = null) {
        // {
        //     "code" => 0,
        //     "msg" => "",
        //     "data" => {
        //       "orders" => array(
        //         array(
        //           "symbol" => "BTC-USDT",
        //           "orderId" => 1651880171474731000,
        //           "side" => "SELL",
        //           "positionSide" => "LONG",
        //           "type" => "TAKE_PROFIT_MARKET",
        //           "origQty" => "0.0020",
        //           "price" => "0.0",
        //           "executedQty" => "0.0000",
        //           "avgPrice" => "0.0",
        //           "cumQuote" => "0",
        //           "stopPrice" => "35000.0",
        //           "profit" => "0.0",
        //           "commission" => "0.0",
        //           "status" => "NEW",
        //           "time" => 1682673897986,
        //           "updateTime" => 1682673897986
        //         ),
        //         array(
        //           "symbol" => "BTC-USDT",
        //           "orderId" => 1651880171445371000,
        //           "side" => "SELL",
        //           "positionSide" => "LONG",
        //           "type" => "STOP_MARKET",
        //           "origQty" => "0.0020",
        //           "price" => "0.0",
        //           "executedQty" => "0.0000",
        //           "avgPrice" => "28259.0",
        //           "cumQuote" => "0",
        //           "stopPrice" => "27000.0",
        //           "profit" => "0.0",
        //           "commission" => "0.0",
        //           "status" => "NEW",
        //           "time" => 1682673897979,
        //           "updateTime" => 1682673897979
        //         ),
        //         array(
        //           "symbol" => "BTC-USDT",
        //           "orderId" => 1651287406772699100,
        //           "side" => "BUY",
        //           "positionSide" => "LONG",
        //           "type" => "LIMIT",
        //           "origQty" => "0.0001",
        //           "price" => "25000.0",
        //           "executedQty" => "0.0000",
        //           "avgPrice" => "0.0",
        //           "cumQuote" => "0",
        //           "stopPrice" => "",
        //           "profit" => "0.0",
        //           "commission" => "0.0",
        //           "status" => "PENDING",
        //           "time" => 1682532572000,
        //           "updateTime" => 1682532571000
        //         ),
        //         {
        //           "symbol" => "BTC-USDT",
        //           "orderId" => 1651006482122227700,
        //           "side" => "BUY",
        //           "positionSide" => "LONG",
        //           "type" => "LIMIT",
        //           "origQty" => "0.0001",
        //           "price" => "25000.0",
        //           "executedQty" => "0.0000",
        //           "avgPrice" => "0.0",
        //           "cumQuote" => "0",
        //           "stopPrice" => "",
        //           "profit" => "0.0",
        //           "commission" => "0.0",
        //           "status" => "PENDING",
        //           "time" => 1682465594000,
        //           "updateTime" => 1682465594000
        //         }
        //       )
        //     }
        //   }
        $marketId = $this->safe_string($order, 'symbol');
        $market = $this->safe_market($marketId);
        $symbol = $market['symbol'];
        $id = $this->safe_string($order, 'orderId');
        $price = $this->safe_string($order, 'price');
        $amount = $this->safe_string($order, 'origQty');
        $filled = $this->safe_string($order, 'executedQty');
        $cost = $this->safe_string($order, 'executedQty');
        $average = $this->safe_string($order, 'avgPrice');
        $type = $this->parse_order_type($this->safe_string_lower($order, 'type'));
        $timestamp = $this->safe_integer($order, 'time');
        $rawStopTrigger = $this->safe_string($order, 'stopPrice');
        $trigger = $this->parse_stop_trigger($rawStopTrigger);
        $side = $this->safe_string_lower($order, 'side');
        $reduce = $this->safe_value($order, 'reduceOnly', false);
        $close = $reduce;
        $planType = $this->safe_string_lower($order, 'type');
        if ($planType === 'stop_market' || $planType === 'take_profit_market') {
            $reduce = true;
            $close = true;
        }
        if ($side && explode('_', $side)[0] === 'close') {
            $reduce = true;
            $close = true;
        }
        // $order $type LIMIT, MARKET, STOP_MARKET, TAKE_PROFIT_MARKET, TRIGGER_LIMIT, TRIGGER_MARKET
        // if ($rawStopTrigger) {
        //     if ($type === 'market') {
        //         $type = 'stop';
        //     } else {
        //         $type = 'stopLimit';
        //     }
        // } else {
        //     if ($type === 'market') {
        //         $type = 'market';
        //     } else {
        //         $type = 'limit';
        //     }
        // }
        $clientOrderId = $this->safe_string($order, 'orderId');
        $fee = $this->safe_string($order, 'comission');
        $rawStatus = $this->safe_string_lower($order, 'status');
        $status = $this->parse_order_status($rawStatus);
        $lastTradeTimestamp = $this->safe_integer($order, 'updateTime');
        $timeInForce = $this->safe_string($order, 'timeInForce');
        $postOnly = $timeInForce === 'PostOnly';
        $stopPrice = $this->safe_number($order, 'stopPrice');
        return $this->safe_order(array(
            'info' => $order,
            'id' => $id,
            'clientOrderId' => $clientOrderId,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'lastTradeTimestamp' => $lastTradeTimestamp,
            'symbol' => $symbol,
            'type' => $type,
            'timeInForce' => 'GTC',
            'postOnly' => $postOnly,
            'side' => $side,
            'price' => $price,
            'stopPrice' => $stopPrice,
            'average' => $average,
            'cost' => $cost,
            'amount' => $amount,
            'filled' => $filled,
            'remaining' => null,
            'status' => $status,
            'fee' => $fee,
            'trades' => null,
            'reduce' => $reduce,  // TEALSTREET
            'close' => $close,  // TEALSTREET
            'trigger' => $trigger,  // TEALSTREET
        ), $market);
    }

    public function fetch_open_orders_v2($symbol = null, $since = null, $limit = null, $params = array ()) {
        /**
         * fetch all unfilled currently open $orders
         * @param {string|null} $symbol unified market $symbol
         * @param {int|null} $since the earliest time in ms to fetch open $orders for
         * @param {int|null} $limit the maximum number of  open $orders structures to retrieve
         * @param {array} $params extra parameters specific to the bybit api endpoint
         * @return {[array]} a list of ~@link https://docs.ccxt.com/#/?id=order-structure order structures~
         */
        $this->load_markets();
        $response = $this->swap2OpenApiPrivateGetSwapV2TradeOpenOrders ();
        $data = $this->safe_value($response, 'data', array());
        $orders = $this->safe_value($data, 'orders', array());
        $result = array();
        for ($i = 0; $i < count($orders); $i++) {
            $result[] = $this->parse_order($orders[$i]);
        }
        return $result;
    }

    public function fetch_orders($symbol = null, $since = null, $limit = null, $params = array ()) {
        return $this->fetch_open_orders_v2($symbol, $since, $limit, $params);
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
        if ($access === 'private') {
            $this->check_required_credentials();
            $isOpenApi = mb_strpos($url, 'openOrders') !== false;
            $isUserDataStreamEp = mb_strpos($url, 'userDataStream') !== false;
            if ($isOpenApi || $isUserDataStreamEp) {
                $params = array_merge($params, array(
                    'timestamp' => $this->milliseconds() - 0,
                ));
                $params = $this->keysort($params);
                $paramString = $this->rawencode($params);
                $signature = $this->hmac($this->encode($paramString), $this->encode($this->secret), 'sha256');
                $params = array_merge($params, array(
                    'signature' => $signature,
                ));
                $headers = array(
                    'X-BX-APIKEY' => $this->apiKey,
                );
                if ($method !== 'GET') {
                    $body = $this->urlencode($params);
                }
            } else {
                $params = array_merge($params, array(
                    'apiKey' => $this->apiKey,
                    'timestamp' => $this->milliseconds() - 0,
                ));
                $params = $this->keysort($params);
                // ACTUAL SIGNATURE GENERATION
                $paramString = $this->rawencode($params);
                $originString = $method . '/api/' . $version . '/' . $rawPath . $paramString;
                $signature = $this->hmac($this->encode($originString), $this->encode($this->secret), 'sha256', 'base64');
                // ACTUAL SIGNATURE GENERATION
                $params = array_merge($params, array(
                    'sign' => $signature,
                ));
            }
        }
        if ($params) {
            $url .= '?' . $this->urlencode($params);
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function handle_errors($httpCode, $reason, $url, $method, $headers, $body, $response, $requestHeaders, $requestBody) {
        if (!$response) {
            return; // fallback to default error handler
        }
        $errorCode = $this->safe_integer($response, 'code');
        if ($errorCode !== null && $errorCode > 0) {
            throw new ExchangeError($this->id . ' ' . $this->json($response));
        }
    }
}
