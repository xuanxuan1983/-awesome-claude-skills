# 🎙️ Podcast Automation

全自动播客工作流：Notion → AI 声音克隆 → 网站发布

## 功能

- 📝 **自动获取内容** - 从 Notion 数据库读取
- 🎙️ **声音克隆** - 使用 Qwen3-TTS 克隆你的声音
- 🚀 **自动发布** - 推送到网站并更新 Notion 状态
- ⏰ **定时任务** - GitHub Actions 每天自动运行

## 快速开始

### 1. 配置

```bash
cp .env.example .env
# 编辑 .env 填入你的配置
```

### 2. 录制声音样本

- 用「语音备忘录」录 3-5 秒
- 导出为 `voice-sample.wav`
- 放在项目根目录

### 3. 运行

```bash
./run.sh
```

## 详细文档

- [完整设置指南](./SETUP.md) - 从零开始的详细教程
- [使用说明](./USAGE.md) - 日常使用指南

## 工作流程

```
Notion (待发布) → 生成音频 → 更新网站 → Notion (已发布)
```

## 技术栈

- **内容源**: Notion API
- **TTS**: DashScope Qwen3-TTS / 本地 Qwen3-TTS
- **托管**: GitHub Pages / Vercel
- **自动化**: GitHub Actions

## License

MIT
