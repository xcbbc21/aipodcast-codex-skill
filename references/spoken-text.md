# Spoken text: numbers, English, figures, footnotes, and TTS export

Use this reference for all narration text.

## Numbers and dates

Choose readings by meaning:

| Context | Spoken form |
| --- | --- |
| Year or historical date | Digit-by-digit Chinese year, such as 二〇二五年 |
| Amount, count, duration, or scale | Natural quantity, such as 一千九百九十九元 |
| Ratio, percentage, decimal, or multiple | Mathematical reading, such as 百分之零点二、三点五倍 |
| Code, model, or account number | Digit-by-digit reading |
| Episode, chapter, or issue number | Natural ordinal; `第 002 讲` becomes `第二讲` |

Preserve units, denominators, dates, comparison bases, and direction. For example, a change from zero point two percent to one percent is an increase of zero point eight percentage points and a level five times as large; choose the wording that matches the source claim.

## English and citations

On first use, provide a necessary Chinese identity or function before an English abbreviation. Keep author-year brackets and URLs in written records unless the identity or date is part of the argument. Do not make listeners decode a dense sequence of English names, symbols, or citations when a concise Chinese explanation is clearer.

## Figures, tables, and footnotes

For every substantive figure, record the axes, units, range, series, relevant value or trend, source note, and uncertainty before deciding what enters the narration. Never infer an exact value from an unclear image.

### 纯音频的图表处理

- 图表只是重复正文：检查图表与正文是否一致，在覆盖表记录“与正文重复，未单独口播”，不在朗读稿中提图。
- 图表包含正文没有展开的独有信息：把必要的数据、比较关系、趋势或限定条件改写成自然语言，并放在它所支持的论证附近。
- 图号、图例颜色、线型、左右位置和“见图”“如下图”等视觉导航只留在覆盖表或书面档案中，不进入纯音频朗读文本。
- 只有用户明确要求同步视频、配套画面或可视阅读时，才可以保留听众实际能够看到并使用的视觉指引。

因此，纯音频稿应说“数据显示，美元储备占比从约百分之六十五降至百分之五十七”，而不是“图一之五显示……”；如果这项数据已经在正文中完整出现，则不再增加一段图表说明。

Classify footnotes as definition, limitation, argument support, bibliography, or link. Bring the first three into adjacent speech when they change the listener’s understanding. Keep bibliography and links in the written record.

## Export text for synthesis

The Markdown file is an archive. The text passed to the synthesizer is a separate plain-text export. Remove the title unless the series configuration says it should be spoken; always remove metadata blocks, Markdown markers, raw footnote symbols, URLs, and source-only citation brackets. Preserve paragraph breaks where a pause helps listening.
