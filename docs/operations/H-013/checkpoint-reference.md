# Research: LangGraph in-process clarification checkpoint/resume

## Request Type
Implementation reference lookup. Documentation only; not product execution evidence.

## Direct Answer
Retain the compiled graph and its `InMemorySaver` for the session. Start with normal input and a stable application thread identifier; resume a dynamic interrupt with `Command(resume=...)` and the same configuration. Resume restarts the interrupting node, not its suspended Python frame. Put completed provider work in earlier graph nodes and store outputs in graph state; keep the clarification node free of provider calls before its interrupt. This is the documented separate-node pattern, not an exactly-once guarantee for failed external effects. [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

## Official Docs Evidence
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): checkpointer/thread requirements, `Command(resume=...)`, node reentry, JSON-safe interrupt values, stable interrupt ordering, and idempotency guidance. Do not swallow the interrupt exception. Conditional graph edges are preferable to nondeterministic interrupt loops.
- [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers): snapshots occur at super-steps; `get_state(config)` selects latest state unless `checkpoint_id` is supplied. Snapshot configuration contains `thread_id`, `checkpoint_ns`, and `checkpoint_id`; `next`, `tasks`, and `interrupts` support inspection. Ordinary dictionary input starts new work from the entry point; matching `thread_id` alone is not a resume instruction.
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence): `InMemorySaver` stores RAM-only checkpoints, lost on process restart. Keep the saver alive across UI reruns; constructing a new saver loses the old checkpoints.
- [interrupt API](https://reference.langchain.com/python/langgraph/types/interrupt): API reference identifies version 1.2.20 and documents reentry/resume ordering.

## Version Note
Retrieved 2026-11-07. Local package metadata verified `langgraph==1.2.20`, `langgraph-checkpoint==4.3.1`, Python 3.12 environment. Online guides are rolling documentation, not release-pinned snapshots. The reference search result identifies 1.2.20; direct API-page retrieval reported unsupported Markdown content type. Core APIs below were also confirmed by read-only installed-source inspection. No upgrade, dependency installation, or compatibility migration performed.

## Supporting Examples
Illustrative API sketch only; not run or added to application code:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

# builder has a completed provider node preceding this clarification node.
def clarify(state):
    choice = interrupt(state["clarification"])
    return {"choice": choice}  # validate choice before downstream work

saver = InMemorySaver()
graph = builder.compile(checkpointer=saver)
config = {"configurable": {"thread_id": "example-session-run"}}
first = graph.invoke(initial_state, config)
if first.get("__interrupt__"):
    snapshot = graph.get_state(config)
    checkpoint_identity = snapshot.config["configurable"]
    checkpoint_id = checkpoint_identity["checkpoint_id"]
    pending = snapshot.interrupts
    # Application validates session/run/schema, expiry, and pending checkpoint.
    resumed = graph.invoke(Command(resume=validated_choice), config)
```

The example uses latest-state resume, not historical replay. Retain checkpoint identity for evidence and stale-submission checks; passing an older checkpoint to invocation can replay work rather than continue the latest pause. [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

## Source-Reference Evidence
No upstream code citation needed: docs answer the API question. Supplemental local version confirmation only (not a pinned upstream reference): installed `langgraph/types.py` lines 721–747 declare `StateSnapshot`; lines 913–935 describe interrupt reentry. Installed `langgraph/pregel/main.py` lines 1460–1482 select live/latest snapshots when no checkpoint ID is supplied. Installed checkpoint package `memory/__init__.py` lines 34–64 describe RAM storage and test/debug use. Latest `StateSnapshot.interrupts` contains still-pending interrupts; historical snapshots may include interrupts answered later. These locations are version-local and may drift.

## Caveats / Ambiguity Flags
- Application obligations from H-013, not LangGraph defaults: two-pause maximum, 15-minute TTL, session/schema isolation, shared counters and active-time accounting, stale/duplicate resume rejection, and same-run trace continuity. LangGraph waits indefinitely unless the application imposes expiry. [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- A provider side effect committed before a node failure may repeat on retry; checkpoints do not make arbitrary external calls transactional. Keep effect deduplication and attempt accounting explicit. [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- H-013 was read entirely as context; it is not the received child task. No private source copied, credentials loaded, provider/count calls made, runtime/goal/Git state changed, or product tests executed by this lookup.

## Reusable Takeaway
Use a retained saver/compiled graph, dedicated interrupt node, and same-thread `Command(resume=...)`. Prove no repeated prior provider calls with application tests; inspect real checkpoint identity and pending interrupts rather than simulating clarification through fresh graph input. Implementation decisions and acceptance evidence remain with the leader.
