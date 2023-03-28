export = BigInteger;
declare function BigInteger(a: any, b: any): void;
declare class BigInteger {
    constructor(a: any, b: any);
    am: typeof am3;
    DB: number;
    DM: number;
    DV: number;
    FV: number;
    F1: number;
    F2: number;
    copyTo: typeof bnpCopyTo;
    fromInt: typeof bnpFromInt;
    fromString: typeof bnpFromString;
    fromByteArray: typeof bnpFromByteArray;
    fromBuffer: typeof bnpFromBuffer;
    clamp: typeof bnpClamp;
    dlShiftTo: typeof bnpDLShiftTo;
    drShiftTo: typeof bnpDRShiftTo;
    lShiftTo: typeof bnpLShiftTo;
    rShiftTo: typeof bnpRShiftTo;
    subTo: typeof bnpSubTo;
    multiplyTo: typeof bnpMultiplyTo;
    squareTo: typeof bnpSquareTo;
    divRemTo: typeof bnpDivRemTo;
    invDigit: typeof bnpInvDigit;
    isEven: typeof bnpIsEven;
    exp: typeof bnpExp;
    chunkSize: typeof bnpChunkSize;
    toRadix: typeof bnpToRadix;
    fromRadix: typeof bnpFromRadix;
    bitwiseTo: typeof bnpBitwiseTo;
    addTo: typeof bnpAddTo;
    dMultiply: typeof bnpDMultiply;
    dAddOffset: typeof bnpDAddOffset;
    multiplyLowerTo: typeof bnpMultiplyLowerTo;
    multiplyUpperTo: typeof bnpMultiplyUpperTo;
    toString: typeof bnToString;
    negate: typeof bnNegate;
    abs: typeof bnAbs;
    compareTo: typeof bnCompareTo;
    bitLength: typeof bnBitLength;
    mod: typeof bnMod;
    clone: typeof bnClone;
    intValue: typeof bnIntValue;
    signum: typeof bnSigNum;
    toByteArray: typeof bnToByteArray;
    toBuffer: typeof bnToBuffer;
    equals: typeof bnEquals;
    min: typeof bnMin;
    max: typeof bnMax;
    and: typeof bnAnd;
    or: typeof bnOr;
    xor: typeof bnXor;
    not: typeof bnNot;
    getLowestSetBit: typeof bnGetLowestSetBit;
    add: typeof bnAdd;
    subtract: typeof bnSubtract;
    multiply: typeof bnMultiply;
    divide: typeof bnDivide;
    remainder: typeof bnRemainder;
    modPow: typeof bnModPow;
    pow: typeof bnPow;
    gcd: typeof bnGCD;
    square: typeof bnSquare;
}
declare namespace BigInteger {
    export { int2char };
    export const ZERO: BigInteger;
    export const ONE: BigInteger;
}
declare function am3(i: any, x: any, w: any, j: any, c: any, n: any): any;
declare function bnpCopyTo(r: any): void;
declare function bnpFromInt(x: any): void;
declare class bnpFromInt {
    constructor(x: any);
    t: number;
    s: number;
    0: any;
}
declare function bnpFromString(data: any, radix: any, unsigned: any): void;
declare class bnpFromString {
    constructor(data: any, radix: any, unsigned: any);
    t: number;
    s: number;
}
declare function bnpFromByteArray(a: any, unsigned: any): void;
declare function bnpFromBuffer(a: any): void;
declare function bnpClamp(): void;
declare function bnpDLShiftTo(n: any, r: any): void;
declare function bnpDRShiftTo(n: any, r: any): void;
declare function bnpLShiftTo(n: any, r: any): void;
declare function bnpRShiftTo(n: any, r: any): void;
declare function bnpSubTo(a: any, r: any): void;
declare function bnpMultiplyTo(a: any, r: any): void;
declare function bnpSquareTo(r: any): void;
declare function bnpDivRemTo(m: any, q: any, r: any): void;
declare function bnpInvDigit(): number;
declare function bnpIsEven(): boolean;
declare function bnpExp(e: any, z: any): any;
declare function bnpChunkSize(r: any): number;
declare function bnpToRadix(b: any): string;
declare function bnpFromRadix(s: any, b: any): void;
declare function bnpBitwiseTo(a: any, op: any, r: any): void;
declare function bnpAddTo(a: any, r: any): void;
declare function bnpDMultiply(n: any): void;
declare class bnpDMultiply {
    constructor(n: any);
}
declare function bnpDAddOffset(n: any, w: any): void;
declare class bnpDAddOffset {
    constructor(n: any, w: any);
}
declare function bnpMultiplyLowerTo(a: any, n: any, r: any): void;
declare function bnpMultiplyUpperTo(a: any, n: any, r: any): void;
declare function bnToString(b: any): any;
declare function bnNegate(): BigInteger;
declare function bnAbs(): any;
declare function bnCompareTo(a: any): number;
declare function bnBitLength(): number;
declare function bnMod(a: any): BigInteger;
declare function bnClone(): BigInteger;
declare function bnIntValue(): any;
declare function bnSigNum(): 0 | 1 | -1;
declare function bnToByteArray(): any[];
/**
 * return Buffer object
 * @param trim {boolean} slice buffer if first element == 0
 * @returns {Buffer}
 */
declare function bnToBuffer(trimOrSize: any): Buffer;
declare function bnEquals(a: any): boolean;
declare function bnMin(a: any): any;
declare function bnMax(a: any): any;
declare function bnAnd(a: any): BigInteger;
declare function bnOr(a: any): BigInteger;
declare function bnXor(a: any): BigInteger;
declare function bnNot(): BigInteger;
declare function bnGetLowestSetBit(): number;
declare function bnAdd(a: any): BigInteger;
declare function bnSubtract(a: any): BigInteger;
declare function bnMultiply(a: any): BigInteger;
declare function bnDivide(a: any): BigInteger;
declare function bnRemainder(a: any): BigInteger;
declare function bnModPow(e: any, m: any): any;
declare function bnPow(e: any): any;
declare function bnGCD(a: any): any;
declare function bnSquare(): BigInteger;
declare function int2char(n: any): string;
