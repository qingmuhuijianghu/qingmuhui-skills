#!/usr/bin/env python3
"""
export_slices.py - 将滋补品详情页 HTML 导出为 3000x4000 JPG 切片
用法：
  python3 export_slices.py --html /path/to/page.html --output ~/Desktop/产品名第一版详情页/
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("错误：需要 Pillow 库。请运行：pip3 install Pillow")
    sys.exit(1)


def run_agent_browser(args: list) -> str:
    """运行 agent-browser 命令，返回 stdout"""
    cmd = ["agent-browser"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"agent-browser 错误：{result.stderr}")
        return ""
    return result.stdout.strip()


def get_sections(html_path: str) -> list:
    """
    打开 HTML，获取所有 section 的位置信息。
    返回 [{"i": idx, "top": int, "bottom": int, "h2": str}, ...]
    """
    # 打开页面
    out = run_agent_browser(["open", f"file://{html_path}"])
    if not out.startswith("✓"):
        print(f"打开页面失败：{out}")
        return []

    # 等待加载
    time.sleep(2)

    # 获取所有 section 位置
    js = """
    JSON.stringify(Array.from(document.querySelectorAll('section')).map((s,i) => ({
        i,
        top: Math.round(s.getBoundingClientRect().top + window.scrollY),
        bottom: Math.round(s.getBoundingClientRect().bottom + window.scrollY),
        h2: s.querySelector('.h2')?.textContent?.trim().substring(0,20)||''
    })))
    """
    out = run_agent_browser(["eval", js])
    try:
        sections = json.loads(out)
        return sections
    except json.JSONDecodeError:
        print(f"解析 section 位置失败：{out}")
        return []


def take_full_screenshot(output_path: str) -> str:
    """截取整页截图，返回保存路径"""
    out = run_agent_browser(["screenshot", "--full", output_path])
    if "✓ Screenshot saved to" in out:
        # 提取实际路径
        path = out.split("✓ Screenshot saved to ")[-1].strip()
        return path
    print(f"截图失败：{out}")
    return ""


def crop_and_resize(
    full_img_path: str,
    top_px: int,
    bottom_px: int,
    output_path: str,
    target_w: int = 3000,
    target_h: int = 4000,
    bg_color: tuple = (44, 36, 22),  # #2C2416
) -> bool:
    """裁剪指定区域，缩放并居中放置在 target_w x target_h 画布上，保存为 JPG"""
    try:
        img = Image.open(full_img_path)
        pw = img.width
        crop_h = bottom_px - top_px
        if crop_h <= 0:
            print(f"  裁剪高度异常：{crop_h}px，跳过")
            return False

        # 裁剪
        section = img.crop((0, top_px, pw, bottom_px))

        # 计算缩放（保持宽高比，适应目标画布）
        content_ratio = pw / crop_h
        target_ratio = target_w / target_h

        if content_ratio > target_ratio:
            new_w = target_w
            new_h = int(target_w / content_ratio)
        else:
            new_h = target_h
            new_w = int(target_h * content_ratio)

        resized = section.resize((new_w, new_h), Image.LANCZOS)

        # 创建画布并居中粘贴
        canvas = Image.new("RGB", (target_w, target_h), bg_color)
        x = (target_w - new_w) // 2
        y = (target_h - new_h) // 2
        canvas.paste(resized, (x, y))

        # 保存
        canvas.save(output_path, "JPEG", quality=95)
        print(f"  ✓ 保存：{output_path}（内容区 {new_w}x{new_h}）")
        return True

    except Exception as e:
        print(f"  处理失败：{e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="将滋补品详情页 HTML 导出为 3000x4000 JPG 切片")
    parser.add_argument("--html", required=True, help="HTML 文件路径")
    parser.add_argument("--output", required=True, help="输出目录")
    parser.add_argument("--target-w", type=int, default=3000, help="目标宽度（默认 3000）")
    parser.add_argument("--target-h", type=int, default=4000, help="目标高度（默认 4000）")
    args = parser.parse_args()

    html_path = os.path.abspath(args.html)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(html_path):
        print(f"错误：HTML 文件不存在：{html_path}")
        sys.exit(1)

    print(f"📂 输入：{html_path}")
    print(f"📁 输出：{output_dir}")
    print()

    # 获取 section 位置
    print("🔍 正在获取板块位置...")
    sections = get_sections(html_path)
    if not sections:
        print("❌ 无法获取板块位置，退出")
        run_agent_browser(["close"])
        sys.exit(1)

    print(f"   找到 {len(sections)} 个板块：")
    for s in sections:
        print(f"   [{s['i']}] top={s['top']} bottom={s['bottom']} h2={s['h2']}")
    print()

    # 截取整页
    tmp_png = str(output_dir / "_full_page.png")
    print("📸 正在截取整页截图（可能需要 10-30 秒）...")
    screenshot_path = take_full_screenshot(tmp_png)
    if not screenshot_path or not os.path.exists(screenshot_path):
        # 尝试用返回的路径，如果不存在则用 tmp_png
        if os.path.exists(tmp_png):
            screenshot_path = tmp_png
        else:
            print("❌ 截图失败，退出")
            run_agent_browser(["close"])
            sys.exit(1)

    print(f"   ✓ 截图已保存：{screenshot_path}")
    print()

    # 裁剪并导出每个板块
    print("✂️ 正在裁剪并导出切片...")
    for i, s in enumerate(sections):
        top = max(0, s["top"] - 10)  # 加一点 buffer
        bottom = s["bottom"] + 10

        # 生成文件名
        h2_short = s["h2"].replace("/", "-").replace("\\", "-")[:10] or f"板块{i+1}"
        filename = f"{i+1:02d}_{h2_short}_{args.target_w}x{args.target_h}.jpg"
        out_path = str(output_dir / filename)

        ok = crop_and_resize(screenshot_path, top, bottom, out_path, args.target_w, args.target_h)
        if not ok:
            print(f"   ⚠️ 板块 {i+1} 导出失败，跳过")

    print()

    # 清理
    run_agent_browser(["close"])
    if os.path.exists(tmp_png):
        os.remove(tmp_png)

    print("✅ 全部完成！")
    print(f"   输出目录：{output_dir}")


if __name__ == "__main__":
    main()
