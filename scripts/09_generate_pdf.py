#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to PDF Converter for Design Report
将设计思路文档模板转为PDF提交文件
"""

import subprocess
import os
import sys
from datetime import datetime


def check_dependencies():
    """检查必要的依赖"""
    tools = {
        'pandoc': 'pandoc --version',
        'xelatex': 'xelatex --version',
    }

    missing = []
    for tool, cmd in tools.items():
        try:
            subprocess.run(cmd.split(), capture_output=True, check=True)
            print(f"✓ {tool} installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(tool)
            print(f"✗ {tool} NOT installed")

    if missing:
        print(f"\nPlease install missing tools:")
        print(f"  pandoc: https://pandoc.org/installing.html")
        print(f"  xelatex: sudo apt-get install texlive-xetex (Ubuntu)")
        return False
    return True


def generate_pdf(input_md: str = "docs/design_report_template.md",
                 output_pdf: str = "docs/design_report.pdf",
                 team_name: str = "YourTeamName"):
    """生成PDF"""

    if not os.path.exists(input_md):
        print(f"Error: {input_md} not found")
        return False

    # 读取模板并替换占位符
    with open(input_md, 'r') as f:
        content = f.read()

    # 替换占位符
    content = content.replace('YourTeamName', team_name)
    content = content.replace('2026-05-XX', datetime.now().strftime('%Y-%m-%d'))

    # 写入临时文件
    temp_md = "docs/design_report_temp.md"
    with open(temp_md, 'w') as f:
        f.write(content)

    # Pandoc命令
    cmd = [
        "pandoc",
        temp_md,
        "-o", output_pdf,
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=2.5cm",
        "-V", "mainfont=DejaVu Serif",
        "-V", "monofont=DejaVu Sans Mono",
        "--toc",
        "--toc-depth=2",
        "--highlight-style=tango",
        "-f", "markdown",
        "-t", "pdf",
    ]

    print(f"\nGenerating PDF: {output_pdf}")
    print(f"Command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ PDF generated: {output_pdf}")

        # 清理临时文件
        os.remove(temp_md)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PDF generation failed: {e}")
        return False


def generate_with_python(input_md: str = "docs/design_report_template.md",
                         output_pdf: str = "docs/design_report.pdf"):
    """
    纯Python方案（无需pandoc/xelatex）
    使用markdown + pdfkit/weasyprint
    效果较差但无需额外安装
    """
    try:
        import markdown
        from weasyprint import HTML, CSS

        with open(input_md, 'r') as f:
            md_content = f.read()

        # Markdown转HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

        # 添加样式
        html_full = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 2cm; line-height: 1.6; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                h3 {{ color: #7f8c8d; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                blockquote {{ border-left: 4px solid #3498db; margin: 0; padding-left: 20px; color: #555; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        HTML(string=html_full).write_pdf(output_pdf)
        print(f"✅ PDF generated (Python method): {output_pdf}")
        return True

    except ImportError:
        print("❌ weasyprint not installed. Try: pip install weasyprint markdown")
        print("   Or use pandoc method (recommended)")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate design report PDF')
    parser.add_argument('--input', default='docs/design_report_template.md', help='Input markdown')
    parser.add_argument('--output', default='docs/design_report.pdf', help='Output PDF')
    parser.add_argument('--team', default='YourTeamName', help='Team name')
    parser.add_argument('--method', choices=['pandoc', 'python'], default='pandoc', help='Conversion method')
    args = parser.parse_args()

    print("=" * 60)
    print("Design Report PDF Generator")
    print("=" * 60)

    if args.method == 'pandoc':
        if check_dependencies():
            generate_pdf(args.input, args.output, args.team)
        else:
            print("\nFalling back to Python method...")
            generate_with_python(args.input, args.output)
    else:
        generate_with_python(args.input, args.output)


if __name__ == "__main__":
    main()
