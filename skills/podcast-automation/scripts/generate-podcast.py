#!/usr/bin/env python3
"""
每日播客自动生成器
从 Notion 获取内容 → 克隆声音 → 生成播客 → 推送网站
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

def log(msg: str, emoji: str = ""):
    """打印日志"""
    print(f"{emoji} {msg}" if emoji else msg)

class DailyPodcastGenerator:
    def __init__(self):
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID")
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # 本地模型路径（Lexar）
        self.local_model_path = "/Volumes/Lexar/AI-Models/Qwen3-TTS/Base-0.6B"
        self.use_local = Path(self.local_model_path).exists()
        
    def check_requirements(self) -> bool:
        """检查必要配置"""
        log("检查配置...", "🔍")
        
        missing = []
        if not self.notion_token:
            missing.append("NOTION_TOKEN")
        if not self.notion_database_id:
            missing.append("NOTION_DATABASE_ID")
        if not self.dashscope_api_key:
            missing.append("DASHSCOPE_API_KEY")
            
        if missing:
            log(f"❌ 缺少环境变量: {', '.join(missing)}")
            log("请复制 .env.example 为 .env 并填写配置")
            return False
        
        if self.use_local:
            log("Lexar 已连接，可以使用本地模型", "✅")
        else:
            log("Lexar 未连接，将使用 DashScope API", "⚠️")
            
        log("配置检查通过", "✅")
        return True
    
    def get_content_from_notion(self) -> Optional[Dict[str, Any]]:
        """从 Notion 获取今日待发布内容"""
        log("从 Notion 获取内容...", "📝")
        
        try:
            import requests
        except ImportError:
            log("请安装 requests: pip install requests", "❌")
            return None
        
        url = f"https://api.notion.com/v1/databases/{self.notion_database_id}/query"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        
        data = {
            "filter": {
                "and": [
                    {"property": "Status", "select": {"equals": "待发布"}},
                    {"property": "Date", "date": {"equals": self.today}}
                ]
            },
            "sorts": [{"timestamp": "created_time", "direction": "descending"}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            if not results:
                log(f"今天 ({self.today}) 没有待发布的内容", "⚠️")
                return None
            
            page = results[0]
            properties = page.get("properties", {})
            
            # 提取标题
            title_prop = properties.get("Title", {}).get("title", [])
            title = title_prop[0].get("text", {}).get("content", "无标题") if title_prop else "无标题"
            
            # 提取内容
            content_prop = properties.get("Content", {}).get("rich_text", [])
            content = content_prop[0].get("text", {}).get("content", "") if content_prop else ""
            
            log(f"获取内容: {title[:50]}...", "✅")
            return {
                "page_id": page["id"],
                "title": title,
                "content": content,
            }
            
        except Exception as e:
            log(f"Notion API 错误: {e}", "❌")
            return None
    
    def generate_audio_api(self, text: str) -> Optional[str]:
        """使用 DashScope API 生成音频"""
        log("使用 DashScope API 生成音频...", "🎙️")
        
        try:
            import dashscope
            import requests
        except ImportError:
            log("请安装 dashscope: pip install dashscope", "❌")
            return None
        
        dashscope.api_key = self.dashscope_api_key
        
        try:
            # 使用声音克隆或预置音色
            voice_sample = PROJECT_ROOT / "voice-sample.wav"
            
            if voice_sample.exists():
                log(f"使用声音样本: {voice_sample}")
                # 上传声音样本获取 URL（简化版，实际需要先上传）
                response = dashscope.audio.tts.call(
                    model="qwen3-tts-vc-realtime-2026-01-15",
                    text=text,
                    voice="Cherry",  # 暂时用预置音色
                )
            else:
                log("使用默认音色: Cherry")
                response = dashscope.audio.tts.call(
                    model="qwen3-tts-flash-realtime",
                    text=text,
                    voice="Cherry",
                )
            
            # 下载音频
            audio_url = response.output.url
            audio_path = PROJECT_ROOT / "public" / "audio" / f"podcast-{self.today}.mp3"
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            
            r = requests.get(audio_url, timeout=60)
            r.raise_for_status()
            with open(audio_path, "wb") as f:
                f.write(r.content)
            
            log(f"音频生成: {audio_path}", "✅")
            return str(audio_path)
            
        except Exception as e:
            log(f"API 生成失败: {e}", "❌")
            return None
    
    def generate_audio(self, text: str) -> Optional[str]:
        """生成音频"""
        return self.generate_audio_api(text)
    
    def create_episode(self, title: str, content: str, audio_path: str) -> str:
        """创建播客元数据"""
        log("创建播客文件...", "📄")
        
        # 估算时长（中文约 250 字/分钟）
        chars = len(content.replace(" ", "").replace("\n", ""))
        minutes = max(1, round(chars / 250))
        duration = f"{minutes}:00"
        
        episode = {
            "id": self.today,
            "title": title,
            "date": self.today,
            "audio": f"/audio/podcast-{self.today}.mp3",
            "content": content[:500] + "..." if len(content) > 500 else content,
            "duration": duration,
            "created_at": datetime.now().isoformat(),
        }
        
        # 保存
        episode_path = PROJECT_ROOT / "content" / "episodes" / f"{self.today}.json"
        episode_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(episode_path, "w", encoding="utf-8") as f:
            json.dump(episode, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self._update_index(episode)
        
        log(f"播客文件: {episode_path}", "✅")
        return str(episode_path)
    
    def _update_index(self, new_episode: dict):
        """更新索引"""
        index_path = PROJECT_ROOT / "content" / "episodes" / "index.json"
        
        episodes = []
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as f:
                episodes = json.load(f)
        
        # 去重并添加新播客
        episodes = [e for e in episodes if e["id"] != new_episode["id"]]
        episodes.insert(0, new_episode)
        episodes.sort(key=lambda x: x["date"], reverse=True)
        
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(episodes, f, ensure_ascii=False, indent=2)
    
    def update_notion_status(self, page_id: str):
        """更新 Notion 状态"""
        log("更新 Notion 状态...", "🔄")
        
        try:
            import requests
            
            url = f"https://api.notion.com/v1/pages/{page_id}"
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            }
            data = {"properties": {"Status": {"select": {"name": "已发布"}}}}
            
            response = requests.patch(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            log("Notion 状态已更新为「已发布」", "✅")
            
        except Exception as e:
            log(f"更新 Notion 状态失败: {e}", "⚠️")
    
    def run(self) -> bool:
        """运行完整流程"""
        print(f"\n{'='*50}")
        log(f"播客自动生成器 - {self.today}", "🚀")
        print(f"{'='*50}\n")
        
        # 1. 检查配置
        if not self.check_requirements():
            return False
        
        # 2. 获取内容
        content_data = self.get_content_from_notion()
        if not content_data:
            return False
        
        # 3. 生成音频
        audio_path = self.generate_audio(content_data["content"])
        if not audio_path:
            log("音频生成失败", "❌")
            return False
        
        # 4. 创建播客文件
        self.create_episode(content_data["title"], content_data["content"], audio_path)
        
        # 5. 更新 Notion
        self.update_notion_status(content_data["page_id"])
        
        print(f"\n{'='*50}")
        log("播客生成完成！", "✅")
        print(f"{'='*50}\n")
        
        return True

def main():
    generator = DailyPodcastGenerator()
    success = generator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
