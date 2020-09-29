SELECT 
    MD_UPD_ACTUAL_BATCH_ID,
    MD_UPD_INITIAL_BATCH_ID,
    MD_INS_ACTUAL_BATCH_ID,
    MD_INS_INITIAL_BATCH_ID,
    SERVICE_ID,
    SERVICE_PROBLEM_ID,
    SPM_SERVICE_PROBLEM_KEY,
    RESOLUTION_REASON_DESC,
    RESOLUTION_REASON_CODE,
    CAUSE_DESC,
    CAUSE_CODE,
    FAULT_DESC,
    FAULT_CODE,
    CONTACT_ACCOUNT_NUMBER,
    CONTACT_PHONE,
    CONTACT_NAME,
    DIRECTORY_NUMBER,
    PROBLEM_CATEGORY_DESC,
    PROBLEM_CATEGORY_CODE,
    OPERATOR_REFERENCE,
    OPERATOR_ID,
    SERVICE_TYPE,
    MD_UPD_TS,
    MD_INS_TS,
    MD_EFFCTV_TO_TS,
    MD_EFFCTV_FROM_TS,
    CLOSED_DATE,
    LAST_CLEARED_DATE,
    FIRST_CLEARED_DATE,
    OPENED_DATE,
    MLT_REQUESTED,
    MD_CURR_FLAG
FROM ODW_SPM_SERVICE_PROBLEM_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);