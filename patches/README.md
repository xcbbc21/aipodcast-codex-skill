# Patches

本目录保存针对 `minimax_aipodcast` 本地代码包的修复补丁。
本 skill 不直接打包底层 TTS 代码（它属于 `mm-demo-collection/minimax_aipodcast`），
所以修复以 unified diff 形式提供，使用者需要手动 `patch -p1` 到自己的本地副本。

## 应用补丁

```bash
cd /path/to/minimax_aipodcast
patch -p1 --dry-run < /path/to/aipodcast-codex-skill/patches/<patch-name>.patch
patch -p1 < /path/to/aipodcast-codex-skill/patches/<patch-name>.patch
```

`--dry-run` 先验证能否干净 apply（没有偏移），再正式 patch。

## 补丁清单

### `tts_synthesizer_2056_failfast.patch`

修复 `aipodcast/tts_synthesizer.py` 的 `_tts_one()` 函数无法识别 MiniMax API
quota 硬错误（status_code 2056/2057）的问题。

**症状**：账户 Token Plan 配额耗尽时，客户端按 30-45 秒指数退避重试 5 次
（合计约 93 秒），仍在死循环等永远不会通过的请求；进程看起来"在跑"
但 cache 数量不变、CPU 0%、WCHAN 阻塞，用户需等十几分钟才发现是 quota 问题。

**修复**：在 `_tts_one()` 识别到 `status_code in (2056, 2057)` 时
立即 `raise TTSError(...)`，不再重试。实测从 93 秒降到 0.06 秒。

**测试**：跑 08 讲时实测触发。修复后用 monkey-patch 模拟 2056 响应，
0.06 秒即 raise，正常流程未受影响（preflight + 真实 cache 命中调用通过）。