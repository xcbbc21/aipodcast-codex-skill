# Batch production: local synthesis and delivery

Read this reference only when audio is requested.

## Runtime checks

Run `python scripts/preflight.py` from the environment that provides `aipodcast` to confirm the CLI and required flags. To select another environment, pass `--python /path/to/python` or set `AIPODCAST_PYTHON=/path/to/python`. Do not print API-key values.

The local runtime must receive the reviewed plain-text export with `--no-rescript`. Pass the text through a safe argument mechanism; do not build an unquoted shell command from narration text.

Use the series voice already chosen by the user. When there is no established series voice, use `mini`. Keep a series on the same voice unless the user changes that decision.

## Production procedure

1. Run the text check and export the actual spoken text.
2. Run one episode at a time. Do not parallelize a shared API key.
3. Check the resulting file with `check_audio.py` and listen to the opening, ending, long transitions, and any dense number, English, chart, or footnote passage.
4. Correct the TTS-ready text, re-export, and regenerate only the affected episode when a reading or omission is found.

## Production record

For each episode, record the episode ID, source location, source version/hash, script path, plain-text hash, coverage-review state, model, voice setting, language, output path/hash, actual duration, and listening status. Reuse an existing MP3 only when the spoken-text hash and relevant synthesis settings match and prior validation passed.

Do not treat the number of cache files or a basic pitch estimate as proof that every phrase was synthesized or that a voice is consistent. Do not clear the shared cache by default.

## Delivery

For a script-only task, deliver the TTS-ready files, episode index, and coverage records. For an audio task, also deliver the MP3 files and a production-record summary. State unresolved source or listening checks plainly.
