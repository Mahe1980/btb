from src.core.service.ctl_service import CTLService
import pytest
import re


class TestService:
    service = CTLService("BTB", "DAILY")

    @pytest.fixture(autouse=True)
    def setup(self, sourcefixture):
        self.hwm_epoch = sourcefixture.last_hour_epoch()
        self.source = sourcefixture.get_source()

    def test_service_get_source(self):
        result = self.service.get_sources()
        assert len(result) > 0

    def test_update_sql(self):
        expected_match = re.compile("""UPDATE CTL_GCP_MIGRATION SET value = '{"HWM1": (.*)}' WHERE SOURCE_NAME = 'ODW_BTB_UIN_FILE_DIM'""")
        result = self.service.prepare_update_sql(source_name=self.source.source_name,
                                                 wm_json=self.source.value, hwm_epoch=self.hwm_epoch)
        print(result)
        assert expected_match.match(result)
