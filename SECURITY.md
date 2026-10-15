# Security and data handling

This repository contains instructions, templates and local utilities. Installing it does not start services, install hooks, read account credentials or submit generation jobs.

- `studio.py init` writes local policy/templates without replacing existing files.
- `studio.py doctor` checks local prerequisites. Only `--online` enables read-only Higgsfield account/workspace/model queries. Their response bodies are not printed or saved by the doctor.
- `studio.py smoke` and the tests use synthetic local media. The Node test suite mocks the API.
- `verify_project.py` reads the selected studio and invokes local FFmpeg/ffprobe.
- `gemini-review.mjs` sends the explicitly selected media and prompt to Google's Gemini API when run without `--dry-run`. It uses an environment-provided key, writes a local evidence record and never automatically retries an uncertain request.
- The agent may use Higgsfield or another explicitly approved production route. Each upload and paid submission must remain within the user's project permissions and budget.

Keep studios outside this repository. Do not commit `.env` files, keys, browser profiles, job/account logs, private media, commercial fonts or client files. The release ZIP is built only from tracked public-package files. `.gitignore` is a backstop, not a security scan of existing Git history.

The repository's MIT licence covers its own code and writing. It does not grant rights to external software, brand assets, third-party music or generated output.

For a security issue, use GitHub private vulnerability reporting if enabled. Otherwise contact the maintainer privately before posting sensitive details. Public issues are appropriate for non-sensitive bugs; do not attach credentials or confidential media.
