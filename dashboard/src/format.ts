export const CURRENCY_SYMBOL = "$"; // change to your store currency

export const fmtNum = (n: number) => Math.round(n).toLocaleString("en-US");
export const fmtMoney = (n: number) => `${CURRENCY_SYMBOL}${Math.round(n).toLocaleString("en-US")}`;
export const fmtPct = (ratio: number) => `${(ratio * 100).toFixed(1)}%`;