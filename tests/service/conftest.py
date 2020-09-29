import pytest
from src.core.service.source import Source
from datetime import datetime, timedelta


class FixtureService(object):
    def get_source(self):
        source = Source(scope="BTB",
                        source_name="ODW_BTB_UIN_FILE_DIM",
                        source_type="DIM",
                        db_type="NETEZZA",
                        frequency="MONTHLY",
                        load_type="FULL",
                        state=None,
                        status=None,
                        batch_size=None,
                        parallelize=None,
                        watermark_columns="""{"cols" : ["MD_INS_TS"]}""",
                        value=""" {"HWM1": "2019-02-24 00:00:00",  "key1" : "value1"} """,
                        select_fields="""MD_UPD_TS,MD_EFFCTV_TO_TS,MD_EFFCTV_FROM_TS,MD_UPD_BATCH,MD_BATCH_ID,MD_INS_TS,TRANSFER_REBATES_TOTAL""",
                        where_filter=None,
                        last_success_ts=None,
                        last_run_ts=None
                        )
        return source

    def last_hour_epoch(self):
        last_hour_date_time = datetime.now() - timedelta(hours = 1)
        return last_hour_date_time.strftime('%s')

    def maprfs(self):
        return ""


@pytest.fixture(scope="class")
def sourcefixture():
    return FixtureService()
