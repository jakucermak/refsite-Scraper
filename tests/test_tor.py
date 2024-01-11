import time

from  src.utils.tor_req import tor_req

class TestTor:
    def test_tor(self):
        attemp_1 = tor_req("https://ident.me").text
        time.sleep(10)
        attemp_2 = tor_req("https://ident.me").text

        assert attemp_1 != attemp_2
