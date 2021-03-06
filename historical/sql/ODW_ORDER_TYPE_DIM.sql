SELECT 
    ORDER_TYPE_KEY,
    PROVIDE_REQUEST_TYPE,
    ACQUISITION_TYPE,
    ORDER_TYPE_CODE,
    PARENT_ORDER_TYPE_CODE,
    MD_INS_TS,
    MD_CURR_FLAG
FROM ODW_ORDER_TYPE_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
);
