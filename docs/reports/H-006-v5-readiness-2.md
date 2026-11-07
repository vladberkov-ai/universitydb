# H-006-v5 D2 — готовность после локального ремонта OMX

Дата: 2026-11-07T10:22:48.750545+00:00. Режим: solo diagnostics. **ready-for-direct-invocation**, не выполненный B.

- Git root `/home/dev/projects/universitydb`, `main`, HEAD `8931d832d49311ac0d63c3a7a359b4293058da89`. A не повторялся. Staging пуст, remotes нет; рабочее дерево исходно dirty.
- Все **78/78** исходных файлов ремонтного baseline, включая research/blocker/evidence, неизменны. Семь обязательных SHA-256 сохранены; Git index совпадает с ремонтным baseline. Старые документы и Obsidian не менялись.
- Codex **0.162.1**, OMX **0.21.46 + local compatibility patch**, Node **22.23.2**. Repo launcher и `/home/dev/.omx/runtime/bin/omx` идентичны и указывают на проверенный установленный runtime.
- В sandbox doctor: **17/0/3**, `spawnSync EPERM`, PID не виден, `stale-dead/bad_selectors=CODEX_SESSION_ID`. Штатная разрешённая read-only проверка host: **20/0/0**; binding `session-authority/usable`, тот же owner PID и identity проверены. Это различие контекстов, не текущий ID mismatch. Ни selectors, ни pointer/tracker не исправлялись.
- Native hooks **9/9** зарегистрированы, включены и имеют совпадающие trust hashes, включая `UserPromptSubmit`, `SubagentStart`, `SubagentStop`. Actual D triage доставлен; встроенный минимальный doctor smoke успешен. `hooks status` отдельно показывает 0 plugins и не заменяет native checks.
- Planner, Architect, Critic, researcher, dependency-expert: TOML установлены/валидны; роли присутствуют в текущей native `agent_type` schema. **Никто не запускался в D**. Adapted-authority preflight неприменим.
- Local ralplan/plan прочитаны. Дополнительные quality gates: `[]`; обязательные последовательные reviewers этим не отменяются.
- Новый Ralplan state отсутствует — нормально до прямого вызова. Старое поколение `0748daa2-4c89-4a84-a305-486ed1f480a3` cancelled/abandoned, не возобновлялось. Current tracker leader совпадает с native ID нового pointer.

## Ограничения и наблюдения

Из 8 installed-manifest hashes совпали 7; единственное семантическое дополнение config после ремонта — `service_tier=fast`; hooks/trust не изменены. Замороженный vault manifest совпал 20/25: пять status/workflow/index/review/question страниц содержат последующий CHAT-022 о research и отмене. Их текущие hashes сохранены; требования/контракт/PDF без drift. Старый next-step в этих страницах исторический относительно текущего прямого поручения о ремонте. Полное предметное чтение/PDF отложено до B.

Новая Advisory activation, реальные reviewers и весь closeout после ремонта **ещё не проверены**. Успех doctor не доказывает весь lifecycle. После отдельного прямого вызова в этой же ведущей сессии нужно подтвердить новый advisory variant/generation/session/root/turn до Planner. IDs вручную не назначать. Права на будущий B commit не проверялись записью.

## Артефакты и граница

- [Структурированная диагностика](../operations/H-006-v5-readiness-2.json).
- [Baseline и исходные SHA-256](../operations/H-006-v5-readiness-2-evidence/baseline.json).
- [Host binding/hooks/roles](../operations/H-006-v5-readiness-2-evidence/host-binding-hooks-roles.json), [host doctor](../operations/H-006-v5-readiness-2-evidence/host-doctor-command.json), [sandbox commands](../operations/H-006-v5-readiness-2-evidence/commands.json).
- [Actual prompt](../ai/omx/H-006-v5-D2-actual-prompt.txt), [coverage/redactions](../ai/omx/H-006-v5-D2-prompt-coverage.json).

Сохранено локально, **не закоммичено**, не pushed/public. Setup/update/repair, активация, субагенты, проектирование, приложение и paid/live calls не выполнялись. Продуктовые тесты not-run: D не создаёт приложения. Блокеров для прямого вызова не выявлено; диагностические ограничения выше сохранены. **Остановка до отдельного прямого вызова.**
