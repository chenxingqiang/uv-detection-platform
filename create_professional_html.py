#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime

def markdown_to_html(md_content):
    """简单的markdown到HTML转换"""
    html = md_content
    
    # 转换标题
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # 转换粗体
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # 转换列表项
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 转换段落
    lines = html.split('\n')
    result = []
    in_list = False
    in_table = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                result.append('</ul>')
                in_list = False
            elif in_table:
                result.append('</table>')
                in_table = False
            result.append('')
            continue
            
        if line.startswith('<li>'):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(line)
        elif line.startswith('|') and '|' in line[1:]:
            if not in_table:
                result.append('<table>')
                in_table = True
            # 简单表格处理
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if '---' in line:
                continue  # 跳过分隔行
            if len(cells) > 0:
                if in_table and result[-1] == '<table>':
                    # 表头
                    result.append('<thead><tr>')
                    for cell in cells:
                        result.append(f'<th>{cell}</th>')
                    result.append('</tr></thead><tbody>')
                else:
                    # 表格行
                    result.append('<tr>')
                    for cell in cells:
                        result.append(f'<td>{cell}</td>')
                    result.append('</tr>')
        elif line.startswith('<h'):
            if in_list:
                result.append('</ul>')
                in_list = False
            elif in_table:
                result.append('</tbody></table>')
                in_table = False
            result.append(line)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            elif in_table:
                result.append('</tbody></table>')
                in_table = False
            if line and not line.startswith('<'):
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)
    
    if in_list:
        result.append('</ul>')
    elif in_table:
        result.append('</tbody></table>')
    
    return '\n'.join(result)

def create_professional_html():
    """创建专业的HTML文件"""
    
    # 读取markdown文件
    try:
        with open('plan.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print("❌ 未找到plan.md文件")
        return False
    
    # 转换为HTML
    html_content = markdown_to_html(md_content)
    
    # 创建专业的HTML模板
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>非法添加药物紫外光谱云端筛查识别系统技术方案</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm 2cm 2cm 2cm;
            @top-center {{
                content: "图灵智能科技 | 技术方案";
                font-family: 'Microsoft YaHei', sans-serif;
                font-size: 10pt;
                color: #666;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }}
            @bottom-center {{
                content: "第 " counter(page) " 页";
                font-family: 'Microsoft YaHei', sans-serif;
                font-size: 9pt;
                color: #999;
            }}
        }}
        
        @media print {{
            .cover-page {{
                page-break-after: always;
            }}
            .page-break {{
                page-break-before: always;
            }}
            .no-break {{
                page-break-inside: avoid;
            }}
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', serif;
            line-height: 1.6;
            color: #333;
            font-size: 12pt;
            margin: 0;
            padding: 20px;
            background-color: #fff;
        }}
        
        .cover-page {{
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: -20px;
            padding: 40px;
            box-sizing: border-box;
        }}
        
        .logo-container {{
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .logo-text {{
            font-size: 36pt;
            font-weight: bold;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin: 0;
            letter-spacing: 2px;
        }}
        
        .logo-subtitle {{
            font-size: 14pt;
            margin: 10px 0 0 0;
            text-indent: 0;
            opacity: 0.9;
            letter-spacing: 1px;
        }}
        
        .title {{
            font-size: 32pt;
            font-weight: bold;
            margin: 40px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            line-height: 1.2;
        }}
        
        .subtitle {{
            font-size: 20pt;
            margin: 20px 0 40px 0;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .project-info {{
            margin: 40px 0;
            padding: 25px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .project-info p {{
            font-size: 16pt;
            margin: 12px 0;
            text-indent: 0;
        }}
        
        .company-info {{
            margin-top: 60px;
            font-size: 14pt;
            opacity: 0.8;
        }}
        
        .company-info p {{
            text-indent: 0;
            margin: 8px 0;
        }}
        
        .content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px 0;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 20pt;
            font-weight: bold;
            margin: 30px 0 20px 0;
            padding: 15px 0 10px 0;
            border-bottom: 3px solid #3498db;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #34495e;
            font-size: 18pt;
            font-weight: bold;
            margin: 25px 0 15px 0;
            padding: 10px 0 10px 20px;
            border-left: 5px solid #3498db;
            background: linear-gradient(90deg, #f8f9fa 0%, transparent 100%);
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #2c3e50;
            font-size: 16pt;
            font-weight: bold;
            margin: 20px 0 12px 0;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #34495e;
            font-size: 14pt;
            font-weight: bold;
            margin: 15px 0 10px 0;
            page-break-after: avoid;
        }}
        
        p {{
            margin: 10px 0;
            text-align: justify;
            text-indent: 2em;
            line-height: 1.8;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
            text-align: justify;
            line-height: 1.6;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 11pt;
            page-break-inside: avoid;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px 10px;
            text-align: left;
            vertical-align: top;
        }}
        
        th {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: bold;
            text-align: center;
            font-size: 11pt;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tbody tr:hover {{
            background-color: #e3f2fd;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 10pt;
            color: #e74c3c;
        }}
        
        pre {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #3498db;
            overflow-x: auto;
            font-size: 10pt;
            page-break-inside: avoid;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 15px 0;
        }}
        
        .highlight {{
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            padding: 15px;
            border-left: 5px solid #ffc107;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: bold;
        }}
        
        blockquote {{
            border-left: 5px solid #3498db;
            margin: 20px 0;
            padding: 15px 25px;
            background-color: #f8f9fa;
            font-style: italic;
            border-radius: 0 8px 8px 0;
        }}
        
        .section-divider {{
            height: 2px;
            background: linear-gradient(90deg, #3498db, transparent);
            margin: 40px 0;
            border: none;
        }}
        
        .key-point {{
            background: linear-gradient(135deg, #e8f5e8, #d4edda);
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 5px solid #28a745;
        }}
        
        .warning {{
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 5px solid #ffc107;
        }}
        
        .risk {{
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 5px solid #dc3545;
        }}
        
        .toc {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .toc h2 {{
            margin-top: 0;
            text-align: center;
            color: #2c3e50;
        }}
    </style>
</head>
<body>
    <div class="cover-page">
        <div class="logo-container">
            <h1 class="logo-text">图灵智能</h1>
            <p class="logo-subtitle">TURING INTELLIGENCE</p>
        </div>
        <h1 class="title">非法添加药物紫外光谱云端<br>筛查识别系统</h1>
        <h2 class="subtitle">技术方案</h2>
        <div class="project-info">
            <p><strong>项目负责人：</strong>张明均</p>
            <p><strong>项目完成人员：</strong>陈锡龙等</p>
            <p><strong>项目周期：</strong>36个月</p>
            <p><strong>总投资：</strong>1800万元</p>
        </div>
        <div class="company-info">
            <p><strong>图灵智能科技有限公司</strong></p>
            <p>{datetime.now().strftime('%Y年%m月')}</p>
        </div>
    </div>
    
    <div class="page-break"></div>
    
    <div class="content">
        {html_content}
    </div>
</body>
</html>'''
    
    # 保存HTML文件
    with open('plan_professional.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("✅ 专业HTML文件已生成：plan_professional.html")
    print("📄 您可以:")
    print("   1. 在浏览器中打开此文件查看效果")
    print("   2. 使用浏览器的'打印'功能保存为PDF")
    print("   3. 选择'另存为PDF'即可获得专业格式的PDF文件")
    
    return True

if __name__ == "__main__":
    create_professional_html() 