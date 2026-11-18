import secrets
from curl_cffi import requests as curl_requests
from ._logger import get_logger
from ._verify import is_valid_token

logger = get_logger("oppaypay_desktop.auth")

PORTAL_URL = "https://www.paypay.ne.jp"

class WebAuth:
    def __init__(self, proxy: str = None):
        self.session = curl_requests.Session(
            impersonate="chrome",
            proxies={"http": proxy, "https": proxy} if proxy else None,
            timeout=30,
        )
        self.access_token: str = None
        self.refresh_token: str = None
        self.client_uuid: str = secrets.token_hex(16)

    def _get_headers(self) -> dict:
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
            "Content-Type": "application/json",
            "Origin": PORTAL_URL,
            "Referer": f"{PORTAL_URL}/app/account/sign-in",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

    def login(self, phone: str, password: str) -> dict:
        phone = phone.replace("-", "")
        logger.info(f"🔑 Web版ログイン開始: {phone[:4]}****")

        url = f"{PORTAL_URL}/app/v1/oauth/token"
        headers = self._get_headers()
        
        payload = {
            "scope": "SIGN_IN",
            "client_uuid": self.client_uuid,
            "grant_type": "password",
            "username": phone,
            "password": password,
            "add_otp_prefix": True,
            "language": "ja"
        }

        response = self.session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "access_token" not in data:
            raise Exception(f"access_tokenが見つかりません: {data}")

        self.access_token = data["access_token"]
        self.refresh_token = data.get("refresh_token")
        
        if not is_valid_token(self.access_token):
            raise Exception("取得したトークンの形式が不正です")

        self.session.headers["Authorization"] = f"Bearer {self.access_token}"
        logger.info("✅ Web版ログイン成功")
        return data