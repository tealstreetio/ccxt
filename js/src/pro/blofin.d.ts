import blofinRest from '../blofin.js';
export default class blofin extends blofinRest {
    describe(): any;
    requestId(url: any): any;
    subscribe(access: any, channel: any, symbol: any, params?: {}, shouldThrottle?: boolean): Promise<any>;
    watchTrades(symbol: any, since?: any, limit?: any, params?: {}): Promise<any>;
    handleTrades(client: any, message: any): any;
    watchTicker(symbol: any, params?: {}): Promise<any>;
    handleTicker(client: any, message: any): any;
    watchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    handleOHLCV(client: any, message: any): void;
    watchOrderBook(symbol: any, limit?: any, params?: {}): Promise<any>;
    handleDelta(bookside: any, delta: any): void;
    handleDeltas(bookside: any, deltas: any): void;
    handleOrderBookMessage(client: any, message: any, orderbook: any, messageHash: any): any;
    handleOrderBook(client: any, message: any): any;
    checkRequiredUid(): boolean;
    authenticate(params?: {}): any;
    watchPrivate(messageHash: any, message: any, params?: {}): Promise<any>;
    watchOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseWsOrder(order: any, market?: any): any;
    handleOrderUpdate(client: any, message: any): void;
    handleOrder(client: any, message: any): void;
    handleMessage(client: any, message: any): any;
    ping(client: any): string;
    handlePong(client: any, message: any): any;
    handleErrorMessage(client: any, message: any): any;
    handleSubscribe(client: any, message: any): any;
    handleAuth(client: any, message: any): void;
}
