# 技能规范

## 目录结构

```
skill-name/
├── SKILL.md          # 必需 - 技能文档
├── README.md         # 必需 - 使用指南
├── main.py           # 必需 - 入口文件
├── requirements.txt  # 必需 - 依赖
├── .env.example      # 可选 - 环境变量示例
├── src/              # 可选 - 源代码
└── tests/            # 可选 - 测试
```

## SKILL.md 规范

必须包含：
- 技能名称和描述
- 安装说明
- 使用示例
- 作者信息

## 命名规范

- 目录名：小写，连字符分隔 `my-skill`
- 类名：大驼峰 `MySkill`
