# LX — wspólny kontrakt

Buduj interaktywny podręcznik z ciągłym wywodem przyczynowym. Zakres i autoryzacja pochodzą z aktualnej prośby oraz docs/brief.md projektu, nigdy z przykładów pakietu.

1. Przeczytaj brief, obowiązujące instrukcje projektu oraz skills/lx-textbook/SKILL.md. Pytaj tylko o blokujące braki.
2. Przygotuj docs/knowledge-map.md: pojęcia, jawne prerequisites albo foundational, błędne przekonania, źródła powiązane z twierdzeniami, luki dowodowe. Relacje: prerequisite, causes, regulates, part-of, contrasts-with, analogy.
3. Przygotuj docs/learning-path.md: obserwowalne cele, progresja, ciągły przykład, przykład rozwiązany, prognoza przed ujawnieniem, ocena z rubryką i transfer.
4. Przygotuj docs/storyboard.md: dla każdej sceny narracja, wizualizacja, działanie ucznia, obserwacja, dlaczego, jak i co się zmienia. Każdy ruch musi mieć cel dydaktyczny. Modele określają założenia, zakresy, jednostki, reguły i ograniczenia.
5. Recenzent zapisuje docs/quality-gates.md: pass/fail/pending, dowód, właściciel poprawki. Implementacja wymaga wszystkich bramek planu pass; obecność plików nie wystarcza. Nie wymyślaj źródeł. Nie blokuj całej pracy przez nieistotną lukę; ogranicz twierdzenie lub zakres jawnie.
6. Jeśli autoryzowano budowę, wykonaj pełny przekrój 5–10 minut z symulacją i oceną, potem pełny zakres briefu. Tryb plan kończy się po planie.
7. Testuj invariants modelu i ważne przejścia interakcji. Obejrzyj screenshoty desktop/mobile, stan początkowy i ujawniony. Sprawdź klawiaturę, focus, reduced motion, tekstowe odpowiedniki i overflow. Popraw błędy. Niedostępne narzędzia oznacz blocked, nie pass.

React/TypeScript/Vite są domyślne dla nowego projektu; zachowaj działający stack. Oddziel modele i treść od renderera. GSAP/D3/Three dodawaj tylko z uzasadnieniem. Bez limitów słów/slajdów i dekoracyjnego ruchu. Czas lekcji wymaga sprawdzenia z uczniami.

Po każdym etapie raportuj pliki, założenia, niezaliczone bramki i następny krok. Nie publikuj ani nie wysyłaj wiadomości bez autoryzacji.

## Delegowanie i przekazanie

Koordynator deleguje konkretne zadania do ról z agents/, gdy harness pozwala i delegacja jest autoryzowana. Zależności wykonuj kolejno: researcher → designer → reviewer planu → implementer → reviewer implementacji. Niezależne odczyty mogą być równoległe. Jeden właściciel edytuje dany plik; recenzent zwraca uwagi koordynatorowi. Subagenci nie delegują dalej. Jeśli subagenci są niedostępni, główny agent wykonuje te role kolejno i jawnie zaznacza brak niezależnego przeglądu.

Przekazanie zawiera: zadanie, wejściowe ścieżki, dozwolone pliki, kryterium zakończenia. Wynik zawiera pliki lub propozycje, dowody, luki i następny krok. Stan utrwalaj w docs/run-state.md: zakres, etap, właściciele, wyniki bramek, blokady, następna akcja. Przy wznowieniu odczytaj stan i zweryfikuj dowody; nie zaczynaj automatycznie od nowa.

MCP jest interfejsem narzędzi, nie orkiestratorem ani zamiennikiem skilla. Lokalny lx_artifacts czyta artefakty i sprawdza ich obecność, ale nie wydaje merytorycznego pass. Badania i przeglądarka wymagają dostępnych narzędzi harnessu lub osobno skonfigurowanych serwerów.
