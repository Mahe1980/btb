SELECT
    BTB_BILL_YEAR_KEY,
    BILL_YEAR,
    MD_BATCH_ID,
    MD_INS_TS
FROM ODW_BTB_BILL_YEAR_LU
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
);
