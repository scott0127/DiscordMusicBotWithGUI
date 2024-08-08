
---

# Discord 音樂機器人帶有 GUI

這個項目是用 Python 編寫的一個 Discord 音樂機器人，具有圖形用戶界面（GUI），可以在 Discord 聊天中播放音樂。它支持從 YouTube 和 Spotify 播放音樂，並提供了一些基本的音樂控制功能。
-HACKMD=> HackMD URL: https://hackmd.io/@pakkkk/SyAM5MGqC
-HACKMD那邊有些操作上的說明與STEP BY STEP
## 功能介紹

- **播放 YouTube 音樂**：使用 `!play` 命令可以通過網址或關鍵詞播放 YouTube 上的音樂。
- **加入/離開語音頻道**：使用 `!join` 和 `!leave` 命令來控制機器人加入或離開語音頻道。
- **Spotify 播放列表**：使用 `!spotlist` 命令可以播放 Spotify 的播放列表。
- **AI 問答**：使用 `!ai` 命令可以向 AI 提出問題，並獲得回答。
- **網頁界面**：提供了一個網頁界面，用於查找和管理播放列表中的音樂。

## 安裝說明

1. **克隆項目**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **安裝必需的 Python 套件**

   運行以下命令以安裝所需的 Python 套件：

   ```bash
   pip install -r requirements.txt
   ```

3. **設置環境變數**

   創建一個 `.env` 文件，並填入以下信息：

   ```
   discord_token=YOUR_DISCORD_BOT_TOKEN
   下面三個不一定要
   spotify_client_id=YOUR_SPOTIFY_CLIENT_ID  
   spotify_client_secret=YOUR_SPOTIFY_CLIENT_SECRET
   spotify_redirect_uri=YOUR_SPOTIFY_REDIRECT_URI
   ```

   - 您可以從 [Discord 開發者門戶](https://discord.com/developers/docs/intro) 獲取 Discord Bot 的 Token。
   - 從 [Spotify 開發者平臺](https://developer.spotify.com/dashboard/) 獲取 Spotify 的客戶端 ID 和客戶端密鑰。 不一定要

4. **運行機器人**

   執行以下命令以啟動機器人：

   ```bash
   python .\BotWithPage.py
   ```

5. **網頁界面**

   機器人運行後，您可以在瀏覽器中訪問 `http://localhost:8080`，使用網頁界面進行音樂搜索和播放列表管理。

## 使用說明

- **播放音樂**：在 Discord 中使用命令 `!play <歌曲名稱或YouTube鏈接>` 播放音樂。
- **加入語音頻道**：使用命令 `!join` 讓機器人加入您所在的語音頻道。
- **離開語音頻道**：使用命令 `!leave` 讓機器人離開語音頻道。
- **播放 Spotify 播放列表**：使用命令 `!spotlist <Spotify 播放列表鏈接>` 來播放 Spotify 播放列表中的歌曲。
- **AI 問答**：使用命令 `!ai <問題>` 提出問題，獲得 AI 的回答。

## 代碼結構

- `main.py`：主程式，負責處理 Discord 機器人的命令和功能。
- `music_controls.py`：定義音樂控制界面和功能。
- `playlist_controls.py`：定義播放列表控制界面和功能。
- `cohere_client.py`：處理與 AI 的交互功能。
- `custom_playlist.py`：定義自定義播放列表的結構和功能。

## 貢獻

歡迎對本項目進行貢獻！您可以通過 Fork 本倉庫並提交 Pull Request 來提交您的更改。

---

---

# Discord Music Bot with GUI

This project creates a Discord music bot with a graphical user interface. Follow the steps below to set up and run the bot.

## Setup Instructions

1. **Install Required Python Packages**

   Run the following command to install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a Discord Bot Account**

   - Visit the [Discord Developer Portal](https://discord.com/developers/docs/intro).
   - Log in or sign up for a new account if you haven't already.
   - Navigate to the **Applications** section and click on **New Application** to create a new application.
   - Go to the **Bot** tab on the left-hand side and click **Add Bot**.
   - Click **Reset Token** to generate a new token for your bot.

3. **Configure Environment Variables**

   - Open the `.env` file in the project directory.
   - Replace the `discord_token` value with the token you generated:

     ```
     discord_token=YOUR_DISCORD_BOT_TOKEN
     ```

4. **Run the Bot**

   Execute the following command to start the bot:

   ```bash
   python .\BotWithPage.py
   ```

For detailed, step-by-step instructions, refer to the project's documentation on HackMD.

HackMD URL: [https://hackmd.io/@pakkkk/SyAM5MGqC]

---
