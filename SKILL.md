---
name: aipodcast
description: Use when turning Chinese books, reports, articles, or approved scripts into single-narrator TTS-ready narration and optional MP3 files, especially when source fidelity, page-level coverage, spoken numbers, charts, footnotes, or natural episode endings matter.
---

# aipodcast

Create a single-narrator listening script whose scope, claims, and structure can be checked before synthesis. Use this skill for narration work; do not use it to create a dialogue podcast.

## Route the request

| User intent | Mode | Read |
| --- | --- | --- |
| “按原书”“精读”“完整覆盖”“核对资料” | `fidelity` | [fidelity-mode.md](references/fidelity-mode.md), [narration-design.md](references/narration-design.md), [spoken-text.md](references/spoken-text.md) |
| “这是定稿，转成口播或 MP3” | `authored` | [narration-design.md](references/narration-design.md), [spoken-text.md](references/spoken-text.md) |
| “扩写、评论、故事化、加入观点” | `adaptation` | [fidelity-mode.md](references/fidelity-mode.md), [narration-design.md](references/narration-design.md), [spoken-text.md](references/spoken-text.md) |

Only read [batch-production.md](references/batch-production.md) and run synthesis checks when the user requests audio.

## Required outcome

1. Confirm the source range, episode map, and whether the requested output is a plan, script, or audio.
2. 在原书精读的 `fidelity` 模式中，先把定义、主张、推理、例证、数据、反例、限定、图表和有效脚注拆成最小语义单元，再建立逐讲覆盖表；定稿前完成双向语义复核。
3. Write natural spoken Chinese. Keep source facts, speakers, dates, units, conditions, counterexamples, and uncertainty intact.
4. Use the source's information density to determine episode length. Do not pad short episodes or compress dense episodes to fit a preset word count or sentence count.
5. 连续系列从第二讲开始，开头必须有简短的“上一讲回顾”：说清前一讲已经得到的核心结论，再指出它如何引出本讲；第一讲不强行回顾不存在的上一讲，只承担章节总起。回顾不能取代本讲的独立背景，也不能把前一讲整段重讲。
6. End with a concise answer to the episode's central question, then use a natural close. 默认一个主思考问题，并在问题后自然收束；只有用户要求或论证确有必要时才增加追问。
7. Keep the archival Markdown and the actual text sent to TTS separate. Do not read metadata, URLs, citation brackets, raw footnote markers, or Markdown syntax aloud.

## Hard constraints

- Never overwrite a user source script. Create a new `-TTS-ready.md` file and retain the source.
- Do not call audio synthesis unless the user requests audio.
- In `fidelity` mode, do not call a script complete if key source pages, tables, figures, or footnotes have not been inspected.
- In `fidelity` mode, 存在待复核项时不得标记完成。主题被提到不等于原书内容已覆盖；每个实质单元都必须映射到稿件位置或记录合理的省略原因。
- Treat a large source-to-script length drop as a review trigger, not as proof of failure. When the checker reports `疑似过度压缩`, inspect the unit map and obtain explicit approval before delivering a summary instead of a complete reading script.
- Keep `S` source material, `E` explanatory material, and `X` external extensions distinct in the coverage record. Do not present `E` or `X` as the author’s claim.
- Preserve the user's episode mapping and series voice choice. If there is no series choice, use `mini` only when synthesizing; do not infer a different voice from the subject matter.
- 系列稿交付前，逐对核验第 N 讲结尾和第 N+1 讲开头：前讲的“启下”必须被后讲的“呈上”接住，承诺、结论与事实不得错位。
- Use `--no-rescript` for local synthesis. It prevents the runtime from replacing the reviewed script.

## Local checks

- `scripts/check_tts_ready.py INPUT.md --mode fidelity --coverage COVERAGE.md --source SOURCE.md` checks structure, unresolved coverage and suspicious compression; it can also export the text actually sent to TTS.
- `scripts/preflight.py` checks the local runtime only when audio is requested.
- `scripts/check_audio.py SPOKEN.txt OUTPUT.mp3` checks decodability and reports duration and silence findings.

These tools find structural and delivery risks. They do not prove that an adaptation is faithful; complete the source review described in the relevant reference.
