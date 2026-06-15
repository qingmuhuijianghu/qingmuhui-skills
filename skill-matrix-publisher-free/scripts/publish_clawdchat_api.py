#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虾聊(ClawdChat) API发布脚本
使用API Key直接上传，无需浏览器自动化
"""

import os
import sys
import json
import zipfile
import requests
from pathlib import Path

def pack_skill(skill_path):
    """将Skill打包成ZIP文件"""
    skill_path = Path(skill_path)
    skill_name = skill_path.name
    
    temp_dir = Path(__file__).parent.parent / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    zip_path = temp_dir / f"{skill_name}_SKILL.zip"
    
    print(f"[PACK] 打包Skill: {skill_name}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            zf.write(skill_md, "SKILL.md")
            print(f"  [ADD] SKILL.md")
        
        for file_path in skill_path.iterdir():
            if file_path.is_file() and file_path.name != "SKILL.md":
                zf.write(file_path, file_path.name)
                print(f"  [ADD] {file_path.name}")
    
    print(f"[OK] 打包完成: {zip_path}")
    return str(zip_path)

def upload_to_clawdchat(file_path, api_key, title=None, description=None):
    """使用API Key上传文件到虾聊"""
    file_path = Path(file_path)
    
    if not title:
        title = file_path.stem.replace("_SKILL", "")
    
    print(f"\n[UPLOAD] 上传到虾聊...")
    print(f"  文件: {file_path.name}")
    print(f"  标题: {title}")
    
    api_base = "https://clawdchat.cn/api/v1"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    try:
        print("[STEP 1] 上传文件...")
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'application/zip')}
            
            upload_endpoints = [
                f"{api_base}/files/upload",
                f"{api_base}/upload",
                "https://clawdchat.cn/f/upload",
            ]
            
            upload_response = None
            for endpoint in upload_endpoints:
                try:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        files=files,
                        timeout=30
                    )
                    if response.status_code in [200, 201]:
                        upload_response = response
                        print(f"[OK] 上传成功: {endpoint}")
                        break
                except Exception as e:
                    print(f"  [TRY] {endpoint} - {str(e)}")
                    continue
            
            if not upload_response:
                print("[ERROR] 所有上传端点都失败")
                return None
            
            upload_data = upload_response.json()
            file_url = upload_data.get('url') or upload_data.get('file_url') or upload_data.get('data', {}).get('url')
            print(f"[OK] 文件URL: {file_url}")
        
        print("[STEP 2] 创建分享帖子...")
        
        post_data = {
            "title": title,
            "content": description or f"分享Skill: {title}",
            "attachments": [file_url] if file_url else [],
            "type": "skill"
        }
        
        post_endpoints = [
            f"{api_base}/posts",
            f"{api_base}/posts/create",
        ]
        
        post_response = None
        for endpoint in post_endpoints:
            try:
                response = requests.post(
                    endpoint,
                    headers={**headers, "Content-Type": "application/json"},
                    json=post_data,
                    timeout=30
                )
                if response.status_code in [200, 201]:
                    post_response = response
                    print(f"[OK] 帖子创建成功: {endpoint}")
                    break
            except Exception as e:
                print(f"  [TRY] {endpoint} - {str(e)}")
                continue
        
        if not post_response:
            print("[ERROR] 所有发帖端点都失败")
            return None
        
        result = post_response.json()
        
        share_url = result.get('share_url') or result.get('url') or result.get('data', {}).get('share_url')
        post_id = result.get('id') or result.get('post_id') or result.get('data', {}).get('id')
        
        if not share_url and post_id:
            share_url = f"https://clawdchat.cn/post/{post_id}"
        
        print(f"\n[SUCCESS] 虾聊发布成功！")
        print(f"  分享链接: {share_url}")
        print(f"  帖子ID: {post_id}")
        
        return {
            "success": True,
            "share_url": share_url,
            "post_id": post_id,
            "file_url": file_url,
            "raw_response": result
        }
        
    except Exception as e:
        print(f"[ERROR] 发布失败: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    if len(sys.argv) < 3:
        print("虾聊API发布脚本")
        print("=" * 50)
        print("使用API Key直接上传Skill到虾聊")
        print("=" * 50)
        print("\n用法:")
        print("  python publish_clawdchat_api.py <skill_path> <api_key> [title] [description]")
        print("\n示例:")
        print("  python publish_clawdchat_api.py D:/skills/my-skill clawdchat_xxx123")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    api_key = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None
    description = sys.argv[4] if len(sys.argv) > 4 else None
    
    if not os.path.exists(skill_path):
        print(f"[ERROR] Skill路径不存在: {skill_path}")
        sys.exit(1)
    
    zip_path = pack_skill(skill_path)
    result = upload_to_clawdchat(zip_path, api_key, title, description)
    
    if result and result.get("success"):
        print(f"\n{'=' * 50}")
        print("虾聊发布完成！")
        print(f"{'=' * 50}")
        print(f"分享链接: {result['share_url']}")
        print(f"\n使用方式:")
        print("  将此链接发给Agent（WorkBuddy/QClaw）")
        print("  Agent会自动识别并安装Skill")
        sys.exit(0)
    else:
        print(f"\n{'=' * 50}")
        print("发布失败")
        print(f"{'=' * 50}")
        if result and result.get("error"):
            print(f"错误: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
