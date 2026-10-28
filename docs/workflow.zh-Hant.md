# 拍攝與剪輯流程

[English](workflow.en.md)

## 1. 先決定交付用途

宣傳展示與 App Store 上架預覽分開處理。[Apple 預覽指引](https://developer.apple.com/app-store/app-previews/) 強調連貫故事、實際 App 內容、在地化及簡單轉場。上傳時重新核對[最新規格](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications/)。本次查核時：15–30 秒、最高 30 fps、500 MB 上限；Duo 支援橫向 1920×886／直向 886×1920。技術檢查通過，不代表內容或審核通過。

套官方機身的版本用於宣傳。商店版從原生 App 錄影剪輯，依當時規定製作並在 App Store Connect 驗證。Apple 自己發布的宣傳影片，不能當作所有開發者都能採用的商店預覽形式。

## 2. 分鏡：同一工作，兩種螢幕

| 鏡頭 | 原始片段長度 | 展示重點 | 中文字幕 |
|---|---:|---|---|
| 闔上看講題 | 4 秒 | 快速查看 | 闔上，隨手查看講題 |
| 展開同一講題 | 5 秒 | 議程與詳情同時看 | 展開，議程與講題並排 |
| 展開寫筆記 | 6 秒 | 參照與輸入並行 | 一邊參照，一邊記錄 |
| 闔上未存筆記 | 5 秒 | 草稿保留 | 再闔上，剛寫的筆記還在 |
| 再展開儲存 | 7 秒 | 參照欄回來、儲存成功 | 再展開，接著寫、接著存 |

扣除四次 0.4 秒重疊後為 25.4 秒。字幕放在機身外，App 文字要看得清楚。`recordVideo` 不會錄到實體鉸鏈動畫，內外屏是不同錄影片段銜接。使用真實截圖定格須在製作紀錄說明，不能宣稱連續錄到了動作。

## 3. 準備 App 與操作環境

- 用隔離測試資料、虛構人物及一致的外觀／字級，不為清空畫面而刪使用者資料。
- Acadenda 的 `-ScreenshotTestStore` 使用記憶體範例資料；`-ScreenshotHideCloudSyncBanner` 只隱藏拍攝橫幅。這是 **App 專屬參數**，不是通用 iOS 設定。
- 英文版啟動時設定 App 語言與地區，使用英文筆記，實際檢查鍵盤語言；App 語言不一定會切換鍵盤。
- 長時間拍攝優先使用穩定的獨立啟動。工作區 debug session 結束可能一起關閉 App；不要只為拍攝而修改產品程式。
- 操作前後讀取階層與截圖，優先用 hitPoint；確認無效後才以畫面估計。每次開闔後座標及可及性參照都需重新取得。

## 4. 一次錄一個顯示器

先確認自己的顯示器編號。本次外屏是 **1**、內屏是 **3**，不能當作永遠固定。外屏截圖 **1398×2034**，內屏橫向 **2853×2007**；影片可能因編碼偶數尺寸與旋轉 metadata 而略有不同。

```sh
# 換成自己的 UDID，duoctl 需另外安裝。
duoctl -d YOUR_UDID state
duoctl -d YOUR_UDID close
duoctl -d YOUR_UDID screenshot local-assets/before.png

# 此終端錄影，從另一工具或終端操作 App。
python3 scripts/record.py --device YOUR_UDID --display 1 --seconds 12 local-assets/recordings/outer.mov
```

開闔後讀回 `duoctl state` 的實測姿勢與啟用螢幕，指令成功不等於畫面正確。本次半折可能讀到約 91–95 度，展示不必糾結正好 90 度。

後來英文重拍另發現：完全靜止畫面實際錄九秒，卻只寫一幀、容器長度僅 0.07 秒。錄影程序經過時間不等於影片長度，裁切前一定要讀容器 duration。需要時錄入真正的 UI 操作產生後續幀，或明確標為截圖定格；不能補長靜態影格後稱為連續錄影。

同一模擬器同時錄兩個顯示器會出現 `Resource busy`。先結束第一段，再開闔、確認 App，然後錄目前啟用螢幕。錄未啟用螢幕會停在上一幀，**不會錄到實體開闔過程**。

腳本只向自己啟動的 recorder PID 發 SIGINT，等待影片容器寫完；不要用 `pkill` 殺全部 simctl。保留錄影 log，連續性段落前後比對 App PID。安裝 duoctl 不代表所有未來 session 都自動取得 CoreSimulator 權限。

## 5. 選擇真正有效的素材

每一段都看縮圖與關鍵原尺寸影格。本次曾有影片正常寫盤，卻因 debugger session 結束而全段錄到 SpringBoard；已排除，改用同一時刻的真實展開截圖。講題與筆記段是不同次啟動；筆記的 open→closed→open→save 全程維持同一個 App 行程，紀錄不能混淆。

鍵盤必須是真的，每次開闔後確認仍可用，結束時恢復。不要畫假鍵盤，也不要把私人 helper 冒充 Apple 支援的正式 API。

填寫 `examples/evidence.template.json`：前後 PID、感測姿勢、啟用顯示器、所選內容、完整未存文字、素材檔名、檢查結果與是否重啟。

## 6. 可重現剪輯

使用 `examples/plan.zh-Hant.json` 或 `plan.en.json`，修改來源路徑、時間及字幕。`kind: still` 代表真實截圖定格，不是錄影動態。腳本會檢查實際容器長度，拒絕超出來源的區間。來源必須長於裁切區間；腳本不會偷偷補長短錄影來掩蓋缺少的素材。

- 先 `fps=30` **再** `trim`；模擬器靜態畫面可能是極低幀率 VFR。
- FFmpeg 先依輸入資訊轉正像素，編碼後用 `-display_rotation 0 -c copy` remux。這次 FFmpeg 7.1 僅設 `-metadata:s:v rotate=0` 無法清除殘留旋轉矩陣。
- 合併後明確設定 `-r 30 -fps_mode cfr`，避免 time base 造成非預期幀率。
- 保留比例，不把展開畫面壓成外屏；官方螢幕對位尺寸見素材文件。
- 輸出 H.264 High／Level 4、yuv420p、11 Mbps 目標 CBR、fast-start MP4、48 kHz 立體聲 AAC 靜音軌。靜音實測 bitrate 可能遠低於指定的 256 kbps，不能只憑命令列目標宣稱音軌合規。
- 字幕使用 UTF-8 檔，關閉 FFmpeg 文字展開；路徑以 process 參數傳遞，不插入 shell；JSON 不執行任意命令。

## 7. 驗證與交付

執行 `scripts/validate.py` 完整解碼、檢查本預設的長度／幀率／解析度／旋轉、算 SHA-256 並產生縮圖。這只是技術篩檢，不是商店認證。

人工確認：正確 App、相同內容、未存文字真的保留、介面及鍵盤語言、字幕可讀、鏡頭挖孔對位、按鈕未裁掉、最後成功儲存、沒有主畫面或意外對話框、方向正確。轉場也要播放確認；縮圖拼貼最後未用的黑格不一定是影片黑幀。

本機保留原片、JSON、感測證據、成片及報告；公開只分享可重用腳本、文件與連結。不要把 Apple 素材包或使用者資料放到公開 repo。結束 interaction session，只停止自己啟動的錄影程序。
