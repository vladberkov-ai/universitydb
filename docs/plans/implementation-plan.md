# План будущей реализации — proposed, без execution handoff

Цель: компактный работающий и объяснимый demonstrator по [матрице](requirements-test-matrix.md), не production service. Нынешний B заканчивается возвратом в чат. Приняты scope/simple screen/dependent scenario/second schema; domain semantics, stack и eval gate лишь рекомендации. A не повторять. Данный документ не разрешает установку, paid calls, создание remote или push.

## Последовательность после отдельного принятия/поручения
| Этап | Dependencies / ресурсы | Deliverables и verification | Commit/manual gate |
|---|---|---|---|
| I0 Зафиксировать решения и бюджет | chat review этого bundle/ADR003–007 | принятые/изменённые semantics, model, eval cap, deadline; presence-only key availability; versions/advisory audit/lock candidate compatibility | отдельный docs decision commit; stop без разрешения live/budget |
| I1 Первый настоящий vertical slice | I0; будущие src/universitydb/{db,agent,llm,tracing,ui}, resources/schema+seed, prompts/; F1 | минимальный реальный LangGraph question S6→Responses→validated SQLite→80.00→JSONL→Streamlit с доступными SQL/bindings/typed DB rows/full same-run trace+attempts; smoke trace+actual prompts; read-only/timeout boundaries до первого generated SQL | small feat+tests commit, owner walkthrough success/SQL guard; не сначала большой каталог abstractions |
| I2 Семантика, запросы и failure paths | I1; schema/domain adapter/contracts | полный F1, S1–S14 oracle DB tests; D1–D3 двухфазные refs, V1–V2 domain result spec/units, W1–W3 bounds; C1–C4 checkpoint/resume; E1–E7 bounded faults; contract unit tests; incremental small commits | targeted tests сначала, compile/lint/typecheck после; chat review average/ties/retakes/clarification |
| I3 Зависимость и переносимость | I2; graph plan/results, library adapter/F1L | M1 F1/F2+tie sensitivity; L1 unchanged core hash, mocked and actual DB tests; traces completeness/redaction | feat portability commit; owner predicts mutation without agent |
| I4 Live eval и full screen E2E | I3, credentials, explicit spending cap; versioned datasets/prompts | development then sealed heldout 48 counted runs; category coverage, all attempts/cost; manual live S6/M1/C1/L1+UI1, отдельно offline injected EI1–EI3 с provenance (не live score); no hidden fallback | eval evidence commit; failures→defect+new version+rerun, не снижение порога |
| I5 Packaging/clean clone/defense | I4 pass; docs/examples/traces/prompt coverage, README | clean install offline suites and approved live smoke; independent manual explanation; public-safe checklist; unresolved requirements remain open | local release docs commit, затем отдельное remote/push authorization; verify remote SHA+anonymous access до R15 closure |

При каждом code step: inspect diff→targeted regression→all offline tests→compile/lint/typecheck available selected tools→explicit staged paths→diff --check→commit→SHA receipt. No blanket staging, no amend/reset foreign changes. Тесты должны существовать до semantic fixes. Prompt changes versioned вместе с regression и eval evidence. Будущие команды определены в test-plan; exact entrypoints подтверждаются при создании кода, не выдаются сейчас за существующие. Future dependencies допускаются только новым implementation поручением; B не установка.

## Минимальные блокеры и вопросы владельцу
1. Принять предлагаемые grade hundredths/0..100/NULL, all-retakes, equal enrollment weights, all ties? Рекомендуем да для объяснимой арифметики; credit/latest-only требуют иных fixtures.
2. Принять all-semesters default с явной подписью и уточнение «текущий»? Рекомендуем без скрытой текущей даты.
3. Принять SQLite+direct LangGraph+Streamlit+local trace, InMemorySaver и отсутствие resume после рестарта? Рекомендуем да для локальной демонстрации; SQLite checkpointer отдельная будущая зависимость при restart requirement.
4. Принять Luna profile и cap $2 для предложенного development+heldout плана? Ключ отсутствует в текущем env, аккаунтная availability неизвестна. Без разрешения/credentials live остановлен, offline progress можно отдельно поручить.
5. Принять strict 48/48 small-suite gate (не population claim), manual обязательства отдельно? Если нет — согласовать до результатов, не задним числом.
6. Точное время сдачи, допустимый public комплект, GitHub owner/remote? Не выдумывать. Public publication и paid calls требуют отдельных полномочий.

## Handoff и stop
Лидер B: после real sequential reviews и supported terminal closeout упаковывает safe copies, сохраняет provenance/review hashes/actual prompt coverage, doc checks, отдельный docs commit B и отчёт. Только затем пользователь обсуждает proposed решения. Executor не запускается по этому плану автоматически. Будущая реализация завершается только при evidence всей матрицы; если public/credentials/owner rehearsal отсутствуют — отчёт partial с конкретным blocker, не «готово». Нынешний review не тестирование продукта.
