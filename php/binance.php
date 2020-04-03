<?php

namespace ccxtpro;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use \ccxt\ExchangeError;

class binance extends \ccxt\binance {

    use ClientTrait;

    public function describe() {
        return $this->deep_extend(parent::describe (), array(
            'has' => array(
                'ws' => true,
                'watchOrderBook' => true,
                'watchTrades' => true,
                'watchOHLCV' => true,
                'watchTicker' => true,
                'watchTickers' => false, // for now
                'watchOrders' => true,
                'watchBalance' => true,
            ),
            'urls' => array(
                'api' => array(
                    'ws' => array(
                        'spot' => 'wss://stream.binance.com:9443/ws',
                        'future' => 'wss://fstream.binance.com/ws',
                    ),
                ),
            ),
            'options' => array(
                // get updates every 1000ms or 100ms
                // or every 0ms in real-time for futures
                'watchOrderBookRate' => 100,
                'tradesLimit' => 1000,
                'OHLCVLimit' => 1000,
                'requestId' => array(),
            ),
        ));
    }

    public function request_id($url) {
        $options = $this->safe_value($this->options, 'requestId', array());
        $previousValue = $this->safe_integer($options, $url, 0);
        $newValue = $this->sum($previousValue, 1);
        $this->options['requestId'][$url] = $newValue;
        return $newValue;
    }

    public function watch_order_book($symbol, $limit = null, $params = array ()) {
        //
        // https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#partial-book-depth-streams
        //
        // <$symbol>@depth<levels>@100ms or <$symbol>@depth<levels> (1000ms)
        // valid <levels> are 5, 10, or 20
        //
        // todo add support for <levels>-snapshots (depth)
        //
        //     if ($limit !== null) {
        //         if (($limit !== 5) && ($limit !== 10) && ($limit !== 20)) {
        //             throw new ExchangeError($this->id . ' watchOrderBook $limit argument must be null, 5, 10 or 20');
        //         }
        //     }
        //
        $this->load_markets();
        $defaultType = $this->safe_string_2($this->options, 'watchOrderBook', 'defaultType', 'spot');
        $type = $this->safe_string($params, 'type', $defaultType);
        $query = $this->omit($params, 'type');
        $market = $this->market($symbol);
        //
        // notice the differences between trading futures and spot trading
        // the algorithms use different urls in step 1
        // delta caching and merging also differs in steps 4, 5, 6
        //
        // spot/margin
        // https://binance-docs.github.io/apidocs/spot/en/#how-to-manage-a-local-order-book-correctly
        //
        // 1. Open a stream to wss://stream.binance.com:9443/ws/bnbbtc@depth.
        // 2. Buffer the events you receive from the stream.
        // 3. Get a depth snapshot from https://www.binance.com/api/v1/depth?$symbol=BNBBTC&$limit=1000 .
        // 4. Drop any event where u is <= lastUpdateId in the snapshot.
        // 5. The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
        // 6. While listening to the stream, each new event's U should be equal to the previous event's u+1.
        // 7. The data in each event is the absolute quantity for a price level.
        // 8. If the quantity is 0, remove the price level.
        // 9. Receiving an event that removes a price level that is not in your local order book can happen and is normal.
        //
        // futures
        // https://binance-docs.github.io/apidocs/futures/en/#how-to-manage-a-local-order-book-correctly
        //
        // 1. Open a stream to wss://fstream.binance.com/stream?streams=btcusdt@depth.
        // 2. Buffer the events you receive from the stream. For same price, latest received update covers the previous one.
        // 3. Get a depth snapshot from https://fapi.binance.com/fapi/v1/depth?$symbol=BTCUSDT&$limit=1000 .
        // 4. Drop any event where u is < lastUpdateId in the snapshot.
        // 5. The first processed event should have U <= lastUpdateId AND u >= lastUpdateId
        // 6. While listening to the stream, each new event's pu should be equal to the previous event's u, otherwise initialize the process from step 3.
        // 7. The data in each event is the absolute quantity for a price level.
        // 8. If the quantity is 0, remove the price level.
        // 9. Receiving an event that removes a price level that is not in your local order book can happen and is normal.
        //
        $name = 'depth';
        $messageHash = $market['lowercaseId'] . '@' . $name;
        $url = $this->urls['api']['ws'][$type]; // . '/' . $messageHash;
        $requestId = $this->request_id($url);
        $watchOrderBookRate = $this->safe_string($this->options, 'watchOrderBookRate', '100');
        $request = array(
            'method' => 'SUBSCRIBE',
            'params' => array(
                $messageHash . '@' . $watchOrderBookRate . 'ms',
            ),
            'id' => $requestId,
        );
        $subscription = array(
            'id' => (string) $requestId,
            'messageHash' => $messageHash,
            'name' => $name,
            'symbol' => $symbol,
            'method' => array($this, 'handle_order_book_subscription'),
            'limit' => $limit,
            'type' => $type,
        );
        $message = array_merge($request, $query);
        // 1. Open a stream to wss://stream.binance.com:9443/ws/bnbbtc@depth.
        $future = $this->watch($url, $messageHash, $message, $messageHash, $subscription);
        return $this->after($future, array($this, 'limit_order_book'), $symbol, $limit, $params);
    }

    public function fetch_order_book_snapshot($client, $message, $subscription) {
        $type = $this->safe_value($subscription, 'type');
        $symbol = $this->safe_string($subscription, 'symbol');
        $messageHash = $this->safe_string($subscription, 'messageHash');
        // 3. Get a depth $snapshot from https://www.binance.com/api/v1/depth?$symbol=BNBBTC&limit=1000 .
        // todo => this is a synch blocking call in ccxt.php - make it async
        $snapshot = $this->fetch_order_book($symbol);
        $orderbook = $this->safe_value($this->orderbooks, $symbol);
        if ($orderbook === null) {
            // if the $orderbook is dropped before the $snapshot is received
            return;
        }
        $orderbook->reset ($snapshot);
        // unroll the accumulated deltas
        $messages = $orderbook->cache;
        for ($i = 0; $i < count($messages); $i++) {
            $message = $messages[$i];
            $U = $this->safe_integer($message, 'U');
            $u = $this->safe_integer($message, 'u');
            $pu = $this->safe_integer($message, 'pu');
            if ($type === 'future') {
                // 4. Drop any event where $u is < lastUpdateId in the $snapshot
                if ($u < $orderbook['nonce']) {
                    continue;
                }
                // 5. The first processed event should have $U <= lastUpdateId AND $u >= lastUpdateId
                if (($U <= $orderbook['nonce']) && ($u >= $orderbook['nonce']) || ($pu === $orderbook['nonce'])) {
                    $this->handle_order_book_message($client, $message, $orderbook);
                }
            } else {
                // 4. Drop any event where $u is <= lastUpdateId in the $snapshot
                if ($u <= $orderbook['nonce']) {
                    continue;
                }
                // 5. The first processed event should have $U <= lastUpdateId+1 AND $u >= lastUpdateId+1
                if ((($U - 1) <= $orderbook['nonce']) && (($u - 1) >= $orderbook['nonce'])) {
                    $this->handle_order_book_message($client, $message, $orderbook);
                }
            }
        }
        $this->orderbooks[$symbol] = $orderbook;
        $client->resolve ($orderbook, $messageHash);
    }

    public function handle_delta($bookside, $delta) {
        $price = $this->safe_float($delta, 0);
        $amount = $this->safe_float($delta, 1);
        $bookside->store ($price, $amount);
    }

    public function handle_deltas($bookside, $deltas) {
        for ($i = 0; $i < count($deltas); $i++) {
            $this->handle_delta($bookside, $deltas[$i]);
        }
    }

    public function handle_order_book_message($client, $message, $orderbook) {
        $u = $this->safe_integer($message, 'u');
        $this->handle_deltas($orderbook['asks'], $this->safe_value($message, 'a', array()));
        $this->handle_deltas($orderbook['bids'], $this->safe_value($message, 'b', array()));
        $orderbook['nonce'] = $u;
        $timestamp = $this->safe_integer($message, 'E');
        $orderbook['timestamp'] = $timestamp;
        $orderbook['datetime'] = $this->iso8601($timestamp);
        return $orderbook;
    }

    public function handle_order_book($client, $message) {
        //
        // initial snapshot is fetched with ccxt's fetchOrderBook
        // the feed does not include a snapshot, just the deltas
        //
        //     {
        //         "$e" => "depthUpdate", // Event type
        //         "E" => 1577554482280, // Event time
        //         "s" => "BNBBTC", // Symbol
        //         "$U" => 157, // First update ID in event
        //         "$u" => 160, // Final update ID in event
        //         "b" => array( // bids
        //             array( "0.0024", "10" ), // price, size
        //         ),
        //         "a" => array( // asks
        //             array( "0.0026", "100" ), // price, size
        //         )
        //     }
        //
        $marketId = $this->safe_string($message, 's');
        $market = null;
        $symbol = null;
        if ($marketId !== null) {
            if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
                $market = $this->markets_by_id[$marketId];
                $symbol = $market['symbol'];
            }
        }
        $name = 'depth';
        $messageHash = $market['lowercaseId'] . '@' . $name;
        $orderbook = $this->safe_value($this->orderbooks, $symbol);
        if ($orderbook === null) {
            //
            // https://github.com/ccxt/ccxt/issues/6672
            //
            // Sometimes Binance sends the first delta before the subscription
            // confirmation arrives. At that point the $orderbook is not
            // initialized yet and the snapshot has not been requested yet
            // therefore it is safe to drop these premature messages.
            //
            return;
        }
        $nonce = $this->safe_integer($orderbook, 'nonce');
        if ($nonce === null) {
            // 2. Buffer the events you receive from the stream.
            $orderbook->cache[] = $message;
        } else {
            try {
                $U = $this->safe_integer($message, 'U');
                $u = $this->safe_integer($message, 'u');
                $pu = $this->safe_integer($message, 'pu');
                if ($pu === null) {
                    // spot
                    // 4. Drop any event where $u is <= lastUpdateId in the snapshot
                    if ($u > $orderbook['nonce']) {
                        $timestamp = $this->safe_integer($orderbook, 'timestamp');
                        $conditional = null;
                        if ($timestamp === null) {
                            // 5. The first processed event should have $U <= lastUpdateId+1 AND $u >= lastUpdateId+1
                            $conditional = (($U - 1) <= $orderbook['nonce']) && (($u - 1) >= $orderbook['nonce']);
                        } else {
                            // 6. While listening to the stream, each new event's $U should be equal to the previous event's $u+1.
                            $conditional = (($U - 1) === $orderbook['nonce']);
                        }
                        if ($conditional) {
                            $this->handle_order_book_message($client, $message, $orderbook);
                            if ($nonce < $orderbook['nonce']) {
                                $client->resolve ($orderbook, $messageHash);
                            }
                        } else {
                            // todo => $client->reject from handleOrderBookMessage properly
                            throw new ExchangeError($this->id . ' handleOrderBook received an out-of-order nonce');
                        }
                    }
                } else {
                    // future
                    // 4. Drop any event where $u is < lastUpdateId in the snapshot
                    if ($u >= $orderbook['nonce']) {
                        // 5. The first processed event should have $U <= lastUpdateId AND $u >= lastUpdateId
                        // 6. While listening to the stream, each new event's $pu should be equal to the previous event's $u, otherwise initialize the process from step 3
                        if (($U <= $orderbook['nonce']) || ($pu === $orderbook['nonce'])) {
                            $this->handle_order_book_message($client, $message, $orderbook);
                            if ($nonce <= $orderbook['nonce']) {
                                $client->resolve ($orderbook, $messageHash);
                            }
                        } else {
                            // todo => $client->reject from handleOrderBookMessage properly
                            throw new ExchangeError($this->id . ' handleOrderBook received an out-of-order nonce');
                        }
                    }
                }
            } catch (Exception $e) {
                unset($this->orderbooks[$symbol]);
                unset($client->subscriptions[$messageHash]);
                $client->reject ($e, $messageHash);
            }
        }
    }

    public function sign_message($client, $messageHash, $message, $params = array ()) {
        // todo => implement binance signMessage
        return $message;
    }

    public function handle_order_book_subscription($client, $message, $subscription) {
        $symbol = $this->safe_string($subscription, 'symbol');
        $limit = $this->safe_integer($subscription, 'limit');
        if (is_array($this->orderbooks) && array_key_exists($symbol, $this->orderbooks)) {
            unset($this->orderbooks[$symbol]);
        }
        $this->orderbooks[$symbol] = $this->order_book(array(), $limit);
        // fetch the snapshot in a separate async call
        $this->spawn(array($this, 'fetch_order_book_snapshot'), $client, $message, $subscription);
    }

    public function handle_subscription_status($client, $message) {
        //
        //     {
        //         "result" => null,
        //         "$id" => 1574649734450
        //     }
        //
        $id = $this->safe_string($message, 'id');
        $subscriptionsById = $this->index_by($client->subscriptions, 'id');
        $subscription = $this->safe_value($subscriptionsById, $id, array());
        $method = $this->safe_value($subscription, 'method');
        if ($method !== null) {
            $method($client, $message, $subscription);
        }
        return $message;
    }

    public function watch_trades($symbol, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market($symbol);
        $name = 'trade';
        $messageHash = $market['lowercaseId'] . '@' . $name;
        $future = $this->watch_public($messageHash, $params);
        return $this->after($future, array($this, 'filter_by_since_limit'), $since, $limit, 'timestamp', true);
    }

    public function parse_trade($trade, $market = null) {
        //
        //     {
        //         e => 'trade',       // $event type
        //         E => 1579481530911, // $event time
        //         s => 'ETHBTC',      // $symbol
        //         t => 158410082,     // $trade $id
        //         p => '0.01914100',  // $price
        //         q => '0.00700000',  // quantity
        //         b => 586187049,     // buyer order $id
        //         a => 586186710,     // seller order $id
        //         T => 1579481530910, // $trade time
        //         m => false,         // is the buyer the $market maker
        //         M => true           // binance docs say it should be ignored
        //     }
        //
        $event = $this->safe_string($trade, 'e');
        if ($event === null) {
            return parent::parse_trade($trade, $market);
        }
        $id = $this->safe_string($trade, 't');
        $timestamp = $this->safe_integer($trade, 'T');
        $price = $this->safe_float($trade, 'p');
        $amount = $this->safe_float($trade, 'q');
        $cost = null;
        if (($price !== null) && ($amount !== null)) {
            $cost = $price * $amount;
        }
        $symbol = null;
        $marketId = $this->safe_string($trade, 's');
        if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
            $market = $this->markets_by_id[$marketId];
        }
        if (($symbol === null) && ($market !== null)) {
            $symbol = $market['symbol'];
        }
        $side = null;
        $takerOrMaker = null;
        $orderId = null;
        if (is_array($trade) && array_key_exists('m', $trade)) {
            $side = $trade['m'] ? 'sell' : 'buy'; // this is reversed intentionally
            $takerOrMaker = $trade['m'] ? 'maker' : 'taker';
        }
        return array(
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'symbol' => $symbol,
            'id' => $id,
            'order' => $orderId,
            'type' => null,
            'takerOrMaker' => $takerOrMaker,
            'side' => $side,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'fee' => null,
        );
    }

    public function handle_trade($client, $message) {
        // the $trade streams push raw $trade information in real-time
        // each $trade has a unique buyer and seller
        $marketId = $this->safe_string($message, 's');
        $market = null;
        $symbol = $marketId;
        if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
            $market = $this->markets_by_id[$marketId];
            $symbol = $market['symbol'];
        }
        $lowerCaseId = $this->safe_string_lower($message, 's');
        $event = $this->safe_string($message, 'e');
        $messageHash = $lowerCaseId . '@' . $event;
        $trade = $this->parse_trade($message, $market);
        $array = $this->safe_value($this->trades, $symbol, $array());
        $array[] = $trade;
        $length = is_array($array) ? count($array) : 0;
        if ($length > $this->options['tradesLimit']) {
            array_shift($array);
        }
        $this->trades[$symbol] = $array;
        $client->resolve ($array, $messageHash);
    }

    public function watch_ohlcv($symbol, $timeframe = '1m', $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market($symbol);
        $marketId = $market['lowercaseId'];
        $interval = $this->timeframes[$timeframe];
        $name = 'kline';
        $messageHash = $marketId . '@' . $name . '_' . $interval;
        $future = $this->watch_public($messageHash, $params);
        return $this->after($future, array($this, 'filter_by_since_limit'), $since, $limit, 0, true);
    }

    public function find_timeframe($timeframe) {
        // redo to use reverse lookups in a static map instead
        $keys = is_array($this->timeframes) ? array_keys($this->timeframes) : array();
        for ($i = 0; $i < count($keys); $i++) {
            $key = $keys[$i];
            if ($this->timeframes[$key] === $timeframe) {
                return $key;
            }
        }
        return null;
    }

    public function handle_ohlcv($client, $message) {
        //
        //     {
        //         e => 'kline',
        //         E => 1579482921215,
        //         s => 'ETHBTC',
        //         k => {
        //             t => 1579482900000,
        //             T => 1579482959999,
        //             s => 'ETHBTC',
        //             i => '1m',
        //             f => 158411535,
        //             L => 158411550,
        //             o => '0.01913200',
        //             c => '0.01913500',
        //             h => '0.01913700',
        //             l => '0.01913200',
        //             v => '5.08400000',
        //             n => 16,
        //             x => false,
        //             q => '0.09728060',
        //             V => '3.30200000',
        //             Q => '0.06318500',
        //             B => '0'
        //         }
        //     }
        //
        $marketId = $this->safe_string($message, 's');
        $lowercaseMarketId = $this->safe_string_lower($message, 's');
        $event = $this->safe_string($message, 'e');
        $kline = $this->safe_value($message, 'k');
        $interval = $this->safe_string($kline, 'i');
        // use a reverse lookup in a static map instead
        $timeframe = $this->find_timeframe($interval);
        $messageHash = $lowercaseMarketId . '@' . $event . '_' . $interval;
        $parsed = array(
            $this->safe_integer($kline, 't'),
            $this->safe_float($kline, 'o'),
            $this->safe_float($kline, 'h'),
            $this->safe_float($kline, 'l'),
            $this->safe_float($kline, 'c'),
            $this->safe_float($kline, 'v'),
        );
        $symbol = $marketId;
        if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
            $market = $this->markets_by_id[$marketId];
            $symbol = $market['symbol'];
        }
        $this->ohlcvs[$symbol] = $this->safe_value($this->ohlcvs, $symbol, array());
        $stored = $this->safe_value($this->ohlcvs[$symbol], $timeframe, array());
        $length = is_array($stored) ? count($stored) : 0;
        if ($length && $parsed[0] === $stored[$length - 1][0]) {
            $stored[$length - 1] = $parsed;
        } else {
            $stored[] = $parsed;
            $limit = $this->safe_integer($this->options, 'OHLCVLimit', 1000);
            if ($length >= $limit) {
                array_shift($stored);
            }
        }
        $this->ohlcvs[$symbol][$timeframe] = $stored;
        $client->resolve ($stored, $messageHash);
    }

    public function watch_public($messageHash, $params = array ()) {
        $defaultType = $this->safe_string_2($this->options, 'watchOrderBook', 'defaultType', 'spot');
        $type = $this->safe_string($params, 'type', $defaultType);
        $query = $this->omit($params, 'type');
        $url = $this->urls['api']['ws'][$type];
        $requestId = $this->request_id($url);
        $request = array(
            'method' => 'SUBSCRIBE',
            'params' => array(
                $messageHash,
            ),
            'id' => $requestId,
        );
        $subscribe = array(
            'id' => $requestId,
        );
        return $this->watch($url, $messageHash, array_merge($request, $query), $messageHash, $subscribe);
    }

    public function watch_ticker($symbol, $params = array ()) {
        $this->load_markets();
        $market = $this->market($symbol);
        $marketId = $market['lowercaseId'];
        $name = 'ticker';
        $messageHash = $marketId . '@' . $name;
        return $this->watch_public($messageHash, $params);
    }

    public function handle_ticker($client, $message) {
        //
        // 24hr rolling window ticker statistics for a single $symbol
        // These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs
        // Update Speed 1000ms
        //
        //     {
        //         e => '24hrTicker',      // $event type
        //         E => 1579485598569,     // $event time
        //         s => 'ETHBTC',          // $symbol
        //         p => '-0.00004000',     // price change
        //         P => '-0.209',          // price change percent
        //         w => '0.01920495',      // weighted average price
        //         x => '0.01916500',      // the price of the first trade before the 24hr rolling window
        //         c => '0.01912500',      // $last (closing) price
        //         Q => '0.10400000',      // $last quantity
        //         b => '0.01912200',      // best bid
        //         B => '4.10400000',      // best bid quantity
        //         a => '0.01912500',      // best ask
        //         A => '0.00100000',      // best ask quantity
        //         o => '0.01916500',      // open price
        //         h => '0.01956500',      // high price
        //         l => '0.01887700',      // low price
        //         v => '173518.11900000', // base volume
        //         q => '3332.40703994',   // quote volume
        //         O => 1579399197842,     // open time
        //         C => 1579485597842,     // close time
        //         F => 158251292,         // first trade id
        //         L => 158414513,         // $last trade id
        //         n => 163222,            // total number of trades
        //     }
        //
        $event = 'ticker'; // $message['e'] === 24hrTicker
        $wsMarketId = $this->safe_string_lower($message, 's');
        $messageHash = $wsMarketId . '@' . $event;
        $timestamp = $this->safe_integer($message, 'C');
        $symbol = null;
        $marketId = $this->safe_string($message, 's');
        if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
            $market = $this->markets_by_id[$marketId];
            $symbol = $market['symbol'];
        }
        $last = $this->safe_float($message, 'c');
        $result = array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'high' => $this->safe_float($message, 'h'),
            'low' => $this->safe_float($message, 'l'),
            'bid' => $this->safe_float($message, 'b'),
            'bidVolume' => $this->safe_float($message, 'B'),
            'ask' => $this->safe_float($message, 'a'),
            'askVolume' => $this->safe_float($message, 'A'),
            'vwap' => $this->safe_float($message, 'w'),
            'open' => $this->safe_float($message, 'o'),
            'close' => $last,
            'last' => $last,
            'previousClose' => $this->safe_float($message, 'x'), // previous day close
            'change' => $this->safe_float($message, 'p'),
            'percentage' => $this->safe_float($message, 'P'),
            'average' => null,
            'baseVolume' => $this->safe_float($message, 'v'),
            'quoteVolume' => $this->safe_float($message, 'q'),
            'info' => $message,
        );
        $this->tickers[$symbol] = $result;
        $client->resolve ($result, $messageHash);
    }

    public function authenticate() {
        $time = $this->seconds();
        $lastAuthenticatedTime = $this->safe_integer($this->options, 'lastAuthenticatedTime', 0);
        if ($time - $lastAuthenticatedTime > 1800) {
            $type = $this->safe_string_2($this->options, 'defaultType', 'spot');
            $method = ($type === 'future') ? 'fapiPrivatePostListenKey' : 'publicPostUserDataStream';
            $response = $this->$method ();
            $this->options['listenKey'] = $this->safe_string($response, 'listenKey');
            $this->options['lastAuthenticatedTime'] = $time;
        }
    }

    public function watch_balance($params = array ()) {
        $this->load_markets();
        $this->authenticate();
        $defaultType = $this->safe_string_2($this->options, 'watchBalance', 'defaultType', 'spot');
        $type = $this->safe_string($params, 'type', $defaultType);
        $query = $this->omit($params, 'type');
        $url = $this->urls['api']['ws'][$type] . '/' . $this->options['listenKey'];
        $requestId = $this->request_id($url);
        $request = array(
            'method' => 'SUBSCRIBE',
            'params' => array(
            ),
            'id' => $requestId,
        );
        $subscribe = array(
            'id' => $requestId,
        );
        $messageHash = 'outboundAccountInfo';
        return $this->watch($url, $messageHash, array_merge($request, $query), 1, $subscribe);
    }

    public function handle_balance($client, $message) {
        // sent upon creating or filling an order
        //
        // {
        //   "e" => "outboundAccountInfo",   // Event type
        //   "E" => 1499405658849,           // Event time
        //   "m" => 0,                       // Maker commission rate (bips)
        //   "t" => 0,                       // Taker commission rate (bips)
        //   "b" => 0,                       // Buyer commission rate (bips)
        //   "s" => 0,                       // Seller commission rate (bips)
        //   "T" => true,                    // Can trade?
        //   "W" => true,                    // Can withdraw?
        //   "D" => true,                    // Can deposit?
        //   "u" => 1499405658848,           // Time of last $account update
        //   "B" => array(                        // Balances array
        //     array(
        //       "a" => "LTC",               // Asset
        //       "f" => "17366.18538083",    // Free amount
        //       "l" => "0.00000000"         // Locked amount
        //     ),
        //     array(
        //       "a" => "BTC",
        //       "f" => "10537.85314051",
        //       "l" => "2.19464093"
        //     ),
        //     array(
        //       "a" => "ETH",
        //       "f" => "17902.35190619",
        //       "l" => "0.00000000"
        //     ),
        //   )
        // }
        $balances = $this->safe_value($message, 'B', array());
        for ($i = 0; $i < count($balances); $i++) {
            $balance = $balances[$i];
            $currencyId = $this->safe_string($balance, 'a');
            $code = $this->safe_currency_code($currencyId);
            $account = $this->account();
            $account['free'] = $this->safe_float($balance, 'f');
            $account['used'] = $this->safe_float($balance, 'l');
            $this->balance[$code] = $account;
        }
        $this->balance = $this->parse_balance($this->balance);
        $messageHash = $this->safe_string($message, 'e');
        $client->resolve ($this->balance, $messageHash);
    }

    public function watch_orders($params = array ()) {
        $this->load_markets();
        $this->authenticate();
        $defaultType = $this->safe_string_2($this->options, 'watchOrders', 'defaultType', 'spot');
        $type = $this->safe_string($params, 'type', $defaultType);
        $query = $this->omit($params, 'type');
        $url = $this->urls['api']['ws'][$type] . '/' . $this->options['listenKey'];
        $requestId = $this->request_id($url);
        $request = array(
            'method' => 'SUBSCRIBE',
            'params' => array(
            ),
            'id' => $requestId,
        );
        $subscribe = array(
            'id' => $requestId,
        );
        $messageHash = 'executionReport';
        return $this->watch($url, $messageHash, array_merge($request, $query), 1, $subscribe);
    }

    public function handle_order($client, $message) {
        // {
        //   "e" => "executionReport",        // Event $type
        //   "E" => 1499405658658,            // Event time
        //   "s" => "ETHBTC",                 // Symbol
        //   "c" => "mUvoqJxFIILMdfAW5iGSOW", // Client order ID
        //   "S" => "BUY",                    // Side
        //   "o" => "LIMIT",                  // Order $type
        //   "f" => "GTC",                    // Time in force
        //   "q" => "1.00000000",             // Order quantity
        //   "p" => "0.10264410",             // Order $price
        //   "P" => "0.00000000",             // Stop $price
        //   "F" => "0.00000000",             // Iceberg quantity
        //   "g" => -1,                       // OrderListId
        //   "C" => null,                     // Original $client order ID; This is the ID of the order being canceled
        //   "x" => "NEW",                    // Current execution $type
        //   "X" => "NEW",                    // Current order $status
        //   "r" => "NONE",                   // Order reject reason; will be an error code.
        //   "i" => 4293153,                  // Order ID
        //   "l" => "0.00000000",             // Last executed quantity
        //   "z" => "0.00000000",             // Cumulative $filled quantity
        //   "L" => "0.00000000",             // Last executed $price
        //   "n" => "0",                      // Commission $amount
        //   "N" => null,                     // Commission asset
        //   "T" => 1499405658657,            // Transaction time
        //   "t" => -1,                       // Trade ID
        //   "I" => 8641984,                  // Ignore
        //   "w" => true,                     // Is the order on the book?
        //   "m" => false,                    // Is this trade the maker $side?
        //   "M" => false,                    // Ignore
        //   "O" => 1499405658657,            // Order creation time
        //   "Z" => "0.00000000",             // Cumulative quote asset transacted quantity
        //   "Y" => "0.00000000"              // Last quote asset transacted quantity (i.e. lastPrice * lastQty),
        //   "Q" => "0.00000000"              // Quote Order Qty
        // }
        $messageHash = $this->safe_string($message, 'e');
        $orderId = $this->safe_string($message, 'i');
        $marketId = $this->safe_string($message, 's');
        $symbol = $marketId;
        if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
            $market = $this->markets_by_id[$marketId];
            $symbol = $market['symbol'];
        }
        $timestamp = $this->safe_string($message, 'O');
        $lastTradeTimestamp = $this->safe_string($message, 'T');
        $feeAmount = $this->safe_float($message, 'n');
        $feeCurrency = $this->safe_currency_code($this->safe_string($message, 'N'));
        $fee = array(
            'cost' => $feeAmount,
            'currency' => $feeCurrency,
        );
        $price = $this->safe_float($message, 'p');
        $amount = $this->safe_float($message, 'q');
        $side = $this->safe_string_lower($message, 'S');
        $type = $this->safe_string_lower($message, 'o');
        $filled = $this->safe_float($message, 'z');
        $cumulativeQuote = $this->safe_float($message, 'Z');
        $remaining = $amount;
        $average = null;
        $cost = null;
        if ($filled !== null) {
            if ($price !== null) {
                $cost = $filled * $price;
            }
            if ($amount !== null) {
                $remaining = max ($amount - $filled, 0);
            }
            if (($cumulativeQuote !== null) && ($filled > 0)) {
                $average = $cumulativeQuote / $filled;
            }
        }
        $rawStatus = $this->safe_string($message, 'X');
        $status = $this->parse_order_status($rawStatus);
        $trades = null;
        $parsed = array(
            'info' => $message,
            'symbol' => $symbol,
            'id' => $orderId,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'lastTradeTimestamp' => $lastTradeTimestamp,
            'type' => $type,
            'side' => $side,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'average' => $average,
            'filled' => $filled,
            'remaining' => $remaining,
            'status' => $status,
            'fee' => $fee,
            'trades' => $trades,
        );
        $client->resolve ($parsed, $messageHash);
    }

    public function handle_message($client, $message) {
        $methods = array(
            'depthUpdate' => array($this, 'handle_order_book'),
            'trade' => array($this, 'handle_trade'),
            'kline' => array($this, 'handle_ohlcv'),
            '24hrTicker' => array($this, 'handle_ticker'),
            'outboundAccountInfo' => array($this, 'handle_balance'),
            'executionReport' => array($this, 'handle_order'),
        );
        $event = $this->safe_string($message, 'e');
        $method = $this->safe_value($methods, $event);
        if ($method === null) {
            $requestId = $this->safe_string($message, 'id');
            if ($requestId !== null) {
                return $this->handle_subscription_status($client, $message);
            }
            return $message;
        } else {
            return $method($client, $message);
        }
    }
}
