SELECT
    PENFOLD_DSL_SERVICE_KEY,
    SERVICE_ID,
    BT_SERVICE_ID,
    DIRECTORY_NUMBER,
    OPERATOR_CODE,
    OPERATOR_DESCRIPTION,
    PRODUCT_SPEC_ID,
    SERVICE_START_DATE,
    SERVICE_CEASE_DATE,
    CREATED_DATE,
    EXCHANGE_CODE,
    INSTALL_POSTCODE,
    BT_PRODUCT_NAME,
    UNSOLICITED_CEASE_WARNING_DATE,
    MAX_STABLE_SPEED,
    FAULT_THRESHOLD_SPEED,
    MAC,
    NIM_SERVICE_ID,
    SERVICE_UP_SPEED,
    SERVICE_DOWN_SPEED,
    STATUS,
    UAN,
    SOURCE,
    ENDPOINT_ID,
    SERVICE_SPEC_CODE,
    MIGRATING,
    RESTRICTION_TYPE,
    DN_START_DATE,
    CABLE_LINK_REFERENCE,
    UL_SPEED,
    DL_SPEED,
    CIRCUIT_REFERENCE_NUMBER,
    FEATURES_A,
    FEATURES_B,
    IPV6_BLACKLIST_DATE,
    CGN_BLACKLIST_DATE,
    CGN_BLACKLIST_REASON,
    CGN_STATUS,
    CGN_EXCLUSION_DATE,
    CGN_EXCLUSION_REASON,
    CAST(NULL as VARCHAR(10)) AS CARE_LEVEL,
    MD_CURR_FLAG,
    MD_EFFCTV_FROM_TS,
    MD_EFFCTV_TO_TS,
    MD_INS_TS,
    MD_INS_INITIAL_BATCH_ID,
    MD_INS_ACTUAL_BATCH_ID,
    MD_UPD_TS,
    MD_UPD_INITIAL_BATCH_ID,
    MD_UPD_ACTUAL_BATCH_ID
FROM ODW_PENFOLD_DSL_SERVICE_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);
