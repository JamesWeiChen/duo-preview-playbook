# Official assets and references

[繁體中文](assets.zh-Hant.md)

## Download directly from Apple

- [Apple Design Resources → Product Bezels](https://developer.apple.com/design/resources/#product-bezels)
- [iPhone Duo Photoshop / PNG package (.dmg)](https://devimages-cdn.apple.com/design/resources/download/Bezel-iPhone-Duo.dmg)
- [Marketing Resources and Identity Guidelines](https://developer.apple.com/app-store/marketing/guidelines/)

Download the DMG, open it on macOS, review its license, and copy these files into `local-assets/apple/PNG/`:

```text
iPhone Duo - Star White - Outer Closed Portrait.png
iPhone Duo - Star White - Inner Open Landscape.png
```

Retain the included license beside the assets. If a direct URL changes, return to Apple's resources page rather than using an unofficial mirror. This repo does not auto-accept a license for other users.

The inspected package has Star White and Night Sky variants. PNGs cover outer open, outer closed portrait/landscape, and inner open portrait/landscape. PSDs also include inner partially open portrait/landscape. **No ready-made hinge animation or general-purpose animation toolkit was in this package.** Figma/Sketch UI design kits solve a different problem; they are not a product animation export tool.

## Exact mapping used in this version

| PNG | Canvas | Screen rectangle: x, y, width, height |
|---|---|---|
| Star White Outer Closed Portrait | 1574×2194 | 88, 80, 1398, 2034 |
| Star White Inner Open Landscape | 3093×2247 | 120, 120, 2853, 2007 |

These values were checked from the PNG alpha channel and actual screenshots. Composite app footage behind the transparent screen aperture and the unmodified product PNG above it. Use equal product scale for the two poses. The sample plans use 0.336, a 1920×886 canvas and captions above the device. Verify alignment if Apple changes the package. Native recording dimensions can be one pixel smaller; preserve aspect ratio rather than stretching.

## What may be shared

Our MIT license covers our original scripts/docs, not Apple's assets, fonts, other apps' promotional clips or downloaded tools. Share official source links and placement instructions. Keep downloaded source artwork in ignored local storage and do not redistribute it as an open-source asset pack.

Apple's published marketing guidance says to use provided product images as supplied; it lists animating/flipping/spinning them and rendering simulations of Apple products among restricted uses. Our self-modeled 3D experiment was therefore not used for the public marketing cut. Review the current terms for your use. This guide is a workflow record, not legal advice or Apple approval.

## Reference demonstrations

- [Apple's developer showcase](https://www.apple.com/newsroom/2026/10/developers-bring-incredible-new-app-experiences-to-iphone-duo/) and [Netflix video](https://www.apple.com/newsroom/videos/2026/autoplay/10/netflix-app-on-iphone-duo/large_2x.mp4): the viewed ~14-second official promotional clip visibly opens the device while content continues. We studied the narrative, not copied its footage. Its production permissions are not established for third-party developers.
- [Things official blog](https://culturedcode.com/things/blog/): reviewed images/text showing outer lists, inner sidebar, notes and keyboard. Not verified as an App Store preview video.
- [Fantastical / Cardhop official post](https://flexibits.com/blog/2026/10/twice-as-nice-fantastical-cardhop-go-iphone-duo/): reviewed images/text contrasting closed single-pane use with open calendar/contact layouts. Not verified as an App Store preview video.

Sources checked 2026-10-28. Re-check current resources and rules before publication.
