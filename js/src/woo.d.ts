import { Exchange } from './base/Exchange.js';
export default class woo extends Exchange {
    describe(): any;
    fetchMarkets(params?: {}): Promise<any[]>;
    fetchTrades(symbol: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    parseTrade(trade: any, market?: any): import("./base/types.js").Trade;
    parseTokenAndFeeTemp(item: any, feeTokenKey: any, feeAmountKey: any): any;
    fetchTradingFees(params?: {}): Promise<{}>;
    fetchCurrencies(params?: {}): Promise<{}>;
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    editOrder(id: any, symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    maybeAlgoOrderId(id: any): boolean;
    cancelOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    cancelAlgoOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    cancelRegularOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<any>;
    fetchOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    fetchOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    parseTimeInForce(timeInForce: any): string;
    parseOrderType(type: any, algoType?: any): string;
    parseOrder(order: any, market?: any): any;
    parseRegularOrder(order: any, market?: any): any;
    parseAlgoOrder(order: any, market?: any): any;
    parseOrderStatus(status: any): any;
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    fetchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<any[]>;
    parseOHLCV(ohlcv: any, market?: any): number[];
    fetchOrderTrades(id: any, symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchMyTrades(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchAccounts(params?: {}): Promise<any[]>;
    parseAccount(account: any): {
        info: any;
        id: string;
        name: string;
        code: any;
        type: string;
    };
    fetchBalance(params?: {}): Promise<import("./base/types.js").Balances>;
    parseBalance(response: any): import("./base/types.js").Balances;
    fetchDepositAddress(code: any, params?: {}): Promise<{
        currency: any;
        address: string;
        tag: string;
        network: string;
        info: any;
    }>;
    getAssetHistoryRows(code?: string, since?: any, limit?: any, params?: {}): Promise<any[]>;
    fetchLedger(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseLedgerEntry(item: any, currency?: any): {
        id: string;
        currency: any;
        account: string;
        referenceAccount: any;
        referenceId: string;
        status: string;
        amount: number;
        before: any;
        after: any;
        fee: any;
        direction: string;
        timestamp: number;
        datetime: string;
        type: string;
        info: any;
    };
    parseLedgerEntryType(type: any): string;
    getCurrencyFromChaincode(networkizedCode: any, currency: any): any;
    fetchDeposits(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchWithdrawals(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchTransactions(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseTransaction(transaction: any, currency?: any): {
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        address: any;
        addressFrom: string;
        addressTo: string;
        tag: string;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: any;
        info: any;
    };
    parseTransactionStatus(status: any): string;
    transfer(code: any, amount: any, fromAccount: any, toAccount: any, params?: {}): Promise<{
        id: string;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: number;
        fromAccount: any;
        toAccount: any;
        status: string;
        info: any;
    }>;
    fetchTransfers(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseTransfer(transfer: any, currency?: any): {
        id: string;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: number;
        fromAccount: any;
        toAccount: any;
        status: string;
        info: any;
    };
    parseTransferStatus(status: any): string;
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        address: any;
        addressFrom: string;
        addressTo: string;
        tag: string;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: any;
        info: any;
    }>;
    repayMargin(code: any, amount: any, symbol?: string, params?: {}): Promise<any>;
    parseMarginLoan(info: any, currency?: any): {
        id: any;
        currency: any;
        amount: any;
        symbol: any;
        timestamp: any;
        datetime: any;
        info: any;
    };
    nonce(): number;
    sign(path: any, section?: string, method?: string, params?: {}, headers?: any, body?: any): {
        url: any;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(httpCode: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): void;
    parseIncome(income: any, market?: any): {
        info: any;
        symbol: any;
        code: any;
        timestamp: number;
        datetime: string;
        id: string;
        amount: number;
        rate: number;
    };
    fetchFundingHistory(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseFundingRate(fundingRate: any, market?: any): {
        info: any;
        symbol: any;
        markPrice: any;
        indexPrice: any;
        interestRate: number;
        estimatedSettlePrice: any;
        timestamp: number;
        datetime: string;
        fundingRate: number;
        fundingTimestamp: number;
        fundingDatetime: string;
        nextFundingRate: any;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: number;
        previousFundingTimestamp: number;
        previousFundingDatetime: string;
    };
    fetchFundingRate(symbol: any, params?: {}): Promise<{
        info: any;
        symbol: any;
        markPrice: any;
        indexPrice: any;
        interestRate: number;
        estimatedSettlePrice: any;
        timestamp: number;
        datetime: string;
        fundingRate: number;
        fundingTimestamp: number;
        fundingDatetime: string;
        nextFundingRate: any;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: number;
        previousFundingTimestamp: number;
        previousFundingDatetime: string;
    }>;
    fetchFundingRates(symbols?: string[], params?: {}): Promise<any>;
    fetchFundingRateHistory(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchLeverage(symbol: any, params?: {}): Promise<{
        info: any;
        leverage: number;
    }>;
    setLeverage(leverage: any, symbol?: string, params?: {}): Promise<any>;
    fetchPosition(symbol?: string, params?: {}): Promise<{
        info: any;
        id: string;
        symbol: any;
        notional: any;
        marginMode: string;
        liquidationPrice: number;
        entryPrice: number;
        realizedPnl: string;
        unrealizedPnl: number;
        percentage: any;
        contracts: number;
        contractSize: number;
        markPrice: number;
        side: any;
        hedged: boolean;
        timestamp: number;
        datetime: string;
        maintenanceMargin: any;
        maintenanceMarginPercentage: any;
        collateral: any;
        initialMargin: any;
        initialMarginPercentage: any;
        leverage: any;
        marginRatio: any;
    }>;
    fetchPositions(symbols?: string[], params?: {}): Promise<any>;
    parsePosition(position: any, market?: any): {
        info: any;
        id: string;
        symbol: any;
        notional: any;
        marginMode: string;
        liquidationPrice: number;
        entryPrice: number;
        realizedPnl: string;
        unrealizedPnl: number;
        percentage: any;
        contracts: number;
        contractSize: number;
        markPrice: number;
        side: any;
        hedged: boolean;
        timestamp: number;
        datetime: string;
        maintenanceMargin: any;
        maintenanceMarginPercentage: any;
        collateral: any;
        initialMargin: any;
        initialMarginPercentage: any;
        leverage: any;
        marginRatio: any;
    };
    defaultNetworkCodeForCurrency(code: any): any;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchAccountConfiguration(symbol: any, params?: {}): Promise<{
        marginMode: string;
        positionMode: string;
        markets: {};
        leverage: number;
    }>;
}
