# Actual offline M1 dependency evidence

`manifest.json` identifies the source tree and each full same-run JSONL. The three
proof documents record independent frozen expected values, actual typed steps,
provider payloads containing actual materialized refs, checked SQL bindings and
answers. F1 selects course2/student1; F2 changes the actual upstream data to select
course1/students1,2,3; exact tie selects courses1,2 and the deduplicated union.
Nothing here measures real-model NL-to-SQL accuracy: the transport is explicitly
offline/injected and builds SQL from the actual received step/scope/ref payload.

Reproduce on a source-frozen candidate with no concurrent heavy test/browser run:

```bash
env -u OPENAI_API_KEY UNIVERSITYDB_LIVE_APPROVED=no LANGSMITH_TRACING=false \
  LANGCHAIN_TRACING_V2=false UV_CACHE_DIR=/tmp/h013-uv-cache \
  uv run --locked pytest -q tests/test_i3_dependencies.py \
  --basetemp=/tmp/h013-m1-candidate
# After reading the successful result, record its actual command/result:
.venv/bin/python docs/operations/H-013/m1/capture.py /tmp/h013-m1-candidate \
  --verification '<actual passing command/result>' \
  --output-dir docs/operations/H-013/m1-new-candidate
```

`capture.py` only copies known proof/trace files after verifying hashes; it does
not run SQL/provider calls or access credentials/ledger/runtime/native/Git state.
Capture while source remains frozen so the recorded source hashes describe the
code actually loaded by the test process. A later source change requires fresh
proof; do not merely rewrite old evidence hashes. Use a fresh temporary path or
explicitly owned temporary fixture directory, never the real spending ledger.

The capture destination must not already exist; earlier proof is never overwritten.
Use a separately named candidate directory for final evidence after source changes.
