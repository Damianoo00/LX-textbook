# LX Textbook

Samodzielny pakiet workflow do tworzenia interaktywnych podręczników w **Codex, OpenCode i Claude Code**. Pakiet znajduje się w folderze `lx-textbook/`. Możesz przechowywać jego zawartość jako osobne repozytorium GitHub o nazwie `lx-textbook`. Nie zależy od nadrzędnego projektu ani jego modułu neurobiologicznego.

## Struktura

```text
core/workflow.md             wspólny kontrakt i kolejność bramek
agents/                     koordynator oraz cztery role specjalistyczne
skills/lx-textbook/          skill, pedagogika, generator nowego modułu
adapters/codex/              .codex/agents/*.toml oraz config.toml
adapters/opencode/           .opencode/agents/*.md oraz opencode.json
adapters/claude/             .claude/agents/*.md oraz .mcp.json
mcp/artifacts_server.py      lokalny serwer MCP, tylko odczyt
scripts/install.py          instalacja lokalna, kontrola kolizji, dry-run
docs/                       przykładowy brief, projekt pakietu i walidacja
prompts/start.md             prompt uruchamiający workflow
tests/                      testy instalatora i protokołu MCP
```

Koordynator prowadzi researcher → designer → reviewer planu → implementer → reviewer implementacji. Koordynator jest główną sesją w Codex i Claude; OpenCode dodatkowo oferuje primary agent `lx-coordinator`. Nazwy ról natywnych: `lx-researcher`, `lx-designer`, `lx-implementer`, `lx-reviewer` (Codex używa podkreśleń w polu `name`). Koordynator może także zostać wywołany jako rola. Modele nie są narzucone: konfiguracje dziedziczą wybór harnessu.

Subagenci są opcjonalni. W sesji bez delegowania te same zadania wykona jeden agent kolejno. Raport musi wtedy ujawnić brak niezależnej recenzji. Instrukcje nie zastępują ograniczeń uprawnień ani polityk danego harnessu.

## Użycie

Wymagany Python 3.9+ do instalatora i serwera; Python 3.11+ do testów (tomllib). Narzędzia LLM instalujesz i uwierzytelniasz osobno.

Z katalogu nadrzędnego wejdź do folderu pakietu i uruchom instalator:

```sh
cd lx-textbook
python3 scripts/install.py /sciezka/do/projektu --harness all --dry-run
python3 scripts/install.py /sciezka/do/projektu --harness all
```

Jeśli otwarto już katalog główny osobnego repozytorium `lx-textbook`, pomiń `cd lx-textbook`. Nazwa opcji `--harness` pozostaje bez zmian: wskazuje klienta LLM, dla którego instalujesz konfigurację.

Zamiast `all` możesz podać `codex`, `opencode` lub `claude`. Instalator kopiuje wspólny workflow, skill i właściwe konfiguracje; umieszcza kopie skilla także w natywnych katalogach discovery. Nie zapisuje konfiguracji globalnej. W razie kolizji odmawia kopiowania całego zestawu. W istniejącym projekcie wygeneruj pakiet w osobnym pustym katalogu i połącz instrukcje oraz konfiguracje ręcznie; zachowaj istniejące serwery, uprawnienia i ustawienia.

Utwórz `docs/brief.md` na podstawie `docs/brief.example.md` z tego pakietu: temat, odbiorca, zakres, przykład, język i tryb `build` albo `plan`. Następnie **uruchom wybrany harness z katalogu głównego projektu** i przekaż treść `prompts/start.md`. Konfiguracja projektowa musi być zaufana/wczytana zgodnie z zasadami narzędzia. W Codex sprawdź dostępność custom subagents i MCP; w Claude sprawdź `/agents` i `/mcp`; w OpenCode wybierz `lx-coordinator` i sprawdź agentów/MCP. Po instalacji rozpocznij nową sesję, jeśli narzędzie nie odświeża konfiguracji.

Możesz też utworzyć samą bazę nowego modułu:

```sh
python3 skills/lx-textbook/scripts/new_module.py /sciezka/do/nowego-modulu --topic "Fotosynteza" --example "Roślina przy oknie"
```

Generator tworzy projekt ze skillem i briefem, ale **nie instaluje adapterów**. Ponieważ projekt zawiera już AGENTS.md i skill, zainstaluj adaptery w osobnym pustym katalogu i połącz je jak opisano wyżej. Nie deklaruje on przejścia bramek ani nie generuje faktów naukowych.

## MCP

`lx_artifacts` jest rzeczywistym serwerem stdio bez zależności Python. Wszystkie adaptery uruchamiają:

```sh
python3 mcp/artifacts_server.py --root .
```

Udostępnia `artifact_status` i `read_artifact`. Czyta wyłącznie sześć nazw dokumentów LX w `docs/`, z limitem 128 KiB i kontrolą ścieżek/symlinków. Obecność dokumentów nie oznacza przejścia bramek. `quality-gates.md` jest raportem recenzenta, nie automatycznym wynikiem tego serwera. Nie zapisuje plików, nie wyszukuje źródeł i nie uruchamia przeglądarki.

Ścieżki względne zakładają katalog roboczy projektu. Jeśli klient MCP startuje gdzie indziej, w jego konfiguracji ustaw absolutną ścieżkę skryptu oraz absolutny argument `--root`. Nie commituj tych lokalnych ścieżek jako uniwersalnego ustawienia.

Badania źródeł korzystają z narzędzi web harnessu lub materiałów użytkownika. Testy przeglądarkowe korzystają z dostępnej przeglądarki/Playwright projektu. Dodatkowe serwery MCP można dopisać do właściwej konfiguracji klienta; pakiet ich nie instaluje ani nie zakłada ich dostępności. Gdy brak narzędzi, zapisuj luki i blocked. Przed użyciem sprawdź listę narzędzi serwera w kliencie.

## Aktualizacja i walidacja

Wspólny workflow utrzymuj w `core/workflow.md`, role w `agents/*.md`. Adaptery zawierają natywne kopie promptów ról — po zmianie roli uaktualnij odpowiadające pliki w trzech adapterach. Zainstalowane kopie skilla również aktualizuj z `skills/lx-textbook`; nie edytuj każdej kopii niezależnie.

```sh
python3 -m unittest discover -s tests -v
```

Powyższe polecenie uruchom z folderu `lx-textbook/`. Z katalogu nadrzędnego użyj `python3 -m unittest discover -s lx-textbook/tests -v`.

Zakres wykonanych sprawdzeń i ograniczenia: [docs/validation.md](docs/validation.md). To pakiet instrukcji i konfiguracji, nie autonomiczny daemon ani gwarancja identycznego zachowania modeli. Obowiązkowe bramki muszą być ocenione w każdym module. Instalacja nie publikuje projektu na GitHubie ani w hostingu.

Formaty adapterów sprawdzono 2026-10-13 na podstawie dokumentacji: [Codex subagents](https://developers.openai.com/codex/multi-agent), [Codex skills](https://developers.openai.com/codex/skills), [Codex MCP](https://developers.openai.com/codex/mcp), [OpenCode agents](https://opencode.ai/docs/agents/), [OpenCode skills](https://opencode.ai/docs/skills/), [OpenCode MCP](https://opencode.ai/docs/mcp-servers/), [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Claude MCP](https://code.claude.com/docs/en/mcp). Zgodność z każdą historyczną lub przyszłą wersją nie jest deklarowana.
# LX-textbook
