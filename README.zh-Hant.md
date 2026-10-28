# Duo 預覽影片製作手冊

[English](README.md) · [完整流程](docs/workflow.zh-Hant.md) · [官方素材](docs/assets.zh-Hant.md) · [AI 執行指引](AGENTS.md)

整理 **2026-10-28** 製作 Acadenda Duo 展示影片的實際經驗，環境是 **Xcode 27.2 RC（27B48）、iOS 27.2 模擬器、Apple Silicon／macOS 27**。包含成功方法、失敗原因，以及下一個 AI 必須重新驗證的事項。

影片主軸是同一工作在 **闔上 → 展開 → 闔上 → 再展開** 之間延續：讓人看懂大螢幕多了什麼用途，並展示未儲存筆記仍保留。一直錄已展開畫面，無法清楚傳達這件事。

## 包含內容

- 中英文拍攝手冊、踩坑紀錄、素材來源、使用指引與五幕分鏡。
- 單一顯示器錄影、JSON 控制的 FFmpeg 剪輯、完整解碼與縮圖檢查腳本。
- 中英文字幕範本、開闔連續性證據範本，以及給 AI 的交接指引。
- 不含 App 原始碼、個人模擬器資料或帳號資訊。

**不重新散布 Apple 機身圖、字型、FFmpeg 執行檔或 duoctl。** 文件提供官方直接連結及存放方式。本機素材放入 Git 忽略的 `local-assets/`。

## 快速開始

需要 Python 3、FFmpeg **7.1 以上**（含 libx264、drawtext、xfade、-display_rotation）、支援字幕語言的字型。錄影另需 macOS、Xcode、已啟動 Duo，以及獨立安裝的 [duoctl 相容分支](https://github.com/JamesWeiChen/duoctl)。

```sh
python3 -m venv .venv
.venv/bin/pip install imageio-ffmpeg==0.6.0

# 將五段錄影放進 local-assets/recordings/zh-Hant/。
# 依 docs/assets.zh-Hant.md 下載並放入官方 PNG。
.venv/bin/python scripts/render.py examples/plan.zh-Hant.json output/demo-zh-Hant.mp4 --mode official
.venv/bin/python scripts/validate.py output/demo-zh-Hant.mp4 --report output/demo-zh-Hant.validation.json --expected-seconds 25.4
```

也可使用 PATH 上的 FFmpeg，或設定 `FFMPEG=/絕對路徑/ffmpeg`。預設使用 macOS STHeiti Medium，其他環境以 `--font /path/to/font.ttf` 指定字型。JSON 內路徑相對於該 JSON；腳本不覆寫既有成片。`--mode plain` 不套機身，但不代表自動符合商店審核。

英文版請將 App 介面、範例筆記、鍵盤一起切換成英文，再用 `examples/plan.en.json`；不能只翻字幕就稱為全英文版。

## 宣傳影片與商店預覽的差別

官方機身版屬於**宣傳展示影片**。Apple 的 App Preview 指引要求展示 App 內的內容；長度、解析度與編碼通過技術檢查，不等於通過商店審核。上架時另外準備以 App 畫面為主的版本，重新核對官方要求。本專案不宣稱任何成片已通過 App Store 審核。

## 實測限制

原版五幕共 25.4 秒：4＋5＋6＋5＋7 秒，扣除四次 0.4 秒轉場。講題展開那幕採真實截圖定格，因原錄影在 debug session 結束後錄到主畫面。筆記段則在另一個不中斷的 App 行程中完成開闔與儲存，不能宣稱整支影片同一次啟動。

完整細節見[製作流程](docs/workflow.zh-Hant.md)、[素材與來源](docs/assets.zh-Hant.md)、[驗證紀錄](docs/validation.md)。顯示器編號、私有 API 行為、機身尺寸都是本次觀察，未來版本必須重新確認。

## 致謝與授權

本專案原創文件及腳本：Copyright 2026 JamesWeiChen，MIT 授權。[致謝](CREDITS.md) 區分我們的工作與 Apple、FFmpeg、duoctl。這是製作手冊，**不是 duoctl 的 fork**；僅呼叫另外安裝的工具，未包含其實作。與 Apple 無隸屬或背書關係。
