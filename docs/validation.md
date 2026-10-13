# Walidacja

Wykonano `python3 -m unittest discover -s lx-textbook/tests -v` z nadrzędnego projektu: 4 testy PASS. Test instalacji iteruje przez codex/claude/opencode/all, parsuje JSON/TOML i uruchamia zainstalowany serwer MCP jako subprocess: initialize, initialized notification, tools/list i tools/call. Pozostałe testy potwierdzają brak częściowej instalacji przy kolizji, odmowę odczytu poza root oraz brak fałszywego semantic pass.

Skill sprawdzany również walidatorem skill-creator. Zawartość lx-textbook skopiowana jako samodzielny pakiet z generatorami i referencją pedagogiki.

Nie wykonano sesji LLM w trzech klientach ani rzeczywistego generowania lekcji. Codex CLI jest obecny (0.162.1); OpenCode nie mógł odczytać wersji, bo próbuje zapisywać log poza dozwolonym workspace. Claude CLI nie jest obecny. Testy protokołu nie dowodzą discovery ról ani jakości działania modeli. Nie ma UI pakietu do screenshotów; workflow nadal wymaga ich dla wynikowych aplikacji.

Następny sprawdzian: zainstalować pakiet w projekcie testowym, utworzyć konkretny brief i uruchomić prompt w każdym kliencie. Sprawdzić discovery, listę narzędzi MCP oraz zachowanie bramki fail przed implementacją.
