#!/usr/bin/env python3
"""
通用技术方案文档生成器
自动替换模板中的变量，生成具体的提示词
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any


class TemplateGenerator:
    """模板生成器"""
    
    def __init__(self, template_file: str = "通用技术方案生成模板.md"):
        self.template_file = template_file
        self.template_content = ""
        self.variables = {}
        
    def load_template(self) -> str:
        """加载模板文件"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
            print(f"✅ 成功加载模板文件: {self.template_file}")
            return self.template_content
        except FileNotFoundError:
            print(f"❌ 模板文件未找到: {self.template_file}")
            return ""
    
    def load_variables(self, config_file: str) -> Dict[str, Any]:
        """从YAML配置文件加载变量"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.variables = yaml.safe_load(f)
            print(f"✅ 成功加载变量配置: {config_file}")
            return self.variables
        except FileNotFoundError:
            print(f"❌ 配置文件未找到: {config_file}")
            return {}
    
    def extract_variables(self) -> set:
        """从模板中提取所有变量"""
        pattern = r'\$\{([^}]+)\}'
        variables = set(re.findall(pattern, self.template_content))
        print(f"📋 模板中发现 {len(variables)} 个变量:")
        for var in sorted(variables):
            print(f"   - ${{{var}}}")
        return variables
    
    def generate_config_template(self, output_file: str = "project_config.yaml"):
        """生成配置文件模板"""
        variables = self.extract_variables()
        
        # 按类别组织变量
        categories = {
            "基础信息": ["原始领域", "目标领域", "原始文档名", "目标文档名"],
            "公司信息": ["公司全称", "公司简称", "logo文件名", "文档日期"],
            "技术栈": ["原始技术栈", "目标技术栈", "原始核心技术", "目标核心技术"],
            "业务领域": ["原始业务领域", "目标业务领域", "目标对象数量", "目标对象类型"],
            "团队信息": ["项目周期", "阶段数量", "项目经理姓名", "技术总监姓名"],
            "技术指标": ["核心指标1", "指标1目标值", "核心指标2", "指标2目标值"],
            "样式配置": ["主字体名称", "无衬线字体名称", "等宽字体名称", "代码背景色"]
        }
        
        config_content = "# 项目配置文件\n# 请根据具体项目需求填写以下变量\n\n"
        
        for category, var_list in categories.items():
            config_content += f"# {category}\n"
            for var in var_list:
                if var in variables:
                    config_content += f'{var}: "请填写{var}"\n'
            config_content += "\n"
        
        # 添加其他未分类的变量
        uncategorized = variables - set(sum(categories.values(), []))
        if uncategorized:
            config_content += "# 其他变量\n"
            for var in sorted(uncategorized):
                config_content += f'{var}: "请填写{var}"\n'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"📝 已生成配置模板: {output_file}")
        return output_file
    
    def replace_variables(self, content: str = None) -> str:
        """替换模板中的变量"""
        if content is None:
            content = self.template_content
        
        if not self.variables:
            print("⚠️  警告: 未加载变量配置")
            return content
        
        # 统计替换情况
        replaced_count = 0
        missing_vars = []
        
        def replace_func(match):
            nonlocal replaced_count, missing_vars
            var_name = match.group(1)
            if var_name in self.variables:
                replaced_count += 1
                return str(self.variables[var_name])
            else:
                missing_vars.append(var_name)
                return match.group(0)  # 保持原样
        
        # 执行替换
        result = re.sub(r'\$\{([^}]+)\}', replace_func, content)
        
        print(f"🔄 变量替换完成:")
        print(f"   ✅ 成功替换: {replaced_count} 个变量")
        if missing_vars:
            print(f"   ⚠️  缺失变量: {len(set(missing_vars))} 个")
            for var in sorted(set(missing_vars)):
                print(f"      - ${{{var}}}")
        
        return result
    
    def generate_document(self, config_file: str, output_file: str = None) -> str:
        """生成最终文档"""
        if not self.template_content:
            self.load_template()
        
        self.load_variables(config_file)
        result = self.replace_variables()
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"📄 已生成文档: {output_file}")
        
        return result
    
    def interactive_config(self) -> Dict[str, Any]:
        """交互式配置变量"""
        variables = self.extract_variables()
        config = {}
        
        print("\n🎯 交互式配置模式")
        print("请为以下变量提供值（按回车跳过）:\n")
        
        for var in sorted(variables):
            value = input(f"${{{var}}}: ").strip()
            if value:
                config[var] = value
        
        self.variables = config
        return config
    
    def validate_config(self, config_file: str) -> bool:
        """验证配置文件完整性"""
        self.load_variables(config_file)
        template_vars = self.extract_variables()
        config_vars = set(self.variables.keys())
        
        missing = template_vars - config_vars
        extra = config_vars - template_vars
        
        print(f"\n📊 配置验证结果:")
        print(f"   模板变量总数: {len(template_vars)}")
        print(f"   配置变量总数: {len(config_vars)}")
        print(f"   匹配变量数量: {len(template_vars & config_vars)}")
        
        if missing:
            print(f"   ❌ 缺失变量 ({len(missing)}个):")
            for var in sorted(missing):
                print(f"      - ${{{var}}}")
        
        if extra:
            print(f"   ⚠️  多余变量 ({len(extra)}个):")
            for var in sorted(extra):
                print(f"      - {var}")
        
        return len(missing) == 0


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="通用技术方案文档生成器")
    parser.add_argument("--template", "-t", default="通用技术方案生成模板.md", 
                       help="模板文件路径")
    parser.add_argument("--config", "-c", help="配置文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--generate-config", action="store_true", 
                       help="生成配置文件模板")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="交互式配置模式")
    parser.add_argument("--validate", "-v", help="验证配置文件")
    
    args = parser.parse_args()
    
    generator = TemplateGenerator(args.template)
    generator.load_template()
    
    if args.generate_config:
        generator.generate_config_template()
        return
    
    if args.validate:
        generator.validate_config(args.validate)
        return
    
    if args.interactive:
        generator.interactive_config()
        result = generator.replace_variables()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"📄 已生成文档: {args.output}")
        else:
            print("\n" + "="*50)
            print("生成的文档内容:")
            print("="*50)
            print(result)
        return
    
    if args.config:
        generator.generate_document(args.config, args.output)
    else:
        print("请指定配置文件 (--config) 或使用交互模式 (--interactive)")


if __name__ == "__main__":
    main() 