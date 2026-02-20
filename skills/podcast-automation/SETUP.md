# 🚀 播客自动化设置指南

## 目录

1. [准备工作](#准备工作)
2. [Notion 配置](#notion-配置)
3. [阿里云 DashScope](#阿里云-dashscope)
4. [声音样本录制](#声音样本录制)
5. [本地测试](#本地测试)
6. [GitHub 自动化](#github-自动化)

---

## 准备工作

### 克隆项目

```bash
git clone https://github.com/你的用户名/awesome-claude-skills.git
cd awesome-claude-skills/skills/podcast-automation
```

### 安装依赖

```bash
pip install -r requirements.txt
```

---

## Notion 配置

### 步骤 1: 创建集成

1. 访问 [Notion Integrations](https://www.notion.so/my-integrations)
2. 点击 "New integration"
3. 填写名称：「播客自动化」
4. 选择工作区
5. 复制 **Internal Integration Token** (格式: `secret_xxx`)

### 步骤 2: 创建数据库

在 Notion 中创建数据库，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| **Title** | Title | 播客标题 |
| **Content** | Rich Text | 播客正文 |
| **Date** | Date | 发布日期 |
| **Status** | Select | 待发布 / 已发布 / 草稿 |

### 步骤 3: 分享数据库

1. 打开数据库页面
2. 点击右上角 "..." → "Add connections"
3. 选择「播客自动化」集成

### 步骤 4: 获取 Database ID

从 URL 复制：
```
https://www.notion.so/workspace/DATABASE_ID?v=...
```

`DATABASE_ID` 是 32 位的字符串。

---

## 阿里云 DashScope

### 注册与开通

1. 注册 [阿里云](https://www.aliyun.com) 账号
2. 访问 [DashScope](https://dashscope.aliyun.com) 开通服务
3. 创建 [API Key](https://dashscope.aliyun.com/api-key)

### 费用

- 价格：¥0.8 / 百万字符
- 10 分钟播客约 2000 字符
- **实际成本：约 ¥0.002/期（几乎免费）**

---

## 声音样本录制

### 要求

- 时长：3-10 秒
- 格式：WAV 或 MP3
- 内容：清晰的普通话

### 录制步骤

1. 打开 Mac「语音备忘录」
2. 录制示例：
   > "大家好，欢迎来到我的播客。"
3. 文件 → 导出 → 选择 WAV
4. 重命名为 `voice-sample.wav`
5. 放到项目根目录

---

## 本地测试

### 1. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`：
```env
NOTION_TOKEN=secret_xxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DASHSCOPE_API_KEY=sk-xxx
```

### 2. 在 Notion 添加测试内容

1. 创建新条目
2. Title: "测试播客"
3. Content: "这是测试内容"
4. Date: 今天
5. Status: 「待发布」

### 3. 运行

```bash
./run.sh
```

### 预期输出

```
==================================================
🚀 播客自动生成器 - 2024-01-20
==================================================

🔍 检查配置...
✅ 配置检查通过

📝 从 Notion 获取内容...
✅ 获取内容: 测试播客

🎙️ 使用 DashScope API 生成音频...
✅ 音频生成: public/audio/podcast-2024-01-20.mp3

📄 创建播客文件...
✅ 播客文件: content/episodes/2024-01-20.json

🔄 更新 Notion 状态...
✅ Notion 状态已更新为「已发布」

==================================================
✅ 播客生成完成！
==================================================
```

---

## GitHub 自动化

### 步骤 1: 推送代码

```bash
git add .
git commit -m "Add podcast automation skill"
git push
```

### 步骤 2: 设置 Secrets

1. 打开 GitHub 仓库 → Settings → Secrets → Actions
2. 添加以下 secrets：
   - `NOTION_TOKEN`
   - `NOTION_DATABASE_ID`
   - `DASHSCOPE_API_KEY`

### 步骤 3: 启用 GitHub Pages

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / (root)
4. 保存

### 完成！

每天北京时间 8:00 会自动检查并发布播客。

也可以手动触发：Actions → Daily Podcast → Run workflow

---

## 故障排查

### 问题：获取不到 Notion 内容

- 检查 Database ID 是否正确
- 确认数据库已分享给集成
- 检查日期是否为今天
- 检查状态是否为「待发布」

### 问题：音频生成失败

- 检查 DashScope API Key
- 确认账户有余额
- 查看 GitHub Actions 日志

### 问题：Lexar 本地模型不工作

- 确认 Lexar 已连接
- 检查路径：`/Volumes/Lexar/AI-Models/Qwen3-TTS/`
- 会自动 fallback 到 DashScope API

---

## 下一步

- [ ] 完成上述配置
- [ ] 测试一期播客
- [ ] 设置自定义域名（可选）
- [ ] 分享给朋友！
