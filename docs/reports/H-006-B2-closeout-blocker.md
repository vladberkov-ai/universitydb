# H-006 B2 — реальные reviews завершены, post-closeout blocker

Дата: 2026-11-07. Итог: **blocker; B не завершён, коммит B отсутствует**.
Это новая попытка после ремонта OMX, не продолжение отменённого поколения.
Основание: H-006-v5 и отдельный прямой пользовательский вызов Advisory;
[свежая диагностика D2](H-006-v5-readiness-2.md) использована, A не повторялся.

## Git и сохранность

- A/HEAD: `8931d832d49311ac0d63c3a7a359b4293058da89`, ветка `main`, правильный Git root.
- Все **97** файлов pre-B baseline, включая исходные незакоммиченные документы и D2, сохранили SHA-256.
  Ещё **9** исторических private research/evidence файлов и **2** файла отменённого поколения неизменны.
- Все **25** входов Obsidian совпадают с актуальными hashes при начале B. Старые frozen-manifest
  расхождения по пяти обновлённым материалам уже объяснены D2/CHAT-022, это не новые изменения.
  PDF прочитан непосредственно; Obsidian не изменялся.
- Индекс Git неизменен, staging пуст, remotes отсутствуют. Нет commit B, push или публикации.
  Новые файлы — только диагностические документы; существующие индексы docs/AGENTS/wiki не менялись.
- Подробные hashes и команды: [preservation-and-validation.json](../operations/H-006-B2-closeout-blocker-evidence-2/preservation-and-validation.json).

## Активация и настоящие роли

Прямой native hook активировал `workflow_variant=advisory`:

- generation: `ec3e1f0b-d751-4088-bfb2-ec386c08549c`;
- OMX session: `omx-1794046506930-56sf8c`;
- native root: `01a1b581-446d-70b0-84ac-3e5b449c1437`;
- native activation turn: `01a1b58c-206e-7472-bebe-165fab7636bc`.

Отменённое `0748daa2-4c89-4a84-a305-486ed1f480a3` не возобновлялось.
Codex 0.162.1, OMX 0.21.46 с локальным ремонтом, Node 22.23.2; обновлений/setup/repair не выполнялось.
Native `agent_type` использован для установленных `planner`, `architect`, `critic`; модели не навязывались.

| Итерация | Planner | Отдельный Architect | Отдельный Critic |
|---|---|---|---|
| 1 | Draft завершён | ITERATE | ITERATE: текущая редакция отклонена |
| 2 | Revision завершена | ITERATE | ITERATE |
| 3 | Revision завершена | APPROVE, 0 blocking | APPROVE, 0 blocking |

Planner переиспользован для трёх итераций, reviewers — шесть отдельных native children, строго
Architect→Critic последовательно. Для **7/7** детей проверены настоящие native parent/root/role/generation
и `completion_source=native_stop_event`; поздние notify не потеряли completion в tracker.
Это локальная lifecycle evidence, не host-issued authority. Дополнительные настроенные gates: **[]**,
проверены после Critic; фиктивных gate verdicts нет.

Исправлены: различие статического DAG и runtime bindings, конечный типизированный ResultSpec,
точная агрегатная семантика/ничьи, отделение injected faults от real-model оценки, полный SQL/DB/trace
в UI, различие no_rows/no_grades/real_zero и COALESCE вне SUM для пустого входа.
Старые researcher/dependency-expert результаты прочитаны и переиспользованы как исторические входы,
их exports/hashes проверены; они не выданы за новые исследования/reviewer approvals.
Новых research-пробелов, требующих дополнительных агентов, не обнаружено.

[Native completions](../operations/H-006-B2-closeout-blocker-evidence-2/native-role-completions.json),
[точные review-проекции](../operations/H-006-B2-closeout-blocker-evidence-2/review-evidence.json).

## Что подготовлено, но не упаковано как завершённая архитектура

Финальные **proposed** документы остаются в `.omx/plans/H-006-B2/iteration-3/`:
`architecture-proposal.md`, `contracts.md`, `test-plan.md`, `requirements-test-matrix.md`,
`implementation-plan.md`, `production-considerations.md`, ADR-OMX-003…007, additions/changelogs.
Полный bundle: `.omx/plans/H-006-B2/iteration-3/plan-bundle.md`.
Raw SHA-256: `e4d91f3e04113d4f973bb4e578c98a243040c7d05f725f164c6b11a62ece53b8`.
Manifest SHA-256: `f903b9ca80b4fb74f4f17c04ae8b69004abccd879dd065dcd53e1c9cebf891d8`.
Проверены все manifest entries трёх неизменённых редакций: **13/14/15**, без несовпадений.
Reviews: `.omx/plans/H-006-B2/reviews/iteration-{1,2,3}-{architect,critic}.md`.
Raw SHA-256 и domain-separated official Advisory digests — разные алгоритмы представления;
это не повреждение файлов.

Рекомендации (не принятые решения): SQLite/direct LangGraph/OpenAI SDK/Streamlit/local JSONL;
целочисленные сотые оценок, отдельный NULL, все пересдачи, равные веса enrollment, точные ничьи;
ограниченный граф, конечный реестр результатов и второй Library-адаптер без изменения ядра.
Версии/provider/model/budget — кандидаты, не установленный и не live-проверенный стек.
Все новые ADR остаются **proposed до обсуждения в чате**.

## Штатное закрытие и новое противоречие

Команда выполнена **один раз**, через поддержанное разрешение host:

```text
/home/dev/.omx/runtime/bin/omx ralplan advisory complete --json
exit=0
{"ok":true,"status":"closed","host_verified":false,"consensus_gate_complete":false,"execution_handoff_authorized":false,"return_to_caller":true}
```

Штатный append-event reader показывает `closed`, journal `committed`, `approved+proven`,
`corruption:null`. Mode `active:false/current_phase:complete`, run `active:false`;
review lifecycle `complete:true/sequence_valid:true/iteration:3`.
Evidence bundle digest: `57ddd777824da540443657e5f843e8fbd292ef1a528c7112080cd809e7ba5a90`.
Host verification, consensus gate и execution handoff явно **false** — для standalone Advisory это ожидаемо.

**Но после обычных следующих tool calls session `skill-active-state.json` снова содержит
`active:true`, `phase:reviewing`, то же поколение/root/turn и сохранённый `completed_at`.**
Journal назначил ему `active:false`, а `updated_at` уже позднее closeout.
`omx status` одновременно показывает `ralplan: inactive (phase: complete)` и `skill-active: ACTIVE`.
Это post-closeout несовместимость, а не отсутствие reviewer approvals.

Raw base `fence.json` остаётся `pending_closeout` намеренно: append-only `fence-event-0001.json`
задаёт закрытую effective projection. Первая проверка ошибочно потребовала terminal от raw base
и получила AssertionError; правильный официальный reader подтвердил закрытие без повторного complete.

[Команда](../operations/H-006-B2-closeout-blocker-evidence-2/closeout-command.json),
[terminal/current snapshots](../operations/H-006-B2-closeout-blocker-evidence-2/terminal-projections.json),
[status](../operations/H-006-B2-closeout-blocker-evidence-2/status-command.json).

Гипотеза по установленному коду: notify→`syncSkillStateFromTurn` заново выводит фазу из текста
assistant и присваивает active, не проверяя terminal Ralplan в этой функции. Точный triggering payload
не трассировался, поэтому причинность не объявляется доказанной.
Следующий ограниченный тест для сопровождающего интеграцию: isolated fixture с terminal Advisory
и late authorized notify; все mode/run/session-skill должны остаться inactive.
[Фрагменты кода и ограничения вывода](../operations/H-006-B2-closeout-blocker-evidence-2/source-guided-hypothesis.json).
В этом workspace тест/ремонт/replay не запускались.

## Prompt coverage, проверки и остановка

- [Actual task + received-task projections](../ai/omx/H-006-B2-blocker-actual-prompts-2.json),
  [coverage/cutoffs](../ai/omx/H-006-B2-blocker-prompt-coverage-2.json): все 7 запущенных детей,
  три хода Planner, actual пользовательский B prompt. Private exports сохранены, skipped records=0.
- Root actual prompt извлечён из native transcript и hash совпадает с activation. Child assignments
  сохранены как self-projections фактически полученного текста; parent tool arguments зашифрованы,
  plaintext byte equality с ciphertext не заявляется. System/developer/reasoning и полный inherited
  контекст не публикуются. Private vault/repair-output paths redacted; полные transcripts не экспортированы в docs.
- JSON/links/privacy/preservation checks: [финальная проверка](../operations/H-006-B2-closeout-blocker-evidence-2/document-checks.json).
  Первая сборка диагностического экспорта остановилась на старой форме iteration1 observation;
  её частичные unsuffixed outputs сохранены и помечены incomplete. Канонический полный набор — suffix `-2`.
- Продуктовые tests/evals **not-run**: приложения/schema/seed нет. Изолированные schema-free
  SQLite `:memory:` SELECT probes Architect2/Critic2 и документальные расчёты не являются
  product tests, доказательством DB integration или real-model E2E.
- Credentials проверялись только на наличие: OPENAI_API_KEY отсутствовал. Значения не сохранялись.
  Доступ к аккаунту/модели, бюджет, совместимость зависимостей, public delivery, defense и production
  не доказаны. R-15 открыт; остальные будущие acceptance evidence не подменены планом.

**По stop-правилу пользователя упаковка устойчивой архитектуры в docs/ и commit B не начаты.**
Нет повторных запусков, повторного closeout, ручной правки IDs/tracker/state, отмены закрытого поколения
или execution authorization/handoff. Исходные материалы, research и approved private design сохранены.
После отчёта — остановка для отдельного обращения пользователя.
