export const pkcs1: {
    privateExport: (key: any, options: any) => any;
    privateImport: (key: any, data: any, options: any) => void;
    publicExport: (key: any, options: any) => any;
    publicImport: (key: any, data: any, options: any) => void;
    autoImport: (key: any, data: any) => boolean;
};
export const pkcs8: {
    privateExport: (key: any, options: any) => any;
    privateImport: (key: any, data: any, options: any) => void;
    publicExport: (key: any, options: any) => any;
    publicImport: (key: any, data: any, options: any) => void;
    autoImport: (key: any, data: any) => boolean;
};
export const components: {
    privateExport: (key: any, options: any) => {
        n: any;
        e: any;
        d: any;
        p: any;
        q: any;
        dmp1: any;
        dmq1: any;
        coeff: any;
    };
    privateImport: (key: any, data: any, options: any) => void;
    publicExport: (key: any, options: any) => {
        n: any;
        e: any;
    };
    publicImport: (key: any, data: any, options: any) => void;
    autoImport: (key: any, data: any) => boolean;
};
export function detectAndImport(key: any, data: any, format: any): boolean;
