#!/usr/bin/env python3
"""
测试 Skill 的脚本
调用 Codex MCP 来使用生成的 Skill 执行测试任务
"""

import json
import os
import sys
from pathlib import Path

def test_skill(skill_dir, task_file, output_dir):
    """测试指定的 Skill"""
    skill_path = Path(skill_dir)
    task_path = Path(task_file)
    output_path = Path(output_dir)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 读取任务文件
    with open(task_path, 'r', encoding='utf-8') as f:
        task_content = f.read()
    
    # 读取 Skill 信息
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"错误: {skill_md} 不存在")
        return False
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    # 生成测试提示词
    prompt = f"""请使用以下 Skill 来完成 RPG 游戏配置任务：

Skill 位置: {skill_dir}

任务需求:
{task_content[:2000]}...

请生成完整的 Luban 配置表系统，包括：
1. 枚举定义 (__enums__.xlsx)
2. Bean 定义 (__beans__.xlsx)  
3. 表定义 (__tables__.xlsx)
4. 所有数据表

输出目录: {output_dir}

请开始执行。"""
    
    # 保存提示词到文件，供后续使用
    prompt_file = output_path / "test_prompt.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"已生成测试提示词: {prompt_file}")
    print(f"请手动使用 Codex MCP 调用 Skill 执行任务")
    print(f"Skill 目录: {skill_dir}")
    print(f"输出目录: {output_dir}")
    
    return True

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    
    # 测试三个 Skill
    skills = [
        ("skill_v1_001", "luban-excel-editor"),
        ("skill_v1_002", "luban-excel-editor-v2"),
        ("skill_v1_003", "luban-rpg-config-editor"),
    ]
    
    task_file = base_dir / "test_tasks" / "rpg_game_config.md"
    
    for skill_id, skill_name in skills:
        skill_dir = base_dir / "skills" / skill_id
        output_dir = base_dir / "results" / skill_id
        
        print(f"\n{'='*60}")
        print(f"测试 Skill: {skill_name} ({skill_id})")
        print(f"{'='*60}")
        
        if skill_dir.exists():
            test_skill(skill_dir, task_file, output_dir)
        else:
            print(f"警告: Skill 目录不存在: {skill_dir}")

