#!/usr/bin/env bash
# Local bootstrap only: no API calls, billing approval or OMX state changes.
set +x
set -euo pipefail
python3 - "$@" <<'PY'
import getpass
import os
from pathlib import Path
import shlex
import stat
import tempfile
import sys

if sys.argv[1:] not in ([], ['--replace']):
    raise SystemExit('Usage: setup-universitydb-key.sh [--replace]')
replace = sys.argv[1:] == ['--replace']

os.umask(0o077)
folder = Path.home() / '.universitydb-secrets'
if folder.is_symlink():
    raise SystemExit('Refusing symlink credential directory.')
folder.mkdir(mode=0o700, exist_ok=True)
info = folder.stat()
if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
    raise SystemExit('Credential directory must belong to the current user.')
folder.chmod(0o700)
target = folder / 'credentials.env'
if target.is_symlink():
    raise SystemExit('Refusing symlink credential file.')
if target.exists() and (not target.is_file() or target.stat().st_uid != os.getuid()):
    raise SystemExit('Existing credential must be a regular file owned by the current user.')
if target.exists() and not replace:
    raise SystemExit('Key file already exists; preserved. Use the existing file or arrange deliberate rotation.')
with open('/dev/tty', 'w') as terminal:
    key = getpass.getpass('OpenAI API key (hidden): ', stream=terminal)
if not key or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in key):
    raise SystemExit('Empty key or whitespace/control characters: nothing saved.')
fd, temporary = tempfile.mkstemp(prefix='.key-', dir=folder)
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as output:
        output.write('export OPENAI_API_KEY=' + shlex.quote(key) + '\n')
        output.flush()
        os.fsync(output.fileno())
    if replace:
        # Old credential stays intact until the new file has been fully written.
        os.replace(temporary, target)
    else:
        os.link(temporary, target)
finally:
    if os.path.exists(temporary):
        os.unlink(temporary)
print('Saved ~/.universitydb-secrets/credentials.env (0600); directory 0700.')
print('No API call made. Access not verified; spending not approved.')
PY
