# Validation record / 驗證紀錄

2026-10-28 · macOS 27 · Apple Silicon · FFmpeg 7.1.

| Check / 檢查 | Result / 結果 |
|---|---|
| Python syntax / Python 語法 | Three scripts compile / 三個腳本通過 |
| Real Chinese footage, official mode / 真實中文素材官方框版 | 25.4 s, 1920×886, 30 fps |
| Real Chinese footage, plain mode / 真實中文素材無框版 | 25.4 s, 1920×886, 30 fps |
| Full decode / 完整解碼 | Both exports passed / 兩版通過 |
| Inherited rotation / 殘留旋轉 | No nonzero display rotation / 無非零旋轉 |
| Storyboard duration / 分鏡長度 | Both match within one frame / 均在一幀誤差內 |
| Manual frames / 人工畫面檢查 | Correct app, captions and official frame alignment / App、字幕與機身對位正確 |
| Private assets ignored / 本機素材忽略 | Confirmed via git check-ignore / 已確認 |
| App Store review / 商店審核 | Not submitted or assessed / 未提交、未判定通過 |

The capture wrapper is a thin subprocess wrapper around the recording command used in production. It is syntax-checked; full end-to-end wrapper capture is not claimed by this initial record. The renderer and validator were exercised on real source footage, not only synthetic tests.
錄影 wrapper 是既有實測命令的程序包裝；初版只確認語法，不宣稱已完整實測 wrapper 錄影。剪輯與驗證腳本則已使用真實素材完整執行。

An odd native screenshot dimension exposed a YUV padding limitation. The official renderer now uses RGBA before the native screen pad, then converts to yuv420p at the encoded output. This preserves the odd-sized screen aperture without stretching.
原生截圖奇數尺寸曾觸發 YUV 補邊限制；官方框模式在原生螢幕補邊前轉 RGBA，輸出編碼時才轉 yuv420p，保留對位與比例。

Full reports and source files remain in local-assets/ and output/ on the production machine. Their local filesystem paths and simulator identifiers are not published.
完整報告與素材留在製作機的 local-assets/、output/；不公開本機路徑及模擬器識別資訊。
