# LX Textbook

Skill do tworzenia interaktywnych podręczników w Codex, OpenCode i Claude Code. Zbiera informacje w rozmowie, przygotowuje projekt i prowadzi budowę od planu do działającej aplikacji.

## Uruchomienie

Otwórz ten folder w swoim narzędziu LLM i napisz:

> Przeczytaj `skills/lx-textbook/SKILL.md`. Chcę podręcznik o fotosyntezie dla początkujących. Zapytaj mnie o brakujące informacje, skonfiguruj projekt i zbuduj całość.

Agent ustali temat, odbiorców, cel i zakres. Sam zapisze brief, przygotuje konfiguracje trzech klientów i lokalnego MCP, opracuje plan oraz sprawdzi bramki jakości przed implementacją. Następnie zbuduje pierwszą pełną lekcję, rozszerzy ją do ustalonego zakresu i wykona dostępne testy.

Nie musisz wybierać adapterów, pisać briefu ani uruchamiać instalatora. Domyślnie materiał powstaje w języku rozmowy i jest planowany na około 20 minut. Możesz poprosić o inny czas lub samo planowanie. Istniejący projekt jest aktualizowany z zachowaniem jego plików i konfiguracji.

## Zawartość

```text
skills/lx-textbook/
  SKILL.md                  rozmowa, konfiguracja i workflow budowy
  scripts/bootstrap.py      przygotowanie nowego projektu
  references/pedagogy.md     zasady wyjaśnień, eksperymentów i oceny
  assets/project/           workflow, role, konfiguracje klientów i MCP
  agents/openai.yaml        metadane skilla
tests/                      testy przygotowania projektu i MCP
```

Cały folder `skills/lx-textbook` jest samodzielny: możesz przenieść go do innego środowiska i wskazać agentowi jego `SKILL.md`. Instrukcje AGENTS.md i CLAUDE.md w katalogu repozytorium służą utrzymaniu pakietu.

Potrzebujesz działającego narzędzia LLM i Pythona 3.9+. Weryfikacja źródeł oraz testy przeglądarkowe wymagają odpowiednich narzędzi w środowisku. Skill zapisuje konfiguracje projektowe; ich odkrycie przez klienta może wymagać nowej sesji. Budowa kontynuuje pracę z aktualnie dostępnymi narzędziami i rolami wykonywanymi kolejno, jeśli subagenci nie są dostępni.

Lokalny serwer MCP udostępnia odczyt dokumentów LX i sprawdzenie ich obecności. Nie ocenia merytorycznych bramek, nie wyszukuje źródeł ani nie uruchamia przeglądarki. Projekt nie jest automatycznie publikowany.

## Sprawdzanie pakietu

Z katalogu repozytorium, z Pythonem 3.11+:

```sh
python3 -m unittest discover -s tests -v
```

Testy sprawdzają samodzielność skilla, przygotowanie projektu, poprawność konfiguracji, ochronę istniejących danych oraz protokół i ograniczenia odczytu MCP. Pełna rozmowa i wygenerowanie lekcji w trzech klientach pozostają do sprawdzenia. Testy skryptów nie potwierdzają jakości przyszłych treści.

Przy aktualizacji ról utrzymuj ich definicje i natywne odpowiedniki wyłącznie w `skills/lx-textbook/assets/project/`.
