# 官方素材與參考來源

[English](assets.en.md)

## 直接向 Apple 下載

- [Apple Design Resources → Product Bezels](https://developer.apple.com/design/resources/#product-bezels)
- [iPhone Duo Photoshop／PNG 素材包（DMG）](https://devimages-cdn.apple.com/design/resources/download/Bezel-iPhone-Duo.dmg)
- [行銷素材使用指引](https://developer.apple.com/app-store/marketing/guidelines/)

下載 DMG，在 macOS 開啟並閱讀授權，將以下檔案放入 `local-assets/apple/PNG/`：

```text
iPhone Duo - Star White - Outer Closed Portrait.png
iPhone Duo - Star White - Inner Open Landscape.png
```

同時保留包內授權檔。直接連結若失效，回官方資源頁找最新版，不使用不明鏡像。本 repo 不替其他使用者自動接受授權。

本次檢查的包有 Star White、Night Sky 兩款。PNG 包含外屏展開、外屏闔上直／橫向、內屏展開直／橫向；PSD 另含內屏半展開直／橫向。**包內沒有現成鉸鏈動畫或通用開闔動畫工具。** Figma／Sketch UI 設計包是另一種用途，不是機身動畫輸出器。

## 本次實際對位

| PNG | 畫布尺寸 | 螢幕區：x、y、寬、高 |
|---|---|---|
| Star White Outer Closed Portrait | 1574×2194 | 88、80、1398、2034 |
| Star White Inner Open Landscape | 3093×2247 | 120、120、2853、2007 |

依 PNG alpha 與實際截圖確認。將 App 畫面放在透明螢幕孔後方，原貌機身 PNG 疊在前方。兩種姿勢採相同比例；範本使用 0.336、1920×886 畫布、機身上方字幕。Apple 更新素材後要重新核對，不能盲用舊尺寸。原生影片可能少一像素，要保持比例而非拉伸。

## 公開分享範圍

MIT 授權只適用我們原創的腳本／文件，不含 Apple 素材、字型、其他 App 宣傳影片或下載的工具。公開提供官方連結與放置方式，本機下載的來源素材留在 Git 忽略目錄，不當成開源素材包散布。

Apple 公開行銷指引要求機身圖保持原貌，並列出動畫化、翻轉、旋轉圖片與自製 Apple 機身 3D 模擬等限制。因此這次自建 3D 實驗未採用於公開宣傳成片。依用途重新查核當時條款；本手冊是實作紀錄，不是法律意見或 Apple 核准。

## 參考展示

- [Apple 開發者展示](https://www.apple.com/newsroom/2026/10/developers-bring-incredible-new-app-experiences-to-iphone-duo/)／[Netflix 影片](https://www.apple.com/newsroom/videos/2026/autoplay/10/netflix-app-on-iphone-duo/large_2x.mp4)：實際觀看約 14 秒官方宣傳片，機身明顯展開、同內容延續。參考敘事，未複製影片，也未確認第三方開發者有相同製作授權。
- [Things 官方部落格](https://culturedcode.com/things/blog/)：核對圖文中的外屏清單、內屏側欄、筆記與鍵盤，未確認是 App Store 預覽影片。
- [Fantastical／Cardhop 官方文章](https://flexibits.com/blog/2026/10/twice-as-nice-fantastical-cardhop-go-iphone-duo/)：核對圖文的闔上單欄與展開日曆／聯絡人雙欄，未確認商店預覽影片。

來源查核日 2026-10-28；公開或上架前再查最新版。
