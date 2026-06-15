#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub发布脚本
上传Skill到GitHub仓库
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path

def publish_to_github(skill_path, github_token, repo_owner, repo_name, version="1.0.0"):
    """发布Skill到GitHub"""
    
    print(f"[GITHUB] 发布到GitHub...")
    print(f"[REPO] 仓库: {repo_owner}/{repo_name}")
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    skill_name = Path(skill_path).name
    
    success_count = 0
    for root, dirs, files in os.walk(skill_path):
        if '.git' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, skill_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                
                data = {
                    "message": f"Add {rel_path} (v{version})",
                    "content": encoded_content
                }
                
                url = f"{base_url}/contents/{rel_path}"
                response = requests.put(url, headers=headers, json=data)
                
                if response.status_code in [201, 422]:
                    print(f"  [OK] {rel_path}")
                    success_count += 1
                else:
                    print(f"  [FAIL] {rel_path} - {response.status_code}")
                    
            except Exception as e:
                print(f"  [ERROR] {rel_path} - {str(e)}")
    
    print(f"\n[OK] GitHub发布完成！成功: {success_count} 个文件")
    print(f"[LINK] https://github.com/{repo_owner}/{repo_name}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: python publish_github.py <skill_path> <token> <owner> <repo>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    token = sys.argv[2]
    owner = sys.argv[3]
    repo = sys.argv[4]
    
    publish_to_github(skill_path, token, owner, repo)
