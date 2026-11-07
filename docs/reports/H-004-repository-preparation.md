# H-004 v2 — отчёт подготовки

Дата: 2026-11-07, Asia/Jerusalem. Owner: repo. Режим: **solo/direct**, `understand → execute → verify → report` по локальным инструкциям OMX. Итог: **подготовительные документы сохранены; Git-часть заблокирована; этап не объявлен полностью завершённым**.

## 1. Граница и входы

Прочитан только действующий H-004 v2, SHA-256 `69d0fc4b467f4272504d9e6366ee25c5e53607bef30e92975a8fde320ea9335b` (наблюдаемый хеш; независимого ожидаемого хеша самого пакета не передано). Все **25/25** SHA-256 из таблицы совпали. Полный перечень путей/размеров/expected/actual — [input-verification.json](../operations/input-verification.json). Все перечисленные текстовые входы прочитаны полностью. Исходный PDF прочитан целиком: **4 страницы**, все текстовые glyph IDs разрешены через встроенные ToUnicode CMaps. `pdfinfo`/`pdftotext` и библиотеки Python PDF отсутствуют; использовано прямое чтение объектов/Flate streams оригинального PDF без установки зависимостей и без экспорта его текста. Матрица R/U сверена с оригиналом.

H-004 v1 не открывался и не использовался; старые H-001/H-003 не исполнялись. Исторические ссылки в индексах не приняты как действующие поручения. Дополнительно прочитаны последние события журнала, локальные/установленные AGENTS, инструкции прежнего кандидата и установленный wiki skill. Входы/Obsidian/manifest/старые материалы не изменялись. Полная история чатов и hiring context не загружались.

Архитектура приложения, схема/seed, граф, код, UI, runtime prompts, продуктовые тесты и зависимости не создавались; приложение/live или платные eval не запускались. Workers, Team и native subagents не запускались.

## 2. Размещение и canonical evidence

Выбранный **canonical target / рабочая папка**: `/home/dev/projects/universitydb`, `pwd` и `realpath` совпали. `WSL_DISTRO_NAME=UbuntuD`; `/etc/os-release`: Ubuntu 24.04.1 LTS. Соответствующий путь на D: для Linux repo не придумывается. **Инициализированный canonical Git repo пока не доказан и не создан.**

Исходно в рабочей папке: runtime `.omx/` и пустые защищённые `.git`, `.agents`, `.codex`, `.aws`; проектного AGENTS/docs/приложения не было. `.git`: `dr-xr-xr-x`, отдельный `tmpfs`, mount option `ro`, mode `555`. `git rev-parse --show-toplevel`, `git status --short --branch`, `git worktree list --porcelain`, `git remote -v` возвращали **fatal: not a git repository**. Исходные branch/HEAD/status: unavailable, не «чистый repo».

Проверены предпочтительный Linux путь, проектные имена в `/home/dev/projects` и на глубине до 3 в каталоге прежних кандидатов, метаданные старого Genpact, а также относящиеся к проекту OMX pointers. Genpact содержит AGENTS и частные bootstrap/tmp/backup материалы; `.git`/`.gitmodules` не найдены, Git root отсутствует. Ничего оттуда не перенесено. Выявленный кандидат с именем Codevalue проверен **только по Git metadata/именам**: unborn `main`, без commits/remotes, три untracked частных интервью-материала; их содержимое не читалось. Это не доказанная копия UniversityDB; материалы не тронуты. Другие найденные Git-каталоги по именам посторонние; их содержимое не читалось.

OMX session metadata указывает на текущую рабочую папку. Это диагностическое свидетельство размещения, **не полномочие** менять runtime или защищённые mount points. Относящейся к UniversityDB конкурирующей repo-копии в проверенных путях не выявлено; глобальное отсутствие копий на всех дисках не заявляется. Поэтому независимые документы подготовлены здесь, но Git-зависимые действия остановлены. Второй repo, отдельный git-dir, перенос чужих файлов, обход sandbox, chmod/unmount не выполнялись.

## 3. OMX / среда

- Фактический launcher: repo-local `.omx/runtime/bin/omx` (не прежний предположенный launcher). Версия **0.21.46**, Node **22.23.2**, Linux x64; обновления/setup не выполнялись.
- `omx doctor`: **17 passed, 0 warnings, 3 failed**. Failures: запуск Codex CLI из диагностики — EPERM; native-hook smoke — EPERM/ETIMEDOUT в двух наблюдениях; state/session binding — stale-dead и bad selector `CODEX_SESSION_ID`. Это не полностью здоровая среда; не скрывать за успехом team doctor.
- `omx doctor --team`: all team checks passed; работников не запускали, это не проверка приложения.
- `omx status`: перечисленные runtime modes inactive. `omx session lock inspect --cwd ... --json`: lock absent, `safeToRecover=false`; recovery не выполнялся. Не менялись чужие/неподтверждённые session selectors/state.
- Несмотря на diagnostic failures, обычные `omx --version`, help, status и точный session export фактически работали. Поэтому использование OMX не имитировано; недоступные capabilities не задействованы.
- Git identity обнаружена через `git var GIT_AUTHOR_IDENT` без публикации её значения; global config не менялся. Commit блокирует не identity, а read-only `.git`.

## 4. Сохранённые артефакты и diff summary

Новые локальные файлы, не Git diff существующего repo:

- `AGENTS.md`, `.gitignore`: границы, ownership, защита private/runtime/секретов/venv/кешей/бинарных БД.
- **Ровно четыре** безопасных проекции: [requirements](../chat/requirements.md), [acceptance-contract](../chat/planning/acceptance-contract.md), [ADR-CHAT-001](../chat/decisions/ADR-CHAT-001-memory-ownership.md), [ADR-CHAT-002](../chat/decisions/ADR-CHAT-002-result-scope.md).
- [chat-export-receipt.json](../operations/chat-export-receipt.json): vault-relative source paths, hashes фактических source/destination bytes, redactions, ссылки. Vault manifest не обновлён. ADR-CHAT-003/PDF/raw/brief/вложенные зависимости не экспортированы.
- [Prompt index](../ai/README.md), actual prompt, selected OMX export, prompt receipt и хеши instruction context в `docs/ai/omx/`.
- [Единый индекс ADR](../adr/README.md), [ADR-OMX-001](../adr/ADR-OMX-001-preparation-boundary.md): только подготовительный выбор, альтернативы/причины/последствия/проверки, без архитектуры приложения.
- [Git checkpoints](../operations/git-checkpoints.md): текущий conditional docs-коммит разрешён H-004 v2; будущая политика **proposed**, не автоматически accepted.
- [omx_wiki/index.md](../../omx_wiki/index.md), собственная session memory OMX и созданный `omx wiki` журнал lint; ссылки на repo-owned документы, не копия Obsidian.
- Этот отчёт, [input evidence](../operations/input-verification.json), [validation manifest](../operations/preparation-validation.json) и [command evidence](../operations/environment-checks.json).

Приватный вспомогательный build/validation script и исходный session export остаются в ignored `.omx/preparation/`, не входят в публичный состав. `.git` и прочие защищённые каталоги не изменены. Точный состав и итоговые hashes public-safe файлов фиксирует validation manifest; сам manifest исключён из собственного hash-набора во избежание самоссылки.

## 5. Команды и проверки

Фактически выполнены: чтение через `cat`/Python, SHA-256 через `hashlib`, bounded `find` только имён/metadata, `pwd`/`realpath`/`stat`/`findmnt`, Git metadata probes, `omx --version`, `omx --help`, `omx session --help`, `omx session export --help`, `omx doctor`, `omx doctor --team`, `omx status`, `omx session lock inspect`, реальный JSON session export. Детали повторных Git/diff/no-index проверок и exit codes — в command evidence/validation manifest; результаты должны читаться вместе с ограничениями ниже.

| Проверка | Результат |
|---|---|
| Пакет и все обязательные входы | Прочитаны; 25/25 hashes match; PDF p1–4 |
| Исходная Wiki structural lint | `PYTHONDONTWRITEBYTECODE=1 python3 <private-vault>/scripts/lint_wiki.py`: **0 errors**, без записи в vault |
| Источники после подготовки | Повторно сверены по всем 25 hashes; manifest/исходники не изменены |
| Четыре source/destination hashes | Проверены повторно по сохранённым байтам, receipt согласован |
| Markdown/local Wiki links и состав | Проверены validator и OMX wiki lint; конкретные счётчики в validation manifest |
| Private paths/secrets/public composition | Автоматическая проверка и ручной просмотр выбранных текстов; нет private raw/PDF/полного vault; это scoped review, не универсальное доказательство отсутствия любых секретов |
| Accepted/proposed/withdrawn semantics | Приняты scope и исправленная матрица; domain rules/stack/eval open; 27/30 не возвращён |
| Git root/status/branch/worktrees/remotes | FAILED: `.git` не repo; metadata read-only |
| `git diff --check` | BLOCKED/FAILED без Git repo; отдельно выполнен no-index whitespace check каждого нового safe файла |
| Staging / staged diff / docs commit | NOT-RUN: предпосылка Git отсутствует; blanket staging не применялся |
| App tests / typecheck / build / live eval | NOT-RUN: приложение и зависимости не создаются этим этапом |
| Remote change / push / public check | NOT-RUN, запрещено этапом |

`omx wiki wiki_lint --json`: 0 broken refs / 0 contradictions, **1 informational orphan** для единственной content-page (ссылка из index не учитывается как ссылка другой content-page). Ручная проверка index→page проходит. CLI lint дописал собственный repo-local `omx_wiki/log.md`; лишняя пустая строка EOF, выявленная whitespace check, нормализована без удаления записей. При настройке независимого validator исправлены две ошибки самого checker: обработка будущего self-excluded validation manifest и ожидаемого exit 1 no-index diff с пустым файлом; итоговый прогон фиксируется отдельно, первоначальные assertion failures не выданы за зелёные проверки.

## 6. Prompts / redactions / пробелы

Лидер: фактически полученное короткое сообщение извлечено из реального session export, не заменено H-004 или starter template. Публичная версия удаляет четыре частных пути, не инженерную суть. Исходный UTF-8 hash и destination hash — в prompt receipt. В public session export сохранены task и два progress-сообщения до cutoff; первоначальный AGENTS/environment bundle исключён целиком с указанием hash/причины. System/developer/reasoning исключены самим exporter, tools не запрошены; более поздние действия и финальный ответ отсутствуют. Это **partial export**, не полный transcript. Private transcript остаётся в приватном хранилище сессии.

Workers coverage: **not-applicable**, никого не запускали. CHAT-001..009: указатели/очередь, не wholesale export; нормализованная ранняя история не выдана за точный transcript. Runtime prompts: **not-yet-created**. Полнота U-01 остаётся открытой. Redactions снимков: частные dependency links заменены безопасной атрибуцией или локальными ссылками на включённые файлы; visibility относится лишь к проекции, chat owner/accepted/proposed/open не подменены. Подробности — receipts и prompt index.

## 7. Матрица R-01..17 / U-01..08

Ни одно требование приложения не закрывается наличием отчёта. «Частично подготовкой» означает только основу/учёт, не приёмку продукта.

| ID | Статус данного этапа | Что есть / что дальше |
|---|---|---|
| R-01 | следующий этап | Teachers/Students/Courses и имена сверены с PDF; schema/seed отсутствуют |
| R-02 | следующий этап | Offerings/семестр/enrollment/оценки учтены; модель и кардинальности открыты |
| R-03 | следующий этап | NL→SQL→DB→ответ закреплён матрицей; LangGraph не создавался |
| R-04 | следующий этап | JOIN/aggregates/4 filters/multi-step учтены; нужны реальные примеры и проверки |
| R-05 | следующий этап | Независимость ядра от схемы и согласованная вторая схема учтены; доказательства переноса нет |
| R-06 | следующий этап | Полная trace chain учтена; traces приложения отсутствуют |
| R-07 | следующий этап | SQL/empty/inconsistent/ambiguous cases учтены; обработки и прогона нет |
| R-08 | следующий этап | Все три направления тестов учтены; продуктовые тесты not-run |
| R-09 | частично подготовкой | Разделены владельцы docs/prompts/memory; код и модульность приложения не проверены |
| R-10 | следующий этап | Reliability/scalability/monitoring/security/deployment должны быть объяснены позже |
| R-11 | следующий этап | Schema/seed не создавались и не публиковались |
| R-12 | следующий этап | LangGraph код/тесты отсутствуют |
| R-13 | частично подготовкой | Единый ADR index + preparation ADR; архитектурные решения и public delivery открыты |
| R-14 | следующий этап | Реальных examples/outputs/execution traces нет |
| R-15 | следующий этап | Public GitHub остаётся open; нет local commit/remote/push/public proof |
| R-16 | следующий этап | Демонстрация/самостоятельная защита/репетиция не проводились |
| R-17 | следующий этап | Компактный scope принят ранее, работа приложения ещё не доказана |
| U-01 | частично подготовкой | Actual task/selected export/coverage/redactions есть; history и runtime gaps явные |
| U-02 | уже подтверждённый факт (только срок) | По входам: вечер 7 ноября / защита 8 ноября 2026, Asia/Jerusalem; точный час неизвестен, сдача не подтверждена |
| U-03 | частично подготовкой | OMX CLI фактически использован; этап только CLI; doctor failures раскрыты |
| U-04 | частично подготовкой | Общее индексирование/подготовительный ADR; app architecture открыта |
| U-05 | частично подготовкой | Ownership сохранён, 4 safe snapshots и собственная omx_wiki; vault не заменён/не изменён |
| U-06 | частично подготовкой | Checkpoint protocol записан с proposed future status; Git execution заблокирован |
| U-07 | уже подтверждённый факт по входам | Новый содержательный чат начат ранее по CHAT-005; здесь переход не повторялся и независимо не воспроизводился |
| U-08 | следующий этап | Процедура result-understanding прочитана, остаётся proposed; проверки понимания не проводились |

## 8. Вопросы следующего архитектурного этапа (не решения)

1. **Данные/семантика:** шкала оценок, NULL, пересдачи/попытки, кардинальности offerings, веса среднего, default semester, однофамильцы/ничьи; предложенные ранее значения не приняты.
2. **SQL engine:** выбор и причины, ограничения/диалект, воспроизводимый запуск; не обещать поддержку всех диалектов.
3. **Граф/контракты:** состояние, границы DB/schema-specific logic, продолжение уточнений, зависимый сложный сценарий; несколько узлов/SQL сами по себе не доказывают reasoning.
4. **Модель/бюджет:** провайдер, версия, стоимость/число live прогонов, допустимые ошибки; бюджет не придумывать.
5. **UI/tracing:** простой экран уже в scope, библиотека/backend не выбраны; полный Input→Nodes→SQL→Results→Answer, debugging, redaction и доступность traces.
6. **SQL validation/лимиты:** возможные read-only/time/row/retry limits и внешняя проверка SQL — инженерные предложения, не дословные требования PDF; механизмы и риски обосновать.
7. **Portability:** какая небольшая вторая схема и что изменяется, какой actual run/diff докажет неизменность ядра.
8. **Test/eval plan:** independent expected results для SQL/JOIN, NL→SQL, E2E; негативные случаи, все filters/aggregates/multi-step; обоснованные метрики/набор/пороги, без отозванного 27/30 и без подмены coverage процентом.

Архитектура/контракты/план требуют отдельного CLI-поручения, затем разбора в чате **до реализации**.

## 9. Итоговые статусы / blockers / передача

- **Saved:** public-safe файлы записаны и проверены. **Committed:** not-committed — `.git` пустой read-only mount, не Git repository. `git init` не пытался обходить этот факт. Исходный/итоговый HEAD и branch: unavailable; status: not-a-repository, а не clean. После подготовки metadata blocker не изменился.
- **Remote URL/SHA:** unavailable (у целевого workspace нет repo/config); remote не создан/не изменён. **Push:** not-run. **Public check:** not-run. R-15 открыт.
- **Canonical blocker:** предпочтительный target обоснован bounded проверкой; Git identity/history/branch/worktree canonical repo не установлены из-за защищённой metadata. Не объявлять canonical Git repo готовым.
- **Environment caveat:** doctor failures EPERM/native smoke/stale session binding. Не обновляли инструмент, не имитировали здоровую среду, не исправляли недоказанное владение runtime.
- **Открыто:** обычная writable `.git` в том же target перед оставшейся Git-подготовкой, owner/name/branch/полномочия публикации, полный historical/session export, точный час дедлайна и вопросы §8. Публикация — только отдельное будущее поручение; точный следующий шаг описан в Git checkpoints.

**Единственное следующее действие: передать этот отчёт и артефакты в чат. После итогового ответа остановиться.**
