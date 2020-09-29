SELECT 
    MD_INS_BATCH_ID,
    APPOINTMENT_RESERVATION_KEY,
    TROUBLE_REPORT_KEY,
    LINE_TEST_KEY,
    SPM_SERVICE_PROBLEM_KEY,
    MD_INS_TS
FROM ODW_SPM_TR_LT_AP_LINK_FACT
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
);
