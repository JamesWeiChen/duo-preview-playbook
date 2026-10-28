# Instructions for future AI assistants / 給未來 AI 的指引

Read README.md (or README.zh-Hant.md), the matching workflow and asset guide before recording or editing.
先讀 README、製作流程與素材指引，再操作模擬器或剪輯。

1. Scope: media and documentation only unless the user requests app changes. Preserve existing work and never publish the application's repository as this playbook.
   範圍限素材與文件；未獲要求不要改 App，也不要把 App repo 當作本手冊發布。
2. Discover tools and inspect the current simulator. Use an explicit UDID. Read the installed duoctl instructions. Keep only one interaction owner and one recorder per simulator.
   先確認工具、UDID 與 duoctl 指引；同一模擬器只由一人操作、一次只錄一個顯示器。
3. Use isolated sample data. Read UI hierarchy and screenshot before/after interaction; recapture after every fold. Do not reuse old coordinates.
   使用隔離範例資料；每次互動及開闔後重新讀取畫面與階層，不沿用舊座標。
4. For a continuity claim, log fold sensor state, active display, app PID, selected content and unsaved text before/after. Never relaunch halfway and claim the draft survived.
   連續性須記錄感測姿勢、啟用螢幕、App PID、所選內容與未存文字；不可重啟後冒稱保留成功。
5. Inspect actual video frames, not just successful tool exit. Reject SpringBoard, wrong app, frozen inactive display, keyboard mismatch and accidentally recorded dialogs.
   實際看影片；指令成功不等於錄對。排除主畫面、錯誤 App、未啟用螢幕凍結、鍵盤語言不符或對話框。
6. Use Apple PNGs locally with official download links publicly. Do not commit DMG, PSD, PNG, fonts, third-party promotional clips, app databases or logs containing identifiers. Keep local-assets/ ignored.
   官方機身素材留本機，公開分享連結；不要提交素材包、字型、別人的影片、資料庫或識別資訊。
7. Do not produce a self-modeled Apple device as public marketing artwork. Follow current official guidance. Do not describe marketing footage as an approved App Store preview.
   公開宣傳採目前官方指引允許的素材；不要把自建 Apple 機身模型或宣傳剪輯當成商店已核准版本。
8. Resample VFR before trim, normalize rotation after encoding, then decode the entire output and inspect contact sheets plus full-size frames. Keep rendering reproducible through the JSON manifest.
   VFR 先轉固定幀率再裁時間；編碼後清除旋轉資訊，完整解碼並檢查縮圖與原尺寸畫面；保留 JSON。
9. For English output, change UI, fixture text and keyboard as well as captions. Record any intentionally untranslated proper names.
   英文版同步更改介面、範例文字與鍵盤；專有名詞保留原文須註明。
10. Before a public push: inspect the exact staged list, run the renderer/validator smoke checks, verify that local-assets is ignored, then publish only this standalone repository if authorized.
    公開前檢查實際 staged 清單、腳本實測與忽略規則；有授權才發布這個獨立 repo。

Local-only inventory: if local-assets/INDEX.md exists, read it. Public clones must supply their own footage; never invent missing media or claim it was captured.
本機另讀 local-assets/INDEX.md；公開下載者必須自己提供素材，AI 不可捏造缺少的錄影或實測結果。
