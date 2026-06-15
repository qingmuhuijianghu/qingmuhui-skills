#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Skill矩阵分发助手 — Linux/macOS 安装脚本
#  版本: v3.3.0
#  用途: 一键安装到 WorkBuddy skills 目录，支持 CLI 使用
# ═══════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

SKILL_NAME="skill-matrix-publisher-free"
REPO_URL="https://github.com/qingmuhuijianghu/qingmuhui-skills.git"
WORKBUDDY_SKILLS_DIR="${HOME}/.workbuddy/skills"
TARGET_DIR="${WORKBUDDY_SKILLS_DIR}/${SKILL_NAME}"

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════╗"
echo "║   🚀 Skill矩阵分发助手 安装程序 v3.3.0         ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检测 Python
echo -e "${YELLOW}[1/4]${NC} 检测 Python 环境..."
PYTHON=""
for py in python3 python; do
    if command -v $py &> /dev/null; then
        PYTHON=$(command -v $py)
        echo -e "${GREEN}  ✅ Python: $($PYTHON --version 2>&1)${NC}"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    echo -e "${RED}  ❌ 未找到 Python，请先安装 Python 3.7+${NC}"
    exit 1
fi

# 创建目录
echo -e "${YELLOW}[2/4]${NC} 创建 WorkBuddy skills 目录..."
mkdir -p "${WORKBUDDY_SKILLS_DIR}"

# 下载技能文件
echo -e "${YELLOW}[3/4]${NC} 下载技能文件..."

if [ -d "${TARGET_DIR}" ]; then
    echo -e "${YELLOW}  ⚠️  目录已存在，正在更新...${NC}"
    cd "${TARGET_DIR}"
    git pull origin main 2>/dev/null || {
        echo -e "${YELLOW}  ⚠️  git pull 失败，将重新克隆...${NC}"
        cd "${WORKBUDDY_SKILLS_DIR}"
        rm -rf "${SKILL_NAME}"
    }
fi

if [ ! -d "${TARGET_DIR}" ]; then
    # 使用 sparse-checkout 只下载需要的目录
    TEMP_DIR=$(mktemp -d)
    cd "${TEMP_DIR}"
    git clone --depth 1 --filter=blob:none --sparse "${REPO_URL}" . 2>/dev/null || {
        echo -e "${RED}  ❌ Git clone 失败，请检查网络连接${NC}"
        echo -e "${YELLOW}  💡 手动安装: git clone ${REPO_URL}${NC}"
        rm -rf "${TEMP_DIR}"
        exit 1
    }
    git sparse-checkout set "${SKILL_NAME}"
    
    # 复制到 WorkBuddy skills 目录
    cp -r "${SKILL_NAME}" "${TARGET_DIR}"
    rm -rf "${TEMP_DIR}"
fi

# 安装依赖
echo -e "${YELLOW}[4/4]${NC} 安装 Python 依赖..."
$PYTHON -m pip install requests --quiet 2>/dev/null || {
    echo -e "${YELLOW}  ⚠️  pip install 失败，请手动运行: pip install requests${NC}"
}

# 完成
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ 安装完成！                                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📂 安装位置:${NC} ${TARGET_DIR}"
echo ""
echo -e "${CYAN}🚀 CLI 使用方法:${NC}"
echo -e "  ${GREEN}# 一键分发到所有平台${NC}"
echo -e "  ${PYTHON} ${TARGET_DIR}/scripts/matrix_publish.py /path/to/your-skill all"
echo ""
echo -e "  ${GREEN}# 只发布到虾友SkillHub${NC}"
echo -e "  ${PYTHON} ${TARGET_DIR}/scripts/matrix_publish.py /path/to/your-skill skillhub \\"
echo "    --phone 138xxxx --password xxx --api-key sk-xxx --invitation-code XXXX"
echo ""
echo -e "  ${GREEN}# 只发布到ClawHub${NC}"
echo -e "  ${PYTHON} ${TARGET_DIR}/scripts/matrix_publish.py /path/to/your-skill clawhub"
echo ""
echo -e "${CYAN}🗣️  对话使用:${NC}"
echo -e "  在 WorkBuddy 中直接说「帮我把XX Skill发布到虾友SkillHub」"
echo ""
