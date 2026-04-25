import requests
import json
import os
from typing import List, Dict, Optional

class APIService:
    def __init__(self):
        self.base_url = "https://cf-v2.uapis.cn"
        self.account_oauth_issuer = "https://account-api.qzhua.net"
        self.client_id = "019d5ce39a9b728fa1b5565be72d84ca"
        self.client_secret = ""

    def get_stored_user(self) -> Optional[Dict]:
        # Load user from config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('user')
        return None

    def save_user(self, user: Dict):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config['user'] = user
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def login_with_token(self, token: str) -> Dict[str, str]:
        if token.startswith("Bearer "):
            token = token[7:].strip()
        if not token:
            raise ValueError("令牌不能为空")
        user = {
            'accessToken': token,
            'usertoken': token,
        }
        self.save_user(user)
        return user

    def clear_user(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config['user'] = None
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def ensure_authenticated_user(self, token: Optional[str] = None):
        if token:
            if token.startswith("Bearer "):
                token = token[7:].strip()
            return {'accessToken': token, 'legacyToken': None}

        user = self.get_stored_user()
        if not user or not user.get('accessToken'):
            raise Exception("用户未登录")
        return {
            'accessToken': user.get('accessToken'),
            'legacyToken': user.get('usertoken')
        }

    def request(self, endpoint: str, method: str = 'GET', headers: Optional[Dict] = None, data: Optional[Dict] = None):
        url = f"{self.base_url}{endpoint}"
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()

    def fetch_nodes(self, token: Optional[str] = None) -> List[Dict]:
        auth = self.ensure_authenticated_user(token)
        authorization = f"Bearer {auth['accessToken'] or auth['legacyToken']}"

        data = self.request("/node", headers={"authorization": authorization})

        if isinstance(data, list):
            return data
        raise Exception("获取节点列表失败")

    def get_node_udp_support(self, node_name: str, token: Optional[str] = None) -> Optional[bool]:
        # Implement caching if needed
        nodes = self.fetch_nodes(token)
        for node in nodes:
            if node.get('name') == node_name:
                return node.get('udp') == 'true'
        return None