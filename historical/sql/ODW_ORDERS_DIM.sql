SELECT 
    ORDER_ID,
    ORDER_STATUS_KEY,
    ORDER_TYPE_KEY,
    ORDER_KEY,
    SNS_ADDRESS_REFERENCE,
    DELIVERY_POSTCODE,
    DELIVERY_PHONE_NUMBER,
    BT_REFERENCE,
    OPERATOR_NOTES,
    OPERATOR_TYPE_CODE,
    MD_UPD_TS,
    MD_INS_TS,
    MD_EFFCTV_TO_TS,
    MD_EFFCTV_FROM_TS,
    LAST_MODIFIED_DATE,
    REQUESTED_DELIVERY_DATE,
    EXPECTED_DELIVERY_DATE,
    CANCEL_REQUESTED_DATE,
    CREATED_DATE,
    ORDER_RECEIVED_DATE,
    ORDER_STATUS_SET_DATE,
    MD_CURR_FLAG
FROM ODW_ORDERS_DIM
WHERE (
    MD_INS_TS >= '{from_ts}'
    AND MD_INS_TS < '{to_ts}'
) OR (
    MD_UPD_TS >= '{from_ts}'
    AND MD_UPD_TS < '{to_ts}'
);
