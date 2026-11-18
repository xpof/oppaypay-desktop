from ._auth import WebAuth
from ._logger import get_logger
from ._verify import check_response_health

logger = get_logger("oppaypay_desktop.client")
PORTAL_URL = "https://www.paypay.ne.jp"

class PayPayDesktop:
    def __init__(self, phone: str, password: str, proxy: str = None):
        self.auth = WebAuth(proxy=proxy)
        self.phone = phone
        self.password = password

    def login(self) -> dict:
        return self.auth.login(self.phone, self.password)

    def _request(self, method: str, path: str, **kwargs) -> dict:
        if not self.auth.access_token:
            raise Exception("ログインが必要です")
        
        url = f"{PORTAL_URL}{path}"
        headers = self.auth._get_headers()
        
        response = self.auth.session.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        data = response.json()
        
        if not check_response_health(data):
            raise Exception(f"APIリクエストが失敗しました: {data}")
            
        return data

    def get_balance(self) -> dict:
        logger.info("💰 残高を取得中...")
        return self._request("GET", "/app/v2/wallet/balance")