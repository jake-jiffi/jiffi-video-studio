# Public video skill repository

This repository is the distributable skill and tooling, not a production studio.
Keep generated media, account logs, credentials and private projects outside it.
Preserve the common skill under `skills/jiffi-video-studio`; host manifests must
reference the same files. Do not add a hidden paid call to setup or tests.

Use Australian English. Before release, run Python tests, the Node audio-review
tests, `scripts/check_package.py`, and host manifest validation where available.
Document actual compatibility evidence and untested integrations honestly.
