from src.core.connectors.connectors import get_nz_conn, get_oracle_conn


class TestService:

    def test_conn_nz(self):
        get_nz_conn()

    def test_conn_oracle(self):
        get_oracle_conn()

