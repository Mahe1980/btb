from src.core.service.extractor import Extractor
import pytest
import os
import re

class TestExtractor(object):
    @pytest.fixture(autouse=True)
    def setup(self, sourcefixture):
        self.hwm_epoch = sourcefixture.last_hour_epoch()
        self.source = sourcefixture.get_source()
        self.maprfs = sourcefixture.maprfs()

    def test_extractor_produces_file(self):
        service = Extractor(self.source, self.hwm_epoch)
        file_name = service.run("./json_output/abc.json")
        assert os.path.isfile(file_name)

    def test_prepare_watermark(self):
        expected_match = re.compile(r"""\(MD_INS_TS > '2019-02-24 00:00:00'\) and \(MD_INS_TS""")
        service = Extractor(self.source, self.hwm_epoch)
        result = service.prepare_watermark(self.source.watermark_columns, self.source.value)
        print(result)
        assert expected_match.match(result)

    def test_prepare_watermark_two_cols(self):
        expected_match = re.compile("""\(MD_INS_TS > '2019-02-24 00:00:00' or MD_UPD_TS > '2019-02-24 00:00:00'\) and \(MD_INS_TS <= (.*) or MD_UPD_TS <= (.*)""" )
        self.source.watermark_columns="""{"cols" : ["MD_INS_TS","MD_UPD_TS"]}"""
        service = Extractor(self.source, self.hwm_epoch)
        result = service.prepare_watermark(self.source.watermark_columns, self.source.value)
        print(result)
        assert expected_match.match(result)


