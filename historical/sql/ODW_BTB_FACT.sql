SELECT 
    CHARGE_FROM,
    CHARGE_TO,
    TRC_START_DATE_TIME,
    MD_INS_TS,
    MD_BATCH_ID,
    OPERATOR_KEY,
    VOICE_SERVICE_KEY,
    NIM_SERVICE_KEY,
    PENFOLD_DSL_SERVICE_KEY,
    CIRCUIT_M140_CODE,
    BTB_PRICE_LIST_KEY,
    BTB_FILE_KEY,
    BTB_BILL_YEAR_KEY,
    BTB_CHARGE_DESCRIPTION_KEY,
    BTB_CHARGE_CODE_KEY,
    BTB_CHARGE_SUB_TYPE_KEY,
    BTB_CHARGE_TYPE_KEY,
    BTB_RECORD_TYPE_KEY,
    BTB_BILL_TYPE_KEY,
    BTB_FACT_KEY,
    BTB_BILL_MONTH_KEY,
    BT_MDF_EXCHANGE_CODE,
    VAT_STATUS,
    WBMC_COL_49,
    WBMC_COL_48,
    WBMC_COL_47,
    WBMC_COL_46,
    WBMC_COL_45,
    WBMC_COL_44,
    WBMC_COL_43,
    WBMC_COL_42,
    WBMC_COL_41,
    WBMC_COL_40,
    WBMC_COL_39,
    WBMC_COL_38,
    WBMC_COL_37,
    WBMC_COL_36,
    WBMC_COL_35,
    EVENT_SOURCE,
    TEST_SESSION_DATE,
    PSTN_TIE_PAIR_DONOR,
    PSTN_TIE_CABLE_REF_DONOR,
    MPF_TIE_PAIR_DONOR,
    MPF_TIE_CABLE_REF_DONOR,
    BT_SERVICE_ID_DONOR,
    PSTN_TIE_PAIR_TARGET,
    PSTN_TIE_CABLE_REF_TARGET,
    MPF_TIE_PAIR_TARGET,
    MPF_TIE_CABLE_REF_TARGET,
    BT_SERVICE_ID_TARGET,
    SP_ORDER_FAULT_REF,
    MAC_CODE,
    CBUK_REF,
    OTHER_DURATION_OR_VISITS,
    PRORATE_DAYS,
    BANDWIDTH_VOLUME_GB,
    BURSTED_BANDWIDTH_MBPS,
    BURST_BANDWIDTH,
    CSP_NAME,
    ABSOLUTE_BURST_STORAGE,
    ROUNDED_PEAK_STORAGE,
    COMMITED_STORAGE,
    NUMBER_DAYS,
    CHARGE_PER_EU,
    EU_COUNT,
    DEVLIVERY_SERVICE_ID,
    TRAFFIC_TYPE,
    MINUTES,
    RECORD_COUNT,
    NETWORK_BUILD_COST_BAND,
    NETWORK_BUILD_COST,
    ADDITIONAL_REFERENCE,
    ADDRESS_LINE_1,
    SEQUENCE_NUMBER,
    TRC_SFI_TIME,
    DURATION,
    ORDER_SCENARIO,
    DOWNSTREAM_BANDWIDTH,
    UPSTREAM_BANDWIDTH,
    TRC_CHARGEABLE_HOURS,
    FREE_TEXT_DESC,
    CHANNEL_REFERENCE,
    ENABLE_SYNC,
    PRICE_BAND,
    UNIT_COST,
    TIER,
    CIRCUIT_CLASSIFICATION,
    NO_OF_UNITS,
    RESILIENCE_OPT_IND,
    MOVED_FROM_TO,
    BILLING_REMARKS,
    LOCATION,
    ROOM,
    FLOOR,
    EXCHANGE_ID,
    EXCHANGE_1141_CODE,
    ZONE_NAME,
    ZONE_DESCRIPTION,
    SITE_CODE,
    SITE_COUNTRY_NAME,
    SITE_COUNTY_NAME,
    SITE_IN_CODE,
    DIRECTORY_NUMBER,
    SITE_OUT_CODE,
    SITE_POST_TOWN_NAME,
    SITE_LOCALITY_NAME,
    PRODUCT_TYPE,
    SITE_THORO_NAME,
    SITE_THORO_NUM,
    SITE_PREM_NAME,
    SITE_SUB_PREM_NAME,
    ASS_PROD_SERV_ID_III,
    ASS_PROD_SERV_ID_II,
    ASS_PROD_SERV_ID,
    CSS_JOB_NO,
    CP_ORDER_REFERENCE,
    CSS_ACCOUNT_NUMBER,
    ADJUSTMENT_FREE_TEXT_DESC,
    OR_SERVICE_ID,
    CLEAR_CODE,
    TRC_DESC_CODE,
    FULLPERIODAMOUNT,
    DNR_REF,
    CUST_ORD_REF_NUM,
    DAILYAMOUNT,
    CUST_ORD_NUM,
    INSTALLATION_FEE,
    COST,
    SIEBEL_JOB_NO,
    OTHER_DETAILS_3,
    OTHER_DETAILS_2,
    SUBSTR(END_DATE,1,10)AS END_DATE,
    OTHER_DETAILS_1,
    BT_CIRCUIT_ID,
    CIRCUIT_ID,
    EXCHANGE_NAME,
    COST_UNITS,
    UNIT_OF_MEASUREMENT,
    POST_CODE,
    BT_CODE
FROM ODW_BTB_FACT
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
);
