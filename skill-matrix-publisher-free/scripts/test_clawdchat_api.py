#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试虾聊API Key有效性"""

import sys
import requests

def test_api_key(api_key):
    """测试API Key"""
    print(f"[TEST] 验证API Key...")
    print(f"  Key: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    test_endpoints = [
        "https://clawdchat.cn/api/v1/agents/status",
        "https://clawdchat.cn/api/v1/me",
    ]
    
    for endpoint in test_endpoints:
        try:
            resp = requests.get(endpoint, headers=headers, timeout=15)
            print(f"  [{resp.status_code}] {endpoint}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"  [OK] API Key有效！")
                print(f"  [DATA] {data}")
                return True
        except Exception as e:
            print(f"  [ERR] {endpoint}: {e}")
    
    print(f"  [FAIL] API Key无效或网络不通")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python test_clawdchat_api.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    success = test_api_key(api_key)
    sys.exit(0 if success else 1)
