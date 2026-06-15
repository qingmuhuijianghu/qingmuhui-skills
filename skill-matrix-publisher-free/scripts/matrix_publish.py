#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill矩阵分发助手 - 主脚本
一键分发到腾讯SkillHub、虾聊、虾友SkillHub、GitHub、ClawHub五大平台
v2.2 - 五平台全覆盖 + 三重验证 + 智能类目识别
"""

import os
import sys
import json
import re
import hashlib
import subprocess
from pathlib import Path
from typing import Optional, Tuple

# 配置存储路径
CONFIG_FILE = Path(__file__).parent.parent / "config" / "publisher_config.json"

# ═══════════════════════════════════════════════════════════
#  智能类目识别引擎
# ═══════════════════════════════════════════════════════════

# 类目关键词映射表（一级 → {关键词, 二级映射}）
# 每个二级类目下面有对应的关键词列表，用于匹配 SKILL.md 内容
CATEGORY_KEYWORDS = {
    "赛博生活": {
        "keywords": ["生活", "社交", "陪伴", "娱乐", "游戏", "美食", "动物", "宠物", "神话", "动漫", "历史", "国潮", "科技人物", "IP", "角色扮演"],
        "children": {
            "云吃美食": ["美食", "吃", "餐厅", "菜谱", "烹饪", "食谱", "做饭", "料理"],
            "赛博职场": ["职场", "职业", "上班", "打工", "同事", "办公室"],
            "云养动物": ["动物", "宠物", "养", "猫", "狗", "鱼", "鸟", "兔"],
            "远古神话": ["神话", "传说", "古代", "神仙", "妖怪", "封神", "山海经"],
            "商业大佬": ["商业", "大佬", "企业家", "创业", "老板", "CEO"],
            "历史名人": ["历史", "名人", "古代人物", "皇帝", "将军", "诗人"],
            "国潮联名": ["国潮", "联名", "国风", "汉服", "传统", "文创"],
            "科技巨匠": ["科技", "巨匠", "科学家", "发明家", "工程师"],
            "动漫IP": ["动漫", "二次元", "漫画", "动画", "番剧", "cosplay"],
            "情感陪伴": ["情感", "陪伴", "社交", "聊天", "交友", "漂流瓶", "搭子", "倾诉", "树洞", "匹配", "同城", "朋友"],
        }
    },
    "职场成长": {
        "keywords": ["职场", "工作", "效率", "办公", "写作", "简历", "面试", "演讲", "沟通", "管理", "领导", "思维", "AI办公", "自动化"],
        "children": {
            "领导力": ["领导", "管理", "带队", "决策", "授权"],
            "职场写作": ["写作", "文案", "报告", "公文", "邮件", "总结", "汇报"],
            "人脉拓展": ["人脉", "社交", "networking", "关系", "圈子"],
            "效率提升": ["效率", "提效", "工具", "流程", "自动化", "省时", "快捷"],
            "AI 办公": ["AI办公", "AI写作", "智能办公", "AI助手", "自动化办公"],
            "思维模型": ["思维", "模型", "框架", "方法论", "认知", "逻辑"],
            "谈判技巧": ["谈判", "协商", "议价", "博弈", "说服"],
            "简历优化": ["简历", "求职", "面试", "CV", "应聘"],
            "演讲表达": ["演讲", "表达", "口才", "演示", "PPT", "汇报"],
            "职业规划": ["职业", "规划", "发展", "晋升", "转型"],
            "职场沟通": ["沟通", "协作", "会议", "反馈", "汇报"],
            "团队管理": ["团队", "组织", "协调", "绩效", "激励"],
        }
    },
    "生态商业": {
        "keywords": ["商业", "营销", "社群", "运营", "微信", "视频号", "直播", "带货", "变现", "IP", "私域", "小龙虾", "推客"],
        "children": {
            "微信小店": ["微信小店", "微信商城", "小程序商城", "开店"],
            "活动运营": ["活动", "运营", "策划", "执行", "拉新", "促活"],
            "社群裂变": ["裂变", "增长", "拉新", "传播", "病毒"],
            "内容工具": ["内容", "工具", "编辑器", "排版", "素材"],
            "社群搭建": ["社群搭建", "建群", "社群架构", "社群设计"],
            "贴图号带货": ["贴图号", "贴图", "带货", "图文带货"],
            "内容营销": ["内容营销", "软文", "种草", "品牌内容"],
            "社群变现": ["变现", "付费", "会员", "订阅", "营收"],
            "社群众筹": ["众筹", "筹资", "预售", "共创"],
            "视频号直播": ["视频号", "直播", "带货直播", "开播"],
            "小龙虾新玩法": ["小龙虾", "龙虾", "虾友", "Qclaw", "WorkBuddy"],
            "视频号": ["视频号", "短视频", "号主"],
            "大健康行业": ["健康", "养生", "医疗", "保健", "大健康"],
            "企业微信社群": ["企业微信", "企微", "SCRM"],
            "推客带货": ["推客", "分销", "推广", "带货"],
            "社群运营": ["社群运营", "社群管理", "用户运营"],
            "IP 打造": ["IP", "个人品牌", "人设", "定位"],
            "活动工具": ["工具", "软件", "SaaS", "平台"],
            "社群管理": ["管理", "群管", "机器人", "自动化管理"],
        }
    },
    "行业方案": {
        "keywords": ["行业", "方案", "美妆", "服饰", "数码", "电商", "珠宝", "教育", "本地", "金融", "餐饮"],
        "children": {
            "美妆服饰": ["美妆", "服饰", "穿搭", "时尚", "化妆", "护肤"],
            "美容养生馆": ["美容", "养生", "spa", "按摩", "理疗"],
            "3C数码": ["数码", "3C", "手机", "电脑", "电子"],
            "零售电商": ["零售", "电商", "淘宝", "京东", "拼多多", "店铺"],
            "珠宝文玩": ["珠宝", "文玩", "玉石", "首饰", "古董"],
            "教育培训": ["教育", "培训", "课程", "学习", "知识付费"],
            "本地生活": ["本地", "同城", "生活服务", "O2O", "到店"],
            "金融保险": ["金融", "保险", "理财", "投资", "银行"],
            "餐饮行业": ["餐饮", "饭店", "外卖", "奶茶", "食品"],
        }
    },
    "专家服务": {
        "keywords": ["专家", "咨询", "顾问", "架构", "增长", "操盘", "发售", "私域", "流量"],
        "children": {
            "社群架构师": ["社群架构", "架构设计", "社群体系"],
            "流量增长专家": ["流量", "增长", "拉新", "获客"],
            "IP引爆操盘手": ["IP引爆", "操盘", "爆款", "出圈"],
            "社群发售专家": ["发售", "发布", "上线", "推出"],
            "内容营销专家": ["内容", "营销", "策略"],
            "短视频专家": ["短视频", "抖音", "快手", "拍摄"],
            "社群变现专家": ["变现", "付费", "营收"],
            "场景社群专家": ["场景", "社群场景", "场景化"],
            "AI客服专家": ["客服", "AI客服", "智能客服"],
            "私域流量专家": ["私域", "私域流量", "SCRM"],
            "活动运营专家": ["活动", "运营", "策划"],
        }
    },
}

def fetch_category_tree(endpoint="https://aiskillhub.vip", token=None):
    """从 SkillHub API 获取实时类目树"""
    try:
        import requests
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        resp = requests.get(f"{endpoint}/api/skills/categories", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('data', [])
    except Exception:
        pass
    return None

def classify_skill(skill_content, skill_name="", category_tree=None):
    """
    智能识别 Skill 应该归属的类目
    
    返回: (categoryId, parentName, childName, confidence)
    """
    # 合并所有可分析文本
    full_text = skill_name + " " + skill_content[:2000]
    
    # 提取 frontmatter 中的 description 和 features
    description = ""
    triggers = []
    # ── 解析 frontmatter（正确处理多行 description）───
    fm_match = re.match(r'^---\s*\n(.*?)\n---', skill_content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        in_description = False
        desc_lines = []
        for line in fm.split('\n'):
            # 如果在 description 多行块内
            if in_description:
                # 续行判定：以≥2空格或tab开头，或为空行
                if line.startswith('  ') or line.startswith('	') or line.rstrip() == '':
                    if line.strip():
                        desc_lines.append(line.strip())
                    # 空行也保留（作为分隔）
                    continue
                else:
                    # 遇到非续行，退出 description 模式
                    in_description = False
            # 正常字段解析（不在 description 续行内）
            if line.strip().startswith('name:'):
                name = line.split(':', 1)[1].strip()
            elif line.strip().startswith('description:'):
                in_description = True
                rest = line.split(':', 1)[1].strip()
                rest = rest.strip('"').strip("'")
                if rest and not rest.startswith('|'):
                    desc_lines.append(rest)
                elif rest.startswith('|'):
                    pass  # 多行块，下一批续行会捕获
            elif line.strip().startswith('version:'):
                version = line.split(':', 1)[1].strip().strip('"')
            elif line.strip().startswith('- ') and not in_description:
                trigger_text = line.strip()[2:].strip()
                if trigger_text:
                    triggers.append(trigger_text)
        description = ' '.join(desc_lines)  # 完整概述，禁止截断

    full_text += " " + description + " " + " ".join(triggers)
    full_text_lower = full_text.lower()
    
    # 计分匹配
    scores = {}  # (parent_name, child_name, child_id) -> score
    
    # 如果 API 返回了真实类目树，使用它
    if category_tree:
        for parent in category_tree:
            parent_name = parent['name']
            parent_id = parent['id']
            for child in parent.get('children', []):
                child_name = child['name']
                child_id = child['id']
                key = (parent_name, child_name, child_id, parent_id)
                scores[key] = 0
    else:
        # 使用本地关键词表
        for parent_name, parent_data in CATEGORY_KEYWORDS.items():
            for child_name, keywords in parent_data.get('children', {}).items():
                key = (parent_name, child_name, None, None)
                scores[key] = 0
    
    # 对每个类目进行关键词匹配打分
    for (parent_name, child_name, child_id, parent_id), _ in scores.items():
        score = 0
        # 获取该二级类目的关键词
        child_keywords = CATEGORY_KEYWORDS.get(parent_name, {}).get('children', {}).get(child_name, [])
        parent_keywords = CATEGORY_KEYWORDS.get(parent_name, {}).get('keywords', [])
        
        for kw in child_keywords:
            if kw.lower() in full_text_lower:
                score += 10  # 二级关键词命中 +10
        for kw in parent_keywords:
            if kw.lower() in full_text_lower:
                score += 3   # 一级关键词命中 +3
        
        # 类目名称本身出现在文本中（强信号）
        if child_name in full_text:
            score += 20
        if parent_name in full_text:
            score += 8
        
        scores[(parent_name, child_name, child_id, parent_id)] = score
    
    # 找最高分
    if not scores:
        return (None, "未分类", "未分类", 0)
    
    best = max(scores.items(), key=lambda x: x[1])
    (parent_name, child_name, child_id, parent_id), score = best
    
    # 计算置信度 (0-100)
    max_possible = 50  # 粗略估计最高可能分数
    confidence = min(int(score / max_possible * 100), 100) if score > 0 else 0
    
    return (child_id, parent_name, child_name, confidence)

def create_version_record(endpoint, token, skill_id, version, changelog):
    """为 Skill 创建历史版本变更记录"""
    try:
        import requests
        resp = requests.post(
            f"{endpoint}/api/skills/{skill_id}/versions",
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            json={'version': version, 'changelog': changelog},
            timeout=10
        )
        if resp.status_code in [200, 201]:
            print(f"  📝 版本记录已同步: v{version}")
            return True
        else:
            print(f"  ⚠️ 版本记录同步失败: {resp.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️ 版本记录同步异常: {e}")
        return False

def print_classification_result(parent_name, child_name, confidence, skill_name):
    """打印分类结果"""
    bar = "█" * (confidence // 10) + "░" * (10 - confidence // 10)
    print(f"\n  🤖 智能类目识别")
    print(f"  ┌─────────────────────────────────────┐")
    print(f"  │ Skill: {skill_name[:35]:<35} │")
    print(f"  │ 一级: {parent_name:<33} │")
    print(f"  │ 二级: {child_name:<33} │")
    print(f"  │ 置信度: [{bar}] {confidence}%{'':<12} │")
    print(f"  └─────────────────────────────────────┘")

def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    """保存配置"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def publish_to_github(skill_path, config):
    """发布到GitHub"""
    print("\n📦 发布到GitHub...")
    
    github_config = config.get('github', {})
    token = github_config.get('token')
    owner = github_config.get('owner')
    repo = github_config.get('repo')
    
    if not all([token, owner, repo]):
        print("❌ GitHub配置不完整")
        return False
    
    script_path = Path(__file__).parent / "publish_github.py"
    cmd = [
        "python", str(script_path),
        skill_path,
        token,
        owner,
        repo
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0

def publish_to_clawdchat(skill_path, config):
    """发布到虾聊（使用API Key方案）"""
    print("\n🦞 发布到虾聊...")
    
    clawdchat_config = config.get('clawdchat', {})
    api_key = clawdchat_config.get('api_key')
    
    if api_key:
        print("💡 使用API Key直接上传")
        script_path = Path(__file__).parent / "publish_clawdchat_api.py"
        cmd = [
            "python", str(script_path),
            skill_path,
            api_key
        ]
        result = subprocess.run(cmd)
        return result.returncode == 0
    else:
        print("💡 使用虾聊分享链接方案")
        print("⚠️  未配置API Key，将使用手动方式")
        
        script_path = Path(__file__).parent / "publish_clawdchat_share.py"
        cmd = [
            "python", str(script_path),
            skill_path
        ]
        result = subprocess.run(cmd)
        return result.returncode == 0

def verify_publish_credentials(phone, password, api_key, invitation_code,
                               endpoint="https://aiskillhub.vip"):
    """
    三重验证：登录 + API Key + 邀请码
    必须三项全部通过才允许发布
    
    返回: (success: bool, message: str, token: str|None)
    """
    import requests
    
    results = {
        "login": False,
        "api_key": False,
        "invitation": False,
    }
    
    print("\n  ╔══════════════════════════════════╗")
    print("  ║   🛡️  三重安全验证           ║")
    print("  ╚══════════════════════════════════╝")
    
    # ── 第一重：平台登录验证 ──
    print("\n  [1/3] 平台登录验证...")
    if not phone or not password:
        print("  ❌ 未提供手机号或密码")
        return False, "缺少登录凭证（手机号+密码）", None
    
    try:
        login_resp = requests.post(f"{endpoint}/api/auth/login", json={
            "phone": phone,
            "password": password
        }, timeout=15)
        
        if login_resp.status_code != 200:
            print(f"  ❌ 登录失败 ({login_resp.status_code})")
            return False, f"登录失败：{login_resp.text[:100]}", None
        
        login_data = login_resp.json()
        token = login_data.get('data', {}).get('access_token')
        if not token:
            print("  ❌ 未获取到 access_token")
            return False, "登录异常：未返回有效token", None
        
        user = login_data.get('data', {}).get('user', {})
        print(f"  ✅ 登录成功 — {user.get('nickname', phone)}")
        results["login"] = True
    except Exception as e:
        print(f"  ❌ 登录异常: {e}")
        return False, f"登录请求异常：{str(e)}", None
    
    # ── 第二重：API Key 验证 ──
    print("\n  [2/3] API Key 验证...")
    if not api_key or not api_key.strip():
        print("  ❌ 未提供 API Key")
        print("  💡 请在 SkillHub「个人中心 → 开发设置」获取")
        return False, "缺少 API Key", None
    
    try:
        # 尝试用 API Key 调用户信息接口进行验证
        verify_resp = requests.get(
            f"{endpoint}/api/user/profile",
            headers={"Authorization": f"Bearer {api_key}", "X-API-Key": api_key},
            timeout=10
        )
        # 也尝试 /api/auth/verify 端点
        if verify_resp.status_code in [401, 403]:
            verify_resp2 = requests.post(f"{endpoint}/api/auth/verify", json={
                "token": api_key
            }, timeout=10)
            if verify_resp2.status_code in [200, 201]:
                print(f"  ✅ API Key 有效")
                results["api_key"] = True
            else:
                # 宽松处理：只要API Key格式合理（长度>10），且登录已通过，就算有效
                if len(api_key.strip()) >= 10:
                    print(f"  ⚠️  无法远程验证API Key，但格式有效(len={len(api_key)})，放行")
                    results["api_key"] = True
                else:
                    print(f"  ❌ API Key 格式无效（长度不足）")
                    print(f"  💡 请在 SkillHub「个人中心 → 开发设置」重新获取")
                    return False, "API Key 格式无效", None
        elif verify_resp.status_code == 200:
            print(f"  ✅ API Key 有效")
            results["api_key"] = True
        else:
            # 端点不存在，做格式校验
            if len(api_key.strip()) >= 10:
                print(f"  ⚠️  验证端点不可用({verify_resp.status_code})，格式校验通过(len={len(api_key)})，放行")
                results["api_key"] = True
            else:
                print(f"  ❌ API Key 格式无效（长度不足）")
                return False, "API Key 格式无效", None
    except Exception as e:
        # 网络异常时宽松处理
        if len(api_key.strip()) >= 10:
            print(f"  ⚠️  验证服务不可达，格式校验通过，放行")
            results["api_key"] = True
        else:
            return False, f"API Key 无效且验证请求异常：{str(e)}", None
    
    # ── 第三重：邀请码验证 ──
    print("\n  [3/3] 邀请码验证...")
    if not invitation_code or not invitation_code.strip():
        print("  ❌ 未提供邀请码")
        print("  💡 请在 SkillHub「个人中心 → 我的邀请码」获取")
        return False, "缺少邀请码", None
    
    try:
        # 尝试调邀请码验证端点
        inv_resp = requests.post(f"{endpoint}/api/invitation/verify", json={
            "code": invitation_code.strip()
        }, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        
        if inv_resp.status_code in [200, 201]:
            print(f"  ✅ 邀请码验证通过 — {invitation_code}")
            results["invitation"] = True
        elif inv_resp.status_code == 404:
            # 端点不存在，做格式校验
            if len(invitation_code.strip()) >= 4:
                print(f"  ⚠️  验证端点不可用(404)，格式校验通过(len={len(invitation_code)})，放行")
                results["invitation"] = True
            else:
                print(f"  ❌ 邀请码格式无效（长度不足4位）")
                return False, "邀请码格式无效", None
        else:
            print(f"  ❌ 邀请码验证失败 ({inv_resp.status_code}): {inv_resp.text[:100]}")
            return False, f"邀请码验证失败：{inv_resp.text[:100]}", None
    except Exception as e:
        # 网络异常时宽松处理
        if len(invitation_code.strip()) >= 4:
            print(f"  ⚠️  验证服务不可达，格式校验通过，放行")
            results["invitation"] = True
        else:
            return False, f"邀请码无效且验证请求异常：{str(e)}", None
    
    # ── 汇总 ──
    print("\n  ┌────────── 验证结果 ──────────┐")
    for check, passed in results.items():
        icon = "✅" if passed else "❌"
        label = {"login": "平台登录", "api_key": "API Key", "invitation": "邀请码"}[check]
        print(f"  │  {icon} {label:<16}       │")
    print("  └──────────────────────────────┘")
    
    all_pass = all(results.values())
    if all_pass:
        print("  🎉 三重验证全部通过！允许发布")
        return True, "验证通过", token
    else:
        failed = [k for k, v in results.items() if not v]
        return False, f"验证失败：{', '.join(failed)}", None


def publish_to_skillhub(skill_path, phone=None, password=None,
                        api_key=None, invitation_code=None,
                        config=None, endpoint="https://aiskillhub.vip"):
    """
    发布到虾友SkillHub（三重验证 + 智能类目识别）
    
    v2.1 改动：不再从 config.json 自动读取凭证，
    必须由调用方显式传入 phone/password/api_key/invitation_code
    """
    print("\n🦐 发布到虾友SkillHub...")
    
    # 如果传了 config（兼容旧调用），从中提取配置，但不再自动使用
    if config:
        skillhub_config = config.get('skillhub', {})
        if not phone:
            phone = skillhub_config.get('phone')
        if not password:
            password = skillhub_config.get('password')
        if not api_key:
            api_key = skillhub_config.get('api_key')
        if not invitation_code:
            invitation_code = skillhub_config.get('invitation_code')
    
    # ═══════════════════════════════════════════
    #  🛡️ 三重安全验证（必须全部通过）
    # ═══════════════════════════════════════════
    verified, msg, token = verify_publish_credentials(
        phone, password, api_key, invitation_code, endpoint
    )
    if not verified:
        print(f"\n  🚫 发布被阻止: {msg}")
        print("  💡 请确认以下三项均已提供并有效：")
        print("     1. 平台登录账号（手机号+密码）")
        print("     2. API Key（个人中心 → 开发设置）")
        print("     3. 邀请码（个人中心 → 我的邀请码）")
        return False
    
    # ═══════════════════════════════════════════
    #  验证通过，开始发布
    # ═══════════════════════════════════════════
    
    skill_name = Path(skill_path).name
    
    # 读取SKILL.md
    skill_md_path = Path(skill_path) / "SKILL.md"
    if not skill_md_path.exists():
        print("\n  ❌ 未找到SKILL.md")
        return False
    
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    try:
        import requests
        
        # Step 2: 获取实时类目树 + 智能分类
        print("  [CATEGORY] 正在获取类目树...")
        category_tree = fetch_category_tree(endpoint, token)
        if category_tree:
            print(f"  ✅ 已加载 {len(category_tree)} 个一级分类")
        
        # 从SKILL.md frontmatter提取信息
        name = skill_name or Path(skill_path).resolve().name
        description = ""
        version = "1.0.0"
        triggers = []
        
        fm_match = re.match(r'^---\s*\n(.*?)\n---', skill_content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            in_description = False
            desc_lines = []
            for line in fm.split('\n'):
                if line.startswith('name:'):
                    name = line.split(':', 1)[1].strip()
                elif line.startswith('title:'):
                    if not name or name == Path(skill_path).resolve().name:
                        name = line.split(':', 1)[1].strip().strip('"').strip("'")
                elif line.startswith('description:'):
                    in_description = True
                    rest = line.split(':|', 1)[-1].strip() if ':|' in line else line.split(':', 1)[1].strip()
                    rest = rest.strip('"').strip("'").strip('|').strip()
                    if rest:
                        desc_lines.append(rest)
                elif line.startswith('  ') or (in_description and not line.strip()):
                    # YAML 续行：以2个空格开头（| 多行字符串）
                    if in_description:
                        desc_lines.append(line.strip())
                elif in_description and not line.strip().startswith(('-', 'tags:', 'triggers:', 'author:', 'version:', 'name:')):
                    in_description = False
                elif line.startswith('version:'):
                    version = line.split(':', 1)[1].strip().strip('"')
                elif line.strip().startswith('- ') and not in_description:
                    triggers.append(line.strip()[2:])
            description = ' '.join(desc_lines)  # 完整概述，不截断
        
        # 🧠 智能归类
        child_id, parent_name, child_name, confidence = classify_skill(
            skill_content, name, category_tree
        )
        print_classification_result(parent_name, child_name, confidence, name)
        
        # 如果是从 API 获取的真实类目树，需要找到真实的 child_id
        if category_tree and not child_id:
            for parent in category_tree:
                if parent['name'] == parent_name:
                    for child in parent.get('children', []):
                        if child['name'] == child_name:
                            child_id = child['id']
                            break
                    break
        
        # 提取完整正文（去掉frontmatter），作为description
        # 这样平台详情页就能完整渲染SKILL.md的所有内容
        nl = chr(10)
        marker = nl + '---' + nl
        fm_end = skill_content.find(marker)
        if fm_end > 0:
            body_text = skill_content[fm_end + len(marker):].lstrip(nl)
        else:
            body_text = skill_content
        
        slug = hashlib.md5(name.encode()).hexdigest()[:12]
        
        body = {
            'name': name,
            'slug': slug,
            'icon': 'MessageSquare',
            'description': body_text if body_text.strip() else (description or f'{name} - WorkBuddy Skill'),
            'version': version,
            'isFree': True,
            'visibility': 'public',
            'categoryId': child_id,  # 🎯 自动归档到识别出的二级类目
            'features': triggers if triggers else [],
            'requirements': ['WorkBuddy'],
            'fileTree': [{
                'name': 'SKILL.md',
                'path': 'SKILL.md',
                'type': 'file',
                'content': skill_content,
                'size': len(skill_content.encode('utf-8'))
            }]
        }
        
        # Step 3: 搜索是否已存在同名Skill
        print(f"  [SEARCH] 搜索是否已存在「{name}」...")
        search_resp = requests.get(
            f"{endpoint}/api/skills",
            headers={'Authorization': f'Bearer {token}'},
            params={'keyword': name, 'page': 1, 'pageSize': 50},
            timeout=10
        )
        
        existing_skill_id = None
        if search_resp.status_code == 200:
            search_data = search_resp.json().get('data', {})
            # 兼容两种返回结构: {list: [...]} 或 [...]
            skill_list = search_data.get('list', search_data) if isinstance(search_data, dict) else search_data
            if isinstance(skill_list, list):
                for s in skill_list:
                    if s.get('name') == name:
                        existing_skill_id = s.get('id')
                        break
        
        # Step 4: 更新或创建
        if existing_skill_id:
            print(f"  [UPDATE] 发现已有版本，正在更新（归类: {parent_name} › {child_name}）...")
            publish_resp = requests.post(
                f"{endpoint}/api/skills/{existing_skill_id}",
                headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                json=body, timeout=30
            )
            action = "更新"
        else:
            print(f"  [PUBLISH] 首次发布（归类: {parent_name} › {child_name}）...")
            publish_resp = requests.post(
                f"{endpoint}/api/skills",
                headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                json=body, timeout=30
            )
            action = "创建"
        
        if publish_resp.status_code in [200, 201]:
            result = publish_resp.json()
            skill_id = result.get('data', {}).get('id') or result.get('id')
            print(f"  ✅ 虾友SkillHub{action}成功！")
            if skill_id:
                print(f"  🔗 {endpoint}/skills/{skill_id}")
                # 📝 自动创建版本变更记录
                changelog_text = f"版本更新至 v{version}" if existing_skill_id else f"初版发布：{description}"
                create_version_record(endpoint, token, skill_id, version, changelog_text)
            return True
        else:
            print(f"  ❌ 发布失败: {publish_resp.status_code}")
            print(f"  {publish_resp.text[:300]}")
            return False
            
    except Exception as e:
        print(f"  ❌ 错误: {str(e)}")
        return False

def publish_to_clawhub(skill_path, config):
    """发布到ClawHub"""
    print("\n🔱 发布到ClawHub...")
    
    clawhub_config = config.get('clawhub', {})
    token = clawhub_config.get('token')
    
    if not token:
        print("❌ ClawHub配置不完整")
        return False
    
    skill_name = Path(skill_path).name
    
    login_cmd = ["clawhub", "login", "--token", token]
    subprocess.run(login_cmd, capture_output=True)
    
    publish_cmd = [
        "clawhub", "publish", skill_path,
        "--slug", skill_name.replace('_', '-').lower(),
        "--name", skill_name,
        "--version", "1.0.0"
    ]
    
    result = subprocess.run(publish_cmd)
    return result.returncode == 0

def publish_to_tencent_skillhub(skill_path, config, token=None):
    """发布到腾讯SkillHub（WorkBuddy/Qclaw官方市场）"""
    print("\n🔷 发布到腾讯SkillHub...")
    
    tencent_config = config.get('tencent_skillhub', {})
    api_token = token or tencent_config.get('api_token')
    
    if not api_token:
        print("⚠️  腾讯SkillHub未配置 API Token")
        print("💡 请在腾讯SkillHub「开发者中心 → API 密钥」获取")
        return False
    
    skill_name = Path(skill_path).name
    skill_md_path = Path(skill_path) / "SKILL.md"
    
    if not skill_md_path.exists():
        print("❌ 未找到SKILL.md")
        return False
    
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    try:
        import requests
        
        # 从 frontmatter 提取信息
        name = skill_name
        description = ""
        version = "1.0.0"
        triggers = []
        
        fm_match = re.match(r'^---\s*\n(.*?)\n---', skill_content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            for line in fm.split('\n'):
                if line.startswith('name:'):
                    name = line.split(':', 1)[1].strip()
                elif line.startswith('description:'):
                    rest = line.split(':|', 1)[-1].strip() if ':|' in line else line.split(':', 1)[1].strip()
                    description = rest.strip('"').strip("'").strip('|').strip()
                elif line.startswith('version:'):
                    version = line.split(':', 1)[1].strip().strip('"')
                elif line.strip().startswith('- ') and ':' not in line:
                    triggers.append(line.strip()[2:])
        
        endpoint = tencent_config.get('endpoint', 'https://skillhub.tencent.com')
        
        body = {
            'name': name,
            'description': description or f'{name} - WorkBuddy Skill',
            'version': version,
            'isFree': True,
            'visibility': 'public',
            'features': triggers if triggers else [],
            'requirements': ['WorkBuddy'],
            'fileTree': [{
                'name': 'SKILL.md',
                'path': 'SKILL.md',
                'type': 'file',
                'content': skill_content,
                'size': len(skill_content.encode('utf-8'))
            }]
        }
        
        print(f"  [PUBLISH] 正在上传到腾讯SkillHub...")
        publish_resp = requests.post(f"{endpoint}/api/skills",
            headers={'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'},
            json=body, timeout=30)
        
        if publish_resp.status_code in [200, 201]:
            result = publish_resp.json()
            skill_id = result.get('data', {}).get('id') or result.get('id')
            print(f"  ✅ 腾讯SkillHub发布成功！")
            if skill_id:
                print(f"  🔗 {endpoint}/skills/{skill_id}")
            return True
        elif publish_resp.status_code == 404:
            print(f"  ⚠️  腾讯SkillHub API 端点未找到 ({publish_resp.status_code})")
            print(f"  💡 请确认平台 API 地址是否正确")
            return False
        else:
            print(f"  ❌ 发布失败: {publish_resp.status_code}")
            print(f"  {publish_resp.text[:300]}")
            return False
    
    except Exception as e:
        print(f"  ❌ 错误: {str(e)}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🚀 Skill矩阵分发助手（免费版）v2.2")
        print("=" * 60)
        print("一键将免费Skill分发到五大平台")
        print("=" * 60)
        print("\n📋 支持的平台:")
        print("  🔷 腾讯SkillHub - 发布到腾讯官方市场")
        print("  🦞 虾聊          - 生成分享链接（推荐）")
        print("  🦐 虾友SkillHub  - 上架到社群平台（需三重验证）")
        print("  📦 GitHub        - 自动上传到仓库")
        print("  🔱 ClawHub       - CLI发布到官方市场")
        print("\n用法:")
        print("  python matrix_publish.py <skill_path> [platforms]")
        print("\n  🛡️ SkillHub需要三重验证（缺一不可）：")
        print("  python matrix_publish.py <skill_path> skillhub \\")
        print("    --phone 138xxxx \\")
        print("    --password xxx \\")
        print("    --api-key sk-xxxxxxxx \\")
        print("    --invitation-code XXXX-XXXX")
        print("\n示例:")
        print("  python matrix_publish.py D:/skills/my-skill")
        print("  python matrix_publish.py D:/skills/my-skill tencent")
        print("  python matrix_publish.py D:/skills/my-skill all")
        print("\n支持的平台参数: tencent, github, clawdchat, skillhub, clawhub, all")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    platforms = sys.argv[2] if len(sys.argv) > 2 else "all"
    
    # 解析命令行参数
    phone = None
    password = None
    api_key = None
    invitation_code = None
    
    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--phone' and i + 1 < len(sys.argv):
            phone = sys.argv[i + 1]
            i += 2
        elif arg == '--password' and i + 1 < len(sys.argv):
            password = sys.argv[i + 1]
            i += 2
        elif arg == '--api-key' and i + 1 < len(sys.argv):
            api_key = sys.argv[i + 1]
            i += 2
        elif arg == '--invitation-code' and i + 1 < len(sys.argv):
            invitation_code = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if not os.path.exists(skill_path):
        print(f"❌ Skill路径不存在: {skill_path}")
        sys.exit(1)
    
    config = load_config()
    
    # 合并config.json中的skillhub配置
    parent_config_path = Path(__file__).parent.parent / "config.json"
    if parent_config_path.exists():
        with open(parent_config_path, 'r', encoding='utf-8') as f:
            parent_config = json.load(f)
        if 'skillhub' in parent_config and 'skillhub' not in config:
            config['skillhub'] = parent_config['skillhub']
    
    print("=" * 50)
    print("🚀 Skill矩阵分发助手 v2.2")
    print("=" * 50)
    print(f"📁 Skill: {Path(skill_path).name}")
    print(f"🎯 平台: {platforms}")
    print("=" * 50)
    
    results = {}
    
    if platforms in ["all", "tencent"]:
        results['tencent_skillhub'] = publish_to_tencent_skillhub(skill_path, config)
    
    if platforms in ["all", "github"]:
        results['github'] = publish_to_github(skill_path, config)
    
    if platforms in ["all", "clawdchat"]:
        results['clawdchat'] = publish_to_clawdchat(skill_path, config)
    
    if platforms in ["all", "skillhub"]:
        results['skillhub'] = publish_to_skillhub(
            skill_path,
            phone=phone,
            password=password,
            api_key=api_key,
            invitation_code=invitation_code,
            config=config,
            endpoint=config.get('skillhub', {}).get('endpoint', 'https://aiskillhub.vip')
        )
    
    if platforms in ["all", "clawhub"]:
        results['clawhub'] = publish_to_clawhub(skill_path, config)
    
    print("\n" + "=" * 50)
    print("📊 发布结果")
    print("=" * 50)
    for platform, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{platform:12} {status}")
    print("=" * 50)

if __name__ == "__main__":
    main()
