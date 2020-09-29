SELECT 
    MD_INS_BATCH_ID,
    SERVICE_ID,
    ORIGINAL_ID,
    LINE_TEST_ID,
    LINE_TEST_STATUS_KEY,
    LINE_TEST_FAULT_KEY,
    BT_SERVICE_KEY,
    VOICE_SERVICE_KEY,
    PENFOLD_DSL_SERVICE_KEY,
    LINE_TEST_SERVICE_TYPE_KEY,
    LINE_TEST_KEY,
    UP_NOISE_MARGIN,
    UP_ATTENUATION,
    UP_ACTUAL_BITRATE,
    UP_ATTAINABLE_BITRATE,
    DOWN_NOISE_MARGIN,
    DOWN_ATTENUATION,
    DOWN_ACTUAL_BITRATE,
    DOWN_ATTAINABLE_BITRATE,
    NTE_POWER_STATUS,
    SYNC_STATUS,
    DOWNSTREAM_SPEED,
    UPSTREAM_SPEED,
    ETHERNET_TRAFFIC,
    PERFORMER_REFERENCE,
    APPOINTMENT_REQUIRED,
    OPERATOR_REFERENCE,
    LINE_TEST_REFERENCE,
    TEST_OUTCOME_DESCRIPTION,
    BT_SERVICE_ID,
    OPERATOR_ID,
    TEST_OUTCOME_CODE,
    TEST_OUTCOME,
    REQUESTER,
    MD_INS_TS,
    FINISHED_DATE,
    REQUESTED_DATE
FROM ODW_LINE_TEST_FACT
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
);