SELECT 
    STATUS,
    MD_INS_TS,
    SPM_STATUS_KEY
FROM ODW_SPM_STATUS_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
);
