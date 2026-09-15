# Fidelity mode: source coverage and claim review

Use this reference for books, reports, lectures, PDFs, scanned documents, or any request that asks for original-text fidelity.

## Establish the source boundary

Record the source title and version, file paths, requested chapter or page range, original and physical page numbering, and the agreed episode map. If the book has no native “lecture” divisions, say that the episode map is editorial. Determine chapter starts and ends from the actual source, not from fixed episode counts.

Inspect scanned pages before trusting OCR. Treat prior scripts and OCR output as aids, not as proof of source content.

## Build a coverage table for every episode

Create a companion file beside the proposed narration, for example `02-...-coverage.md`. It may be Markdown, but it must contain the following information.

| Field | Required record |
| --- | --- |
| Unit ID | Stable source-unit identifier |
| Source location | Page, paragraph, chart, table, or footnote location |
| Type | Question, definition, claim, reasoning, example, data, counterexample, condition, or conclusion |
| Role | What the unit contributes to the argument |
| Script location | Paragraph or anchor in the narration |
| Treatment | Spoken, merged as repetition, retained in written notes, or pending verification |
| Status | Verified, uncertain, or unresolved; include the reason |

Every omitted substantive source unit needs a stated reason. Bibliographic details can remain written-only; definitions, qualifications, exceptions, and evidence that affect the conclusion cannot be silently dropped.

### Completion gate

“出现了同一主题”不是覆盖证据。逐项核对最小语义单元，并确保覆盖表没有“待复核、未核验、未解决”状态。存在待复核项时不得标记完成，也不得用“结构检查通过”代替内容验收。

Compare the source and spoken-text sizes only as an alarm. A severe unexplained reduction is `疑似过度压缩`: return to the unit map and inspect lost reasoning, examples, counterexamples, qualifications, figures, and meaningful footnotes. Do not pad a genuinely short episode, and do not use a favorable ratio as proof of fidelity.

## Review in both directions

1. Read from the source to the script. Verify that every substantive unit has an appropriate destination.
2. Read from the script back to the source. Verify factual support, speaker attribution, time period, unit, comparison baseline, direction of change, and conditional language.
3. Read the script continuously. Remove repetition and add only explanations needed to make the existing argument audible.

Do not use character totals, sentence totals, OCR confidence, or a completed table as substitutes for this review.

## Material types

- `S` — source content: facts, figures, quotations, author conclusions, and stated uncertainty. It must be traceable.
- `E` — explanation: a paraphrase or clearly hypothetical example that helps listeners understand `S`. It cannot change the source’s causal strength or attribution.
- `X` — extension: external facts, commentary, forecasts, or value judgments. Include only when the user allows it and make its status audible when needed.

Use natural speech rather than literal labels. For example: “作者的判断是……” for a source conclusion, or “可以这样理解……” for an explanatory analogy.

## Source uncertainty

保留“可能、倾向于、在某种条件下、作者认为、估算”等限定语。OCR 与扫描页冲突时，以清晰可见的扫描页为准；数值仍无法确认时，在覆盖表标记为待复核，不把猜测写成已确认事实。

For externally updated facts, preserve the original historical claim first. Add current information only when the user asks, and identify it as an update with its source.
