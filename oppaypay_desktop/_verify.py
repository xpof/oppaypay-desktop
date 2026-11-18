# oppaypay_desktop/_verify.py
import re
import logging
from typing import Any, Dict

logger = logging.getLogger("oppaypay_desktop.verify")

def is_valid_token(token: str) -> bool:

    if not token or not isinstance(token, str):
        return False
    
    if len(token) < 100:
        return False
        
    if not re.match(r"^[A-Za-z0-9\-_=/+]+$", token):
        logger.warning("トークンに不正な文字が含まれています")
        return False
        
    return True

def check_response_health(response_data: Dict[str, Any]) -> bool:

    if not isinstance(response_data, dict):
        logger.error("レスポンスがJSONオブジェクトではありません")
        return False

    if response_data.get("resultCode") == "S0000" or response_data.get("status") == "SUCCESS":
        return True

    header = response_data.get("header", {})
    result_code = header.get("resultCode") or response_data.get("resultCode")
    
    if result_code and result_code != "S0000":
        result_message = header.get("resultMessage") or response_data.get("resultMessage", "Unknown Error")
        error_payload = response_data.get("errorPayload") or response_data.get("error", {})
        
        display_error = error_payload.get("displayErrorResponse", {})
        description = display_error.get("description", result_message)
        
        logger.error(f"API Error [{result_code}]: {description}")
        
        return False

    logger.warning("予期せぬレスポンス構造です: %s", response_data)
    return True

def extract_error_message(response_data: Dict[str, Any]) -> str:
    header = response_data.get("header", {})
    error_payload = response_data.get("errorPayload") or response_data.get("error", {})
    display_error = error_payload.get("displayErrorResponse", {})
    
    return (
        display_error.get("description") or 
        header.get("resultMessage") or 
        response_data.get("resultMessage") or 
        "不明なエラーが発生しました"
    )