SELECT 
    TROUBLE_REPORT_EVENT_TYPE_KEY,
    EVENT_TYPE,
    MD_UPD_TS,
    MD_INS_TS,
    MD_CURR_FLAG
FROM ODW_TROUBLE_REPORT_EVENT_TYPE_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);
