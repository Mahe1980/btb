SELECT 
    BTB_PRICE_LIST_KEY,
    ACCOUNTCODE2_UNIT_PRICE,
    UNIT_PRICE,
    MODIFIED_BY,
    NOTES,
    CODING_CATEGORY,
    ACCOUNTCODE2,
    ACCOUNTCODE1,
    PRICE_UNIT,
    CHARGE_DESCRIPTION,
    CHARGE_CODE,
    CHARGE_SUB_TYPE,
    CHARGE_TYPE,
    RECORD_TYPE,
    BILL_ACCOUNT_CODE,
    SERVICE_TYPE,
    SUBSTR(EFFECTIVE_END_DATE,1,10) AS EFFECTIVE_END_DATE,
    SUBSTR(EFFECTIVE_START_DATE,1,10) AS EFFECTIVE_START_DATE,
    MD_UPD_TS,
    MD_INS_TS,
    MD_EFFCTV_TO_TS,
    MD_EFFCTV_FROM_TS,
    LAST_MODIFIED_DATE,
    MD_CURR_FLAG
FROM ODW_BTB_PRICE_LIST
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);
