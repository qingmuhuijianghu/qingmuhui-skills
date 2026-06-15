# ═══════════════════════════════════════════════════════════
#  Skill矩阵分发助手 — Windows PowerShell 安装脚本
#  版本: v3.3.0
#  用途: 一键安装到 WorkBuddy skills 目录，支持 CLI 使用
# ═══════════════════════════════════════════════════════════

$SKILL_NAME = "skill-matrix-publisher-free"
$REPO_URL = "https://github.com/qingmuhuijianghu/qingmuhui-skills.git"
$WORKBUDDY_SKILLS_DIR = "$env:USERPROFILE\.workbuddy\skills"
$TARGET_DIR = "$WORKBUDDY_SKILLS_DIR\$SKILL_NAME"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚀 Skill矩阵分发助手 安装程序 v3.3.0         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 检测 Python
Write-Host "[1/4] 检测 Python 环境..." -ForegroundColor Yellow
$PYTHON = $null
foreach ($py in @("python3", "python")) {
    try {
        $ver = & $py --version 2>&1
        $PYTHON = (Get-Command $py -ErrorAction SilentlyContinue).Source
        Write-Host "  ✅ Python: $ver" -ForegroundColor Green
        break
    } catch {}
}
if (-not $PYTHON) {
    Write-Host "  ❌ 未找到 Python，请先安装 Python 3.7+" -ForegroundColor Red
    Write-Host "  💡 下载: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 创建目录
Write-Host "[2/4] 创建 WorkBuddy skills 目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $WORKBUDDY_SKILLS_DIR | Out-Null

# 下载
Write-Host "[3/4] 下载技能文件..." -ForegroundColor Yellow

if (Test-Path $TARGET_DIR) {
    Write-Host "  ⚠️  目录已存在，正在更新..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $TARGET_DIR
}

# 使用 ZIP 下载（GitHub 原生支持）
$ZIP_URL = "https://github.com/qingmuhuijianghu/qingmuhui-skills/archive/refs/heads/main.zip"
$TEMP_ZIP = "$env:TEMP\skill-matrix-publisher-free.zip"
$TEMP_DIR = "$env:TEMP\skill-matrix-publisher-free-extract"

try {
    Write-Host "  正在下载..." -ForegroundColor Gray
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $ZIP_URL -OutFile $TEMP_ZIP -UseBasicParsing

    Write-Host "  正在解压..." -ForegroundColor Gray
    Expand-Archive -Path $TEMP_ZIP -DestinationPath $TEMP_DIR -Force

    # 复制技能目录
    $EXTRACTED = Get-ChildItem -Path $TEMP_DIR -Directory | Select-Object -First 1
    $SKILL_SOURCE = "$($EXTRACTED.FullName)\$SKILL_NAME"

    if (Test-Path $SKILL_SOURCE) {
        Copy-Item -Recurse -Path $SKILL_SOURCE -Destination $TARGET_DIR
        Write-Host "  ✅ 下载完成" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 仓库中未找到 $SKILL_NAME 目录" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "  ❌ 下载失败: $_" -ForegroundColor Red
    Write-Host "  💡 手动安装: git clone $REPO_URL" -ForegroundColor Yellow
    exit 1
} finally {
    Remove-Item -Force $TEMP_ZIP -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force $TEMP_DIR -ErrorAction SilentlyContinue
}

# 安装依赖
Write-Host "[4/4] 安装 Python 依赖..." -ForegroundColor Yellow
try {
    & $PYTHON -m pip install requests --quiet 2>&1 | Out-Null
    Write-Host "  ✅ 依赖安装完成" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  pip install 失败，请手动运行: pip install requests" -ForegroundColor Yellow
}

# 完成
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ 安装完成！                                  ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📂 安装位置: " -NoNewline -ForegroundColor Cyan
Write-Host $TARGET_DIR
Write-Host ""

Write-Host "🚀 CLI 使用方法:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  # 一键分发到所有平台" -ForegroundColor Gray
Write-Host "  $PYTHON `"$TARGET_DIR\scripts\matrix_publish.py`" C:\path\to\your-skill all" -ForegroundColor Green
Write-Host ""
Write-Host "  # 只发布到虾友SkillHub" -ForegroundColor Gray
Write-Host "  $PYTHON `"$TARGET_DIR\scripts\matrix_publish.py`" C:\path\to\your-skill skillhub ``" -ForegroundColor Green
Write-Host "    --phone 138xxxx --password xxx --api-key sk-xxx --invitation-code XXXX" -ForegroundColor Green
Write-Host ""
Write-Host "  # 只发布到ClawHub" -ForegroundColor Gray
Write-Host "  $PYTHON `"$TARGET_DIR\scripts\matrix_publish.py`" C:\path\to\your-skill clawhub" -ForegroundColor Green
Write-Host ""

Write-Host "🗣️  对话使用:" -ForegroundColor Cyan
Write-Host "  在 WorkBuddy 中直接说「帮我把XX Skill发布到虾友SkillHub」" -ForegroundColor White
Write-Host ""
