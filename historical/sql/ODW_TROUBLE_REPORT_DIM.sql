SELECT 
    UPPER_TRC_BAND,
    CONFIRM_EQUIP_DISC_REQUESTED,
    AMEND_REQUESTED,
    CANCEL_REQUESTED,
    SERVICE_PROBLEM_ID,
    TROUBLE_REPORT_ID,
    TROUBLE_REPORT_KEY,
    REQUIRED_RESPONSE_IN_FLIGHT,
    RESPONSE_REQUIRED,
    TEMP_CALL_DIVERSION_NUMBER,
    SECONDARY_CONTACT_NAME,
    TWENTY_FOUR_HOUR_ACCESS,
    SECONDARY_CONTACT_NUMBER,
    CONTACT_NUMBER,
    CONTACT_NAME,
    ACCESS_NOTES,
    NOTES,
    ACCESS_HAZZARDS,
    LINE_TEST_REFERENCE,
    BT_REFERENCE,
    APPOINTMENT_REFERENCE,
    TEST_PRODUCT,
    SHORT_DESCRIPTION,
    BT_LINE_TEST_REFERENCE,
    STATUS,
    DNR_REFERENCE,
    MD_UPD_TS,
    MD_INS_TS,
    MD_EFFCTV_TO_TS,
    MD_EFFCTV_FROM_TS,
    MD_CURR_FLAG
FROM ODW_TROUBLE_REPORT_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);

