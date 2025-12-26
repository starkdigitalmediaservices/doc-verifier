import os
import requests
from typing import Optional, Dict


def post_data_via_webhook(
    url: str,
    data: Optional[Dict] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 300,
) -> requests.Response:
    try:
            
        response = requests.post(
            url=url,
            json=data or {},
            headers=headers or {},
            timeout=timeout,
        )

        response.raise_for_status()
        print(f"Status code : {response.status_code}\nContent : {response.content}")

        return response

    except requests.exceptions.RequestException as exc:
        print("Exception reason : ", response.reason)
        raise RuntimeError(f"Webhook call failed: {exc}") from exc
