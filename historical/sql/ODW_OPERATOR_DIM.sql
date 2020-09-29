SELECT 
    MD_UPD_ACTUAL_BATCH_ID,
    MD_UPD_INITIAL_BATCH_ID,
    MD_INS_ACTUAL_BATCH_ID,
    MD_INS_INITIAL_BATCH_ID,
    OPERATOR_KEY,
    PARENT_OPERATOR_CODE,
    RADIUS_DOMAIN,
    NETSTREAM_OPERATOR_CODE,
    OPERATOR_DESCRIPTION,
    OPERATOR_CODE,
    MD_UPD_TS,
    MD_INS_TS,
    MD_EFFCTV_TO_TS,
    MD_EFFCTV_FROM_TS,
    MD_CURR_FLAG
FROM ODW_OPERATOR_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);