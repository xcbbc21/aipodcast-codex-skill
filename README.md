# aipodcast

面向中文书籍、报告、文章和已审定脚本的 Codex 单人口播技能。它把资料整理成可审计、可直接交给 TTS 的口播稿；重点处理原文覆盖、章节衔接、数字与英文读法、图表、脚注以及自然收束等问题。

当前版本：[`v1.2.0`](https://github.com/xcbbc21/aipodcast-codex-skill/releases/tag/v1.2.0)

> 这个技能用于单人口播，不用于双人对谈播客。只有用户明确要求生成音频时，才会进入语音合成流程。

## 适用场景

- 按原书顺序制作“精读”或“完整覆盖”的系列口播稿。
- 把已经定稿的文章、讲稿整理为自然、稳定的 TTS 文本。
- 在明确标注边界的前提下，对资料进行扩写、评论或故事化改编。
- 处理含图表、脚注、引文、数字、英文缩写和多讲连续结构的复杂资料。

## 三种工作模式

| 模式 | 适合的请求 | 核心要求 |
| --- | --- | --- |
| `fidelity` | “按原书”“精读”“完整覆盖”“核对资料” | 建立逐讲覆盖表，拆分最小语义单元，完成双向语义复核；未核验的内容不能标记为完成 |
| `authored` | “这是定稿，转成口播或 MP3” | 保留原稿事实与结构，重点做口语化、读法和 TTS 清理，不擅自重写观点 |
| `adaptation` | “扩写、评论、故事化、加入观点” | 区分原始材料、解释性补充和外部扩展，不把新增观点冒充作者原意 |

## 核心方法

1. 先确认资料范围、分讲边界和交付物是规划、口播稿还是音频。
2. `fidelity` 模式先拆分定义、主张、推理、例证、数据、反例、限定、图表和有效脚注，再建立逐讲覆盖表。
3. 每讲长度由原文的信息密度决定，不套固定字数、句数或时长。
4. 连续系列从第二讲开始简短回顾上一讲，并说明上一讲的结论如何引出本讲；第一讲只承担章节总起。
5. 每讲先回答中心问题，再自然收束。默认只保留一个真正值得思考的问题，避免机械地连问三个问题后突然结束。
6. 存档 Markdown 与实际送入 TTS 的纯文本分开，元数据、链接、引文标记、脚注符号和 Markdown 语法不进入朗读文本。

## 纯音频中的图表处理

听众看不到图，因此口播稿默认不朗读图号，也不使用“见图”“如下图”“图一之五”等视觉导航：

- 图表只是重复正文：核验后不在口播中单独提及。
- 图表包含正文没有的独有信息：把趋势、比较关系、关键数值、异常点和结论改写为自然语言，但不报图号、坐标位置或图例位置。
- 图表无法可靠辨认：记录为待复核项，不猜测，也不能把该讲标记为完成。
- 只有用户明确要求同步视频、配套画面或可视阅读时，才允许保留必要的视觉指引，并在检查时显式开启相应选项。

图号、坐标、图例和来源可以保留在覆盖表或书面档案中，用于制作核验，但不会直接送入 TTS。

## 安装与更新

使用已登录 GitHub 的 `gh` CLI 安装：

```bash
gh repo clone xcbbc21/aipodcast-codex-skill ~/.codex/skills/aipodcast
```

已经安装时，在技能目录中更新：

```bash
git -C ~/.codex/skills/aipodcast pull --ff-only
```

安装或更新后，重新打开 Codex 会话即可让新会话读取最新版技能说明。

## 在 Codex 中使用

直接在请求中点名 `aipodcast`，并说明资料、范围、模式和交付目标。例如：

```text
请用 aipodcast 的 fidelity 模式，把这本书第一章按原书完整覆盖，制作成连续的单人口播稿。先建立逐讲覆盖表，不生成音频。
```

```text
请用 aipodcast 把这份已定稿讲稿整理成 TTS-ready 版本。保留事实和段落顺序，处理数字、英文和脚注，不要扩写观点。
```

若要求音频，还应明确声音、格式和是否允许同步画面；未明确要求音频时，技能只交付文本。

## 本地检查

检查一份精读稿、覆盖表和原始文本：

```bash
python3 scripts/check_tts_ready.py INPUT.md \
  --mode fidelity \
  --coverage COVERAGE.md \
  --source SOURCE.md
```

导出实际送入 TTS 的纯文本：

```bash
python3 scripts/check_tts_ready.py INPUT.md \
  --mode authored \
  --export-spoken SPOKEN.txt
```

只有听众确实能看到同步画面时，才使用 `--allow-visual-references`。

运行仓库测试：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tests/test_skill_contract.py SKILL.md
```

这些检查能发现结构、覆盖状态、视觉引用和疑似过度压缩等风险，但不能代替人工语义核对，也不能单独证明改编忠实。

## 目录结构

```text
aipodcast/
├── SKILL.md                       # Codex 技能入口与硬性规则
├── README.md                      # 项目说明与使用入口
├── CHANGELOG.md                   # 版本更新记录
├── references/
│   ├── fidelity-mode.md           # 原书精读与完整覆盖流程
│   ├── narration-design.md        # 分讲、承上启下与结尾设计
│   ├── spoken-text.md             # TTS 文本、数字、英文、脚注和图表规则
│   └── batch-production.md        # 用户要求音频时才读取的批量制作说明
├── scripts/
│   ├── check_tts_ready.py         # 文稿与覆盖状态检查
│   ├── preflight.py               # 音频运行环境预检
│   └── check_audio.py             # 音频可解码性、时长和静音检查
└── tests/                          # 自动化测试与技能契约检查
```

## 重要边界

- 不覆盖用户原稿；重构稿另存为 `-TTS-ready.md`。
- 不在用户没有要求时调用语音合成。
- `fidelity` 模式存在待复核项时，不得宣称已经完整覆盖。
- 外部补充必须与作者原意明确区分。
- 原文到口播稿篇幅显著缩短时，只能触发复核，不能仅凭长度直接判定成功或失败。
- 本地合成应使用 `--no-rescript`，避免运行时替换已经审核的稿件。

## 版本与更新记录

- 当前稳定版本：[`v1.2.0`](https://github.com/xcbbc21/aipodcast-codex-skill/releases/tag/v1.2.0)
- 完整更新记录：[CHANGELOG.md](CHANGELOG.md)
- GitHub 仓库：[xcbbc21/aipodcast-codex-skill](https://github.com/xcbbc21/aipodcast-codex-skill)

