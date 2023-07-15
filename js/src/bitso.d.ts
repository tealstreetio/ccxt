import { Exchange } from './base/Exchange.js';
export default class bitso extends Exchange {
    describe(): any;
    fetchLedger(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseLedgerEntryType(type: any): string;
    parseLedgerEntry(item: any, currency?: any): {
        id: string;
        timestamp: number;
        datetime: string;
        direction: string;
        account: string;
        referenceId: string;
        referenceAccount: string;
        type: string;
        currency: any;
        amount: number;
        before: number; /**
         * @method
         * @name bitso#fetchDepositWithdrawFees
         * @description fetch deposit and withdraw fees
         * @see https://bitso.com/api_info#fees
         * @param {[string]|undefined} codes list of unified currency codes
         * @param {object} params extra parameters specific to the bitso api endpoint
         * @returns {[object]} a list of [fee structures]{@link https://docs.ccxt.com/#/?id=fee-structure}
         */
        after: number;
        status: string;
        fee: any;
        info: object;
    };
    fetchMarkets(params?: {}): Promise<any[]>;
    parseBalance(response: any): import("./base/types.js").Balances;
    fetchBalance(params?: {}): Promise<import("./base/types.js").Balances>;
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    fetchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").OHLCV[]>;
    parseOHLCV(ohlcv: any, market?: any, timeframe?: string): number[];
    parseTrade(trade: any, market?: any): import("./base/types.js").Trade;
    fetchTrades(symbol: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchTradingFees(params?: {}): Promise<{}>;
    fetchMyTrades(symbol?: string, since?: any, limit?: number, params?: {}): Promise<import("./base/types.js").Trade[]>;
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    cancelOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    cancelOrders(ids: any, symbol?: string, params?: {}): Promise<any[]>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<any[]>;
    parseOrderStatus(status: any): string;
    parseOrder(order: any, market?: any): any;
    fetchOpenOrders(symbol?: string, since?: any, limit?: number, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    fetchOrderTrades(id: any, symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchDeposit(id: any, code?: any, params?: {}): Promise<{
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: string;
        address: string;
        addressTo: string;
        amount: string;
        type: string;
        currency: any;
        status: string;
        updated: any;
        tagFrom: any;
        tag: any;
        tagTo: any;
        comment: any;
        fee: any;
        info: any;
    }>;
    fetchDeposits(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchDepositAddress(code: any, params?: {}): Promise<{
        currency: any;
        address: string;
        tag: any;
        network: any;
        info: any;
    }>;
    fetchTransactionFees(codes?: string[], params?: {}): Promise<{}>;
    fetchDepositWithdrawFees(codes?: string[], params?: {}): Promise<{}>;
    parseDepositWithdrawFees(response: any, codes?: string[], currencyIdKey?: any): {};
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: string;
        address: string;
        addressTo: string;
        amount: string;
        type: string;
        currency: any;
        status: string;
        updated: any;
        tagFrom: any;
        tag: any;
        tagTo: any;
        comment: any;
        fee: any;
        info: any;
    }>;
    safeNetwork(networkId: any): string;
    parseTransaction(transaction: any, currency?: any): {
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: string;
        address: string;
        addressTo: string;
        amount: string;
        type: string;
        currency: any;
        status: string;
        updated: any;
        tagFrom: any;
        tag: any;
        tagTo: any;
        comment: any;
        fee: any;
        info: any;
    };
    parseTransactionStatus(status: any): string;
    sign(path: any, api?: any, method?: string, params?: {}, headers?: any, body?: any): {
        url: string;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(httpCode: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): void;
}
