from time import sleep

from src.utils.req import tor_req


class TestTor:
    def test_tor(self):
        attemp_1 = tor_req("https://ident.me").text
        sleep(10)
        attemp_2 = tor_req("https://ident.me").text

        assert attemp_1 != attemp_2
