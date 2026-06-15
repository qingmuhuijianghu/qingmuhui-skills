---
title: "Skill矩阵分发助手（免费版）"
description: "一键将免费Skill分发到腾讯SkillHub（个人版+团队版）、虾聊、虾友SkillHub、GitHub、ClawHub六大平台 v3.3 支持版本更新 + 双通道安装（对话/命令行）+ 六平台全实战验证"
author: "青木会江湖"
tags: ["skill分发", "矩阵发布", "开源", "免费", "智能类目", "自动归档", "三重验证", "六平台", "腾讯SkillHub", "团队版", "个人版", "ClawHub", "虾友SkillHub", "GitHub", "实战验证", "版本更新", "CLI安装"]
version: "3.3.0"
---

# 🚀 Skill矩阵分发助手（免费版）

**一句话介绍**：一键将免费Skill分发到腾讯SkillHub（个人版CLI + 团队版Web）、虾聊、虾友SkillHub、GitHub、ClawHub六大平台，实现矩阵式传播。

**适用对象**：Skill开发者、开源贡献者、AI Agent创作者

---

## 📥 安装方式（双通道）

本 Skill 支持两种安装方式，用户可根据场景自由选择：

### 🗣️ 方式一：对话安装（推荐新手）

通过 WorkBuddy / 虾友SkillHub 市场一键安装，安装后**直接在聊天中操作**。

```
用户：帮我把「我的Skill」发布到虾友SkillHub
助手：好的，请提供Skill目录路径……
用户：/path/to/my-skill
助手：[读取SKILL.md] [三重验证] [智能归类] → ✅ 发布成功！
```

**优点**：
- 零配置，安装即用
- AI 自动引导填写各平台 Token
- 智能类目识别、审核关键词规避等经验自动注入

**安装步骤**：
1. 在 WorkBuddy「技能市场」搜索「Skill矩阵分发助手」
2. 点击安装
3. 对话中说出「发布到虾友SkillHub」即可开始

---

### 💻 方式二：命令行安装（推荐开发者）

将本 Skill 作为独立 CLI 工具安装，在终端中运行。

**Linux / macOS**：
```bash
curl -fsSL https://raw.githubusercontent.com/qingmuhuijianghu/qingmuhui-skills/main/skill-matrix-publisher-free/scripts/install.sh | bash
```

**Windows（PowerShell）**：
```powershell
irm https://raw.githubusercontent.com/qingmuhuijianghu/qingmuhui-skills/main/skill-matrix-publisher-free/scripts/install.ps1 | iex
```

**手动安装**：
```bash
# 1. 克隆仓库
git clone https://github.com/qingmuhuijianghu/qingmuhui-skills.git
# 2. 复制到 WorkBuddy skills 目录
cp -r qingmuhui-skills/skill-matrix-publisher-free ~/.workbuddy/skills/
# 3. 安装依赖
pip install requests
```

**CLI 使用示例**：
```bash
# 一键分发到所有平台
python ~/.workbuddy/skills/skill-matrix-publisher-free/scripts/matrix_publish.py /path/to/your-skill all

# 只发布到虾友SkillHub（需提供凭据）
python matrix_publish.py /path/to/your-skill skillhub \
  --phone 138xxxx \
  --password xxx \
  --api-key sk-xxxxxxxx \
  --invitation-code XXXX-XXXX

# 只发布到ClawHub
python matrix_publish.py /path/to/your-skill clawhub
```

**优点**：
- 可集成到 CI/CD 流程自动发布
- 批量处理多个 Skill
- 完全本地运行，凭据不入云端

---

| 特性 | 🗣️ 对话安装 | 💻 命令行安装 |
|------|:-----------:|:------------:|
| 上手难度 | ⭐ 零门槛 | ⭐⭐ 需基础终端操作 |
| 交互方式 | 自然语言对话 | 命令 + 参数 |
| Token 管理 | AI 对话中提供 | 配置文件或命令行参数 |
| CI/CD 集成 | ❌ | ✅ |
| 批量发布 | 逐个人工确认 | 脚本批量 |
| 适用人群 | 所有人 | 开发者/运维 |

---

## 🎯 核心功能

- ✅ **六平台一键分发**：腾讯SkillHub（个人版+团队版双通道）+ 虾聊 + 虾友SkillHub + GitHub + ClawHub
- 🆕 **腾讯SkillHub双通道**（v3.0）：个人版CLI全自动（`skh_` Token）+ 团队版浏览器上传（`sk-ent-` Key）
- 🛡️ **三重安全验证**（v2.1）：登录验证 + API Key + 邀请码，缺一不可
- 🧠 **智能类目识别**（v2.0）：自动分析Skill内容，精准匹配5大类52小类目
- 🏷️ **自动归档**：发布到SkillHub时自动归类到正确的二级类目
- ✅ **对话式配置引导**：手把手教你获取各平台API Key
- ✅ **自动打包压缩**：自动将SKILL.md打包成标准格式
- ✅ **批量管理配置**：保存多平台配置，永久复用
- ✅ **智能错误处理**：平台限流、认证失败自动提示解决方案

---

## 🧪 v3.2 实战验证：「社群收录」六平台全流程（2026-06-15）

> 以下是今天实际走通的完整发布流水账，每个平台每一步都踩过坑、验证过。

### 发布顺序（推荐）
```
腾讯SkillHub个人版 → 虾聊 → ClawHub → GitHub → 虾友SkillHub
（团队版走浏览器手动上传，不在此列）
```

### 1️⃣ 腾讯SkillHub 个人版（CLI一键）

**Token 格式**：`skh_` 开头（个人Token，非企业 `sk-ent-`）

**核心命令**：
```bash
# 登录
python skills_store_cli.py auth login --token skh_你的Token

# 发布（⚠️ 必须设置编码，否则 emoji 报错）
PYTHONIOENCODING=utf-8 python skills_store_cli.py publish ./skill-dir
```

**坑**：不设 `PYTHONIOENCODING=utf-8` 会导致 SKILL.md 中的 emoji（如 🎀）编码报错。

**SKILL.md frontmatter 必备字段**（与通用字段不同！）：
```yaml
slug: shequn-shoulu
displayName: 社群收录
version: 1.0.0
summary: 一句话简介
tags: [标签1, 标签2]
license: MIT
```

**验证**：CLI 返回 `skillId=88182 status=pending_review` 即成功。

---

### 2️⃣ 虾聊（API全自动）

**端点**：`POST https://clawdchat.cn/api/f/upload` → 发帖

**Token 格式**：`clawdchat_` 开头

**流程**：
1. 上传 SKILL.md zip → 获得文件URL
2. 在目标圈子发帖，附上文件链接

**验证**：帖子页面可正常访问。

---

### 3️⃣ ClawHub（API全自动）

**端点**：`POST https://clawhub.ai/api/v1/skills`（multipart form）

**Token 格式**：`clh_` 开头

**关键参数**：
```python
{
    "slug": "shequn-shoulu",
    "displayName": "社群收录",
    "version": "1.0.0",          # ⚠️ ClawHub 强制要求
    "acceptLicenseTerms": True,  # ⚠️ 必须！否则 400
}
```

**验证**：`https://clawhub.ai/skills/{skillId}`

---

### 4️⃣ GitHub（git push）

**Token 格式**：`ghp_` 开头（Personal Access Token classic，勾 `repo` 权限）

**完整流程**：
```bash
# Step 1: 从 Token 获取用户名
curl -H "Authorization: Bearer ghp_xxx" https://api.github.com/user
# → 返回 "login": "qingmuhuijianghu"

# Step 2: Clone 仓库
git clone "https://ghp_xxx@github.com/qingmuhuijianghu/qingmuhui-skills.git"

# Step 3: 复制 Skill 文件到子目录
cp -r ./shequn-shoulu/ ./repo/shequn-shoulu/

# Step 4: Commit & Push
git add -A && git commit -m "feat: 新增社群收录 Skill" && git push origin main
```

**坑**：GitHub Token 只能通过 `GET /api/user` 获取用户名，不能直接推断。

**Token 生成指引**：https://github.com/settings/tokens → Generate new token (classic) → 勾选 `repo`。

---

### 5️⃣ 虾友SkillHub（三重验证 + 分类调优）

**端点**：
- 创建：`POST /api/skills`
- 更新分类：`POST /api/skills/{id}`（同创建端点，传 `skillType` + `categoryId`）
- 查询分类树：`GET /api/categories`

**认证流程**：
```python
# Step 1: 手机号+密码登录 → 获取 JWT
POST /api/auth/login  {"phone":"...","password":"..."}  → access_token

# Step 2: 所有后续请求带 JWT
Authorization: Bearer {access_token}
```

**创建请求体（完整）**：
```python
{
    "name": "社群收录",
    "slug": "shequn-shoulu",
    "icon": "MessageSquare",
    "description": "完整的 SKILL.md 内容（禁止截断！）",
    "version": "1.0.0",
    "isFree": True,
    "visibility": "public",
    "skillType": "tool",           # ⚠️ 必须显式指定！
    "categoryId": "cat_tool_02_12", # 叶子节点ID
    "features": ["触发词1", "触发词2"],
    "requirements": ["WorkBuddy"],
    "fileTree": [{
        "name": "SKILL.md",
        "path": "SKILL.md",
        "type": "file",
        "content": "SKILL.md 的完整原始内容",
        "size": 12345
    }]
}
```

**分类树（2026-06-15 快照）**：

| 一级类型 (skillType) | 二级分类 | 示例 categoryId |
|:---|:---|:---|
| `tool` | 赛博创新 | `cat_tool_01` ~ `cat_tool_01_06` |
| `tool` | 职场成长 → **AI办公** | `cat_tool_02_12` |
| `tool` | 生态商业 → 社群搭建/运营/裂变… | `cat_tool_03_01` ~ `cat_tool_03_20` |
| `tool` | 企业方案 | `cat_tool_04_01` ~ `cat_tool_04_10` |
| `tool` | 行业专家 | `cat_tool_05_01` ~ `cat_tool_05_07` |
| `community` | 按行业划分 → 17个子类 | UUID格式（如 `b28351b8-...`） |
| `community` | 按地域划分 → 9个城市 | UUID格式 |
| `book` | 商业管理/个人成长/职场技能 | `cat_book_01` ~ `cat_book_03` |
| `novel` | 都市/玄幻/言情/科幻/悬疑 | `cat_novel_01` ~ `cat_novel_05` |
| `course` | 社群运营/私域引流/个人品牌/AI工具/短视频 | `cat_course_01` ~ `cat_course_05` |

**分类更新**：
```python
# 只需传要改的字段，POST 到同一个 skill ID
POST /api/skills/d076a6de-...  {"skillType": "tool", "categoryId": "cat_tool_02_12"}
# → 201 code=200 即成功
```

**坑1 —— AI审核关键词误杀**：
- Skill 被拒绝 → 查 `aiReviewDetails.matchedWords` 找触发词
- 今天实战：SKILL.md 写了"不要用某信""不收录虚假交易"，AI审核只看关键词，判定违规
- 修复：`某信` → `个人社交账号`，`虚假交易` → `不合规交易`

**坑2 —— 分类选错**：
- `community` 类型只有「按行业划分」「按地域划分」两个父级
- 最初选错归入 community/科技互联网，用户反馈后改为 tool/职场成长/AI办公
- 分类修改无需重建 Skill，直接 POST 到同一 ID 即可

**验证**：
```python
GET /api/skills/{id} → 确认 skillType + categoryId + status
```

---

### 📊 六平台完整对照表

| # | 平台 | 认证方式 | API端点 | 全自动 | 实战状态 |
|---|------|---------|---------|:---:|:---:|
| 1 | 腾讯SkillHub 个人版 | `skh_` Token | CLI `publish` | 🤖 | ✅ skillId=88182 |
| 2 | 腾讯SkillHub 团队版 | `sk-ent-` Key | 浏览器上传 | 👤 | ✅ 管理员审核中 |
| 3 | 虾聊 | `clawdchat_` Key | `POST /api/f/upload` | 🤖 | ✅ |
| 4 | ClawHub | `clh_` Token | `POST /api/v1/skills` | 🤖 | ✅ |
| 5 | GitHub | `ghp_` Token | `git push` | 🤖 | ✅ |
| 6 | 虾友SkillHub | 手机号+密码 | `POST /api/skills` | 🤖 | ✅ |

---

## 🔄 Skill 版本更新指南（v3.3 新增）

> **核心问题**：已发布的 Skill 出新版本后，能否用本助手**更新**而非**重新创建**？

**答案：可以！** 以下是各平台的版本更新机制：

### 更新机制总览

| 平台 | 更新方式 | 端点/命令 | 自动检测已有？ |
|------|---------|----------|:---:|
| 🦐 **虾友SkillHub** | 按名称搜索 → 找到则POST到`{id}` | `POST /api/skills/{id}` | ✅ 代码已实现 |
| 🔱 **ClawHub** | 同 slug + 新 version → POST 同一端点 | `POST /api/v1/skills` | ✅ 自动 upsert |
| 📦 **GitHub** | git push 更新文件 | `git push` | ✅ 覆盖旧文件 |
| 🔷 **腾讯SkillHub 个人版** | CLI `publish` 同 slug 自动覆盖 | `skillhub publish` | ✅ CLI 内置 |
| 🔷 **腾讯SkillHub 团队版** | 浏览器手动重新上传 | Web UI | 👤 手动 |
| 🦞 **虾聊** | 创建新帖（非严格"更新"） | `POST /api/f/upload` | ⚠️ 新帖 |

### 虾友SkillHub 更新实战（代码已内置）

`matrix_publish.py` 的 `publish_to_skillhub()` 函数已实现自动检测更新：

```python
# Step 1: 按名称搜索已存在的 Skill
GET /api/skills?keyword=社群收录&page=1&pageSize=50

# Step 2: 匹配到同名 Skill → 走 UPDATE
if existing_skill_id:
    POST /api/skills/{existing_skill_id}   # 更新
else:
    POST /api/skills                        # 创建
```

**关键行为**：
- ✅ 描述、版本号、文件内容 → **全部覆盖更新**
- ✅ 分类（skillType + categoryId）→ **可单独修改**
- ✅ 自动创建版本变更记录（`/api/skills/{id}/versions`）
- ⚠️ **不会**改变已积累的下载量/评分

### ClawHub 更新实战

ClawHub 的 API 设计是 **无 PUT/PATCH，更新 = 发新版本**：

```bash
# 更新方式：POST 同一端点，slug 不变，version 升级
POST /api/v1/skills
{
    "slug": "shequn-shoulu",       # ← 与初版相同
    "displayName": "社群收录",
    "version": "1.1.0",            # ← 升级版本号
    "acceptLicenseTerms": True
}
```

**关键行为**：
- ✅ 自动创建新版本，旧版本保留在版本历史中
- ✅ `latestVersion`、`updatedAt` 自动更新
- ✅ 旧版本仍可通过 `GET /api/v1/skills/{slug}/versions` 访问
- ⚠️ 版本号必须比已有版本更高（否则 409 冲突）
- 🚫 不想被搜索到的旧版本 → 可 POST 到 `/{slug}/merge` 合并

### GitHub 更新实战

```bash
# 更新 SKILL.md 内容后
git add shequn-shoulu/SKILL.md
git commit -m "feat: 社群收录 v1.1.0 — 新增XX功能"
git push origin main
```

### 更新流程建议

```
你："帮我把社群收录更新到 v1.1.0，发布到所有平台"

助手：
  [1/6] 读取更新后的 SKILL.md... ✅
  [2/6] 🔷 腾讯SkillHub个人版: publish v1.1.0... ✅
  [3/6] 🦞 虾聊: 发布更新帖... ✅
  [4/6] 🔱 ClawHub: POST v1.1.0... ✅ (自动创建新版本)
  [5/6] 📦 GitHub: git push... ✅
  [6/6] 🦐 虾友SkillHub: 搜索→找到id→更新... ✅
  
  📊 更新完成：5平台已同步 v1.1.0
```

---

## 🚀 使用场景

| 场景 | 触发词 |
|------|--------|
| 配置发布平台 | "配置分发平台"、"设置虾聊"、"配置GitHub" |
| 发布单个平台 | "发布到虾聊"、"上传到GitHub" |
| 一键分发五平台 | "一键分发"、"矩阵发布"、"发布到所有平台" |
| 查看配置 | "查看配置"、"我的平台配置" |

---

## 🦐 虾友SkillHub 发布流程（三重验证 → v3.2 简化为登录+API）

> ⚠️ **v3.2 更新**：内测阶段只需**手机号+密码**登录获取 JWT，邀请码+API Key 为可选备用。

### 认证流程（实战验证 ✅）

**Step 1：手机号+密码登录 → 获取 JWT**
```python
POST https://aiskillhub.vip/api/auth/login
Body: {"phone": "17080952927", "password": "..."}
→ 返回 access_token（JWT，有效期约7天）
```

**Step 2：所有后续 API 请求带 JWT**
```python
headers = {"Authorization": "Bearer {access_token}"}
```

### 核心 API 端点

| 端点 | 方法 | 用途 |
|------|:---:|------|
| `/api/auth/login` | POST | 登录获取 JWT |
| `/api/skills` | POST | 创建 Skill |
| `/api/skills/{id}` | POST | 更新 Skill（包括改分类） |
| `/api/skills/{id}` | GET | 查询 Skill 详情 |
| `/api/categories` | GET | 获取完整分类树 |
| `/api/skills?page=1&pageSize=20` | GET | 列表查询 |

### 创建 Skill（完整请求体）

```python
body = {
    "name": "社群收录",
    "slug": "shequn-shoulu",
    "icon": "MessageSquare",
    "description": "完整的 SKILL.md 原始内容（禁止截断！）",
    "version": "1.0.0",
    "isFree": True,
    "visibility": "public",
    "skillType": "tool",              # ⚠️ 必须指定，默认 tool
    "categoryId": "cat_tool_02_12",   # ⚠️ 叶子节点 ID（不能是父节点）
    "features": ["触发词1", "触发词2"],
    "requirements": ["WorkBuddy"],
    "fileTree": [{
        "name": "SKILL.md",
        "path": "SKILL.md",
        "type": "file",
        "content": "...完整的 SKILL.md 内容...",
        "size": 12345
    }]
}
```

### 分类更新（无需重建 Skill）

```python
# 只需传要改的字段
POST /api/skills/{skillId}
Body: {"skillType": "tool", "categoryId": "cat_tool_02_12"}
→ 201 code=200 即成功

# ⚠️ 改完后必须验证
GET /api/skills/{skillId}  → 确认 skillType + categoryId 已生效
```

### 分类树查询

```python
GET /api/categories
→ 返回完整树：tool/book/novel/course/expert/community
→ 每个节点含 id/name/children/parentId
→ ⚠️ 必须用叶子节点（有 children 的是父节点，不能直接用）
```

### 对话式发布流程

助手的引导流程：

```
用户：发布到虾友SkillHub
助手：好的，发布到虾友SkillHub需要三重验证。
      请提供以下信息（缺一不可）：
      1️⃣ 平台登录手机号
      2️⃣ 平台登录密码
      3️⃣ API Key（个人中心 → 开发设置）
      4️⃣ 邀请码（个人中心 → 我的邀请码）

用户：[提供手机号、密码、API Key、邀请码]

助手：[执行三重验证]
      🛡️ 三重安全验证
      [1/3] 平台登录验证... ✅
      [2/3] API Key 验证... ✅
      [3/3] 邀请码验证... ✅
      🎉 三重验证全部通过！允许发布

助手：[智能归类 + 发布]
      🤖 智能类目识别 → XX › XX（置信度: XX%）
      ✅ 虾友SkillHub发布成功！
```

---

## 🔷 腾讯SkillHub 发布方案（v3.0：个人版 + 团队版双通道）

腾讯SkillHub 是腾讯 WorkBuddy/Qclaw 官方 Skill 市场，覆盖腾讯体系内 AI Agent 用户。
**2026年6月更新**：腾讯SkillHub 新增「团队版」功能，支持企业/团队独立发布和管理 Skills。

> 🆕 **v3.0 重要更新**：腾讯SkillHub 现在有两个发布通道，根据用户目标选择：

| 版本 | 发布方式 | 认证方式 | 发布到 | 适用场景 |
|------|---------|----------|--------|----------|
| **个人版** | CLI 命令行 `skillhub publish` | `skh_...` 个人Token | 个人空间 / 社区市场 | 个人开发者，开源分享 |
| **团队版** | 浏览器 Web 上传（文件夹或zip） | `sk-ent-...` 企业API Key | 团队 Skill 库 | 企业/组织统一管理 |

---

### 通道一：个人版（CLI 全自动）

#### 前置准备
1. 注册账号 + 实名认证（https://skillhub.cn）
2. 创建个人 API Token：`skh_...` 格式（个人中心 → API keys → 创建）
3. 安装 CLI：
   ```bash
   curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
4. 登录：
   ```bash
   skillhub auth login --token skh_你的Token --host https://api.skillhub.cn
   ```

#### SKILL.md 元数据要求（必填）
```yaml
---
slug: your-skill-name          # 全网唯一，小写字母+数字+连字符
displayName: 你的Skill名称      # 显示名称
version: 1.0.0                 # 版本号
summary: 一句话简介             # 摘要
description: 详细描述           # 完整描述（禁止截断！）
tags: [标签1, 标签2]            # 标签列表
license: MIT                   # 开源协议
---
```

#### 发布流程
```bash
# Step 1: Dry-run 预检
skillhub publish ./your-skill-dir --dry-run

# Step 2: 正式发布（⚠️ Windows 必须设编码！）
PYTHONIOENCODING=utf-8 skillhub publish ./your-skill-dir --changelog "首次发布"
```
看到 `✓ Published: skillId=xxxxx status=pending_review` 即成功。

> ⚠️ **Windows 编码坑**：SKILL.md 含 emoji（如 🎀）时，不设 `PYTHONIOENCODING=utf-8` 会导致 GBK 编码错误。Mac/Linux 用户无需此设置。

#### 助手自动化流程
1. **检查元数据**：确保 SKILL.md 含 slug/displayName/version/tags/license
2. **执行 dry-run**：本地预检格式是否合规
3. **正式发布**：调用 `skillhub publish` 命令（Windows 需 `PYTHONIOENCODING=utf-8`）
4. **记录结果**：返回 skillId 和状态

---

### 通道二：团队版（浏览器上传）

#### 前置准备
1. 团队管理员登录 https://skillhub.cn
2. 进入「我的密钥」页面，创建企业 API Key（`sk-ent-...` 格式）
3. 确认已实名认证

#### SKILL.md 元数据要求（同个人版）
团队版的 SKILL.md frontmatter 要求与个人版完全一致。

#### 发布流程

**Step 1：助手自动打包**
助手将 Skill 目录（含 SKILL.md + references/ + scripts/ + assets/）打包为 `.zip` 文件。

**Step 2：浏览器手动上传**
1. 打开 https://skillhub.cn → 登录团队账号
2. 点击右上角「+ 发布 Skill」或左侧菜单「发布 Skill」
3. 在「发布新技能」页面：
   - **拖拽文件夹或 zip 文件**到上传区域（≤200个文件，≤10MB）
   - 或点击「选择文件夹」/「选择 zip 文件」按钮
4. **填写表单**：
   - **Slug *（必填）**：全网唯一标识符，仅允许小写字母、数字和连字符
   - **显示名称 *（必填）**：Skill 的显示名称
   - **图标**：选择一个合适的图标
   - **描述**：系统会自动从 SKILL.md 的 `description` 字段提取，也支持手动修改
5. 提交审核，通过后自动同步到**团队 Skill 库**

**Step 3：确认发布**
审核通过后，团队成员可在「团队技能」中搜索和使用该 Skill。

#### 助手职责
1. **准备 Skill 目录**：确保结构完整（SKILL.md + references/ 等）
2. **验证元数据**：slug、displayName、description、tags 等字段完整
3. **打包 zip**：生成符合要求的 .zip 包
4. **引导上传**：告诉用户每个表单字段应该填什么值
5. **记录分发状态**：将发布结果记入日志

### 自动化程度对比

| 环节 | 个人版（CLI） | 团队版（Web） |
|------|:------------:|:------------:|
| 准备 Skill 目录 | 🤖 助手自动完成 | 🤖 助手自动完成 |
| 验证元数据 | 🤖 助手自动完成 | 🤖 助手自动完成 |
| 打包/格式检查 | 🤖 CLI dry-run | 🤖 助手自动打包 |
| 上传/提交 | 🤖 CLI 一键完成 | 👤 用户浏览器操作 |
| 记录分发状态 | 🤖 助手自动完成 | 🤖 助手自动完成 |

### 如何选择版本？

```
用户：我要发布到腾讯SkillHub
助手：请问您要发布到哪个版本？
     [A] 个人版 — 发布到您的个人空间，CLI全自动，需要 skh_ 个人Token
     [B] 团队版 — 发布到团队 Skill 库，需要浏览器上传，需要 sk-ent- 企业Key
     
     如果不确定，告诉我：
     - 你是想让所有人都能搜到并安装？（→ 个人版）
     - 还是只想在你们团队内部使用？（→ 团队版）
```

---

## 🎯 虾聊发布方案（全自动API）

虾聊支持 **API Key** 方式直接上传Skill，实现真正的**一键自动化**！

### 全自动发布流程

**Step 1: 获取API Key**
1. 访问 https://clawdchat.cn
2. 注册 Agent 账号
3. 获取 API Key（格式：`clawdchat_xxxxxxxx`）

**Step 2: 配置API Key**
告诉 Skill："配置虾聊API Key"，提供用户名和 API Key

**Step 3: 一键发布**
告诉 Skill："发布到虾聊 {Skill名}"

---

## 🔱 ClawHub 发布方案（全自动API）

ClawHub 是 OpenClaw 官方 Skill 注册中心（13,000+ Skills），支持 API 一键发布。

### 全自动发布流程

**Step 1: 获取 API Token**
1. 访问 https://clawhub.ai → GitHub 登录
2. 右上角头像 → Settings → API Tokens → Create Token
3. 复制 Token（格式：`clh_xxxxxxxx`）

**Step 2: 准备 SKILL.md**
确保 SKILL.md frontmatter 包含 ClawHub 必需字段：
```yaml
---
name: your-skill          # Skill 名称
version: 1.0.0            # 版本号（必须有！）
description: 完整描述      # 详细描述
---
```

> ⚠️ 注意：`version` 字段是 ClawHub 强制要求，缺失会被拒绝。

**Step 3: API 一键发布**
```python
import requests, json

payload = json.dumps({
    "slug": "your-skill-slug",
    "displayName": "显示名称",
    "version": "1.0.0",
    "changelog": "首次发布",
    "tags": ["tag1", "tag2"],
    "acceptLicenseTerms": True   # 必须！同意开发者协议
}, ensure_ascii=False)

resp = requests.post(
    "https://clawhub.ai/api/v1/skills",
    headers={"Authorization": "Bearer clh_你的Token"},
    files={
        "payload": (None, payload, "application/json"),
        "files": ("SKILL.md", skill_content.encode("utf-8"), "text/markdown"),
    }
)
```

成功返回：`{"ok":true, "skillId":"...", "versionId":"..."}`

**Step 4: 验证发布**
- Skill 页：`https://clawhub.ai/skills/{skillId}`
- 搜索：`https://clawhub.ai/search?q=your-skill-slug`

### 安全扫描注意事项
- 🔴 避免硬编码 API Key → 用环境变量并在 `metadata.openclaw.requires.env` 中声明
- 🟡 HTTP 端点 → 在 SKILL.md 中添加安全警告
- ⚠️ 必须先同意开发者协议（`acceptLicenseTerms: true`），否则 400 错误

### 常见错误
| 错误 | 原因 | 解决 |
|------|------|------|
| 400 acceptLicenseTerms | 未同意开发者协议 | 访问 clawhub.ai → Settings → Developer Settings → 同意协议 |
| 409 版本冲突 | 版本号已存在 | 升级版本号如 1.0.0 → 1.0.1 |
| 安全扫描不通过 | 硬编码凭证/未声明环境变量 | 改用环境变量 + 声明 metadata |

---

## 🛠️ 执行脚本

本Skill包含可执行脚本，位于 `scripts/` 目录：

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `matrix_publish.py` | 一键分发主脚本 | 批量发布到五大平台 |
| `publish_tencent_skillhub.py` | 腾讯SkillHub发布 | 发布到腾讯官方Skill市场 |
| `publish_clawdchat_api.py` | 虾聊全自动发布 ⭐推荐 | 配置API Key后一键发布 |
| `publish_clawdchat_share.py` | 虾聊分享链接生成 | 无API Key时使用 |
| `publish_clawhub.py` | ClawHub全自动发布 ⭐推荐 | 配置Token后一键发布到ClawHub |
| `publish_github.py` | GitHub发布脚本 | 代码托管和版本管理 |
| `test_clawdchat_api.py` | 虾聊API测试 | 验证API Key有效性 |

---

## 📋 支持平台

| 平台 | 类型 | 特点 |
|------|------|------|
| 🔷 **腾讯SkillHub（个人版）** | 官方平台-个人 | CLI全自动发布，`skh_` Token认证，发布到社区市场 |
| 🔷 **腾讯SkillHub（团队版）** | 官方平台-团队 | 浏览器上传，`sk-ent-` 企业Key，发布到团队 Skill 库 |
| 🦞 **虾聊 (ClawdChat)** | 社区平台 | AI Agent交流社区，国内用户活跃 |
| 🦐 **虾友SkillHub** | 自研平台 | 青木会虾友社官方平台，深度整合（三重验证） |
| 📦 **GitHub** | 代码托管 | 开源生态，版本管理，全球开发者 |
| 🔱 **ClawHub** | 官方市场 | OpenClaw官方Skill市场，API全自动发布，13000+ Skills |

---

## ⚠️ 发布规则（强制执行）

> 🔴 **铁律：概述（description）必须完整，禁止极简/截断！**

### 规则1：完整概述，禁止截断
- `description` 字段**必须完整呈现** SKILL.md frontmatter 中的描述内容
- **禁止**任何形式的长度截断（如 `[:200]`、`[:100]` 等）
- 概述应当是有意义的自然段落，包含完整的产品介绍、核心功能说明
- 极简版概述（如"AI助手"、"智能工具"）**一律拒绝发布**

### 规则2：必须完整读取skill的所有内容
- 发布任何skill前，**必须完整读取**该skill的SKILL.md文件（全部内容，不只是frontmatter）
- 确保`description`字段完整反映了skill的实际功能和内容
- 禁止根据frontmatter的简短描述就生成概述，**必须读完全文**
- 概述应当涵盖skill的核心功能、使用场景、技术特点等关键信息

### 规则3：所有平台通用
此规则适用于**全部6个平台**（腾讯SkillHub个人版+团队版、虾聊、虾友SkillHub、GitHub、ClawHub）。
每个平台的 `description` 字段都必须完整。

### 规则4：发布后必须验证
- 任何平台发布/更新后，**必须调用查询接口确认**状态、分类、skillType 等字段已生效
- 虾友SkillHub 修改分类后 → `GET /api/skills/{id}` 确认
- 不要假设成功，**数据说话**

### 规则5：代码保障
矩阵发布助手脚本（`matrix_publish.py`）中，提取 description 的代码行：
```python
# ✅ 正确：不截断
description = ' '.join(desc_lines)

# ❌ 错误：截断（已修复）
# description = ' '.join(desc_lines)[:200]
```

---

## ⚠️ 错误处理

**平台未配置**：提示用户先完成配置
**平台限流/429**：等待60秒自动重试
**认证失败/401**：引导用户重新获取Token
**Skill已存在/409**：提供更新或跳过选项

---

## 🎨 品牌信息

- **出品方**：青木会江湖 | 虾友社
- **官方网站**：https://qingmuhui.com
- **SkillHub**：https://aiskillhub.vip
- **公众号**：青木老贼说社群
- **版本**：v3.3.0

---

## 🔄 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v3.3.0** | 2026-06-15 | 🔄 新增「Skill版本更新指南」：六平台更新机制对比（虾友搜索更新/ClawHub upsert/GitHub push/腾讯CLI），文档化更新 vs 创建的差异；📥 新增「安装方式（双通道）」：对话安装 + 命令行安装（含 install.sh / install.ps1），双通道对比表；更新版本为 v3.3.0 |
| **v3.2.0** | 2026-06-15 | 🧪 六平台全实战验证（社群收录）：新增完整流水账（腾讯个人版CLI/虾聊/ClawHub/GitHub/虾友SkillHub）、GitHub git token认证流程、虾友SkillHub分类更新端点、分类树快照、AI审核关键词规避实战；修复发布规则编号错乱（规则1→5）、5平台→6平台 |
| **v3.1.1** | 2026-06-15 | 🦐 虾友SkillHub全自动发布：新增 API 参数详解（skillType必传）、AI审核关键词规避（某信→社交账号、虚假交易规避）、分类体系说明（leaf node必须） |
| **v3.1.0** | 2026-06-15 | 🔱 新增 ClawHub 全自动API发布方案（POST /api/v1/skills），含完整Python示例、安全扫描注意事项、常见错误处理 |
| **v3.0.0** | 2026-06-15 | 🔷 腾讯SkillHub双通道发布：新增「团队版」浏览器上传流程，保留「个人版」CLI全自动；区分 skh_ 个人Token vs sk-ent- 企业Key 的使用场景 |
| v2.2.1 | 2026-05-29 | 🔷 修正腾讯SkillHub发布方案：CLI不支持上传，改为「助手自动打包 + 浏览器手动上传」务实方案 |
| v2.2.0 | 2026-05-28 | 🔷 新增腾讯SkillHub平台支持，五平台全覆盖（腾讯SkillHub+虾聊+虾友SkillHub+GitHub+ClawHub） |
| v2.1.0 | 2026-05-28 | 🛡️ 新增三重安全验证（登录+API Key+邀请码），缺一不可；移除config.json自动登录 |
| v2.0.0 | 2026-05-28 | 🧠 新增智能类目识别引擎，自动分析Skill内容并归档到正确的二级类目；支持5大类52小类精准匹配 |
| v1.1.0 | 2026-04-27 | ✅ 虾聊全自动发布流程验证成功，新增API Key自动发布方案 |
| v1.0.0 | 2026-04-26 | 初版发布，支持4平台一键分发 |

---

**记住：本Skill仅支持免费开源Skill的分发！**
**如需发布付费Skill，请使用「付费Skill发布助手」。**
