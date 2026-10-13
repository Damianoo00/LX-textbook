# Mapa mechanizmu pakietu

To projekt przenośnego workflow, nie nowa lekcja naukowa.

| Pojęcie | Wymaganie wejściowe |
|---|---|
| Brief i zakres | foundational |
| Skill | foundational |
| Kontrakt workflow | brief, skill |
| Rola agenta | kontrakt workflow |
| Natywny subagent | rola, wsparcie klienta |
| Adapter harnessu | rola, format konfiguracji klienta |
| MCP | foundational: narzędzia wywoływane przez klienta |
| Bramki jakości | artefakty planu i dowody recenzji |

Relacje: brief regulates workflow; skill regulates workflow; rola part-of workflow; adapter regulates odkrywanie ról; subagent contrasts-with rola wykonywana w głównej sesji; MCP contrasts-with orkiestracja; artefakty prerequisite recenzja; recenzja prerequisite implementacja.

Błędne przekonania: wspólny plik konfiguracji dla wszystkich klientów; MCP sam zarządza agentami; obecność pliku dowodzi jakości; subagent jest zawsze dostępny; uprawnienia z jednego projektu przenoszą się na kolejny.

Dowody formatów: oficjalne dokumentacje powiązane w README. Luka: brak pełnego uruchomienia workflow w trzech uwierzytelnionych klientach. Własny serwer sprawdzono przez protokół stdio, nie przez każdy klient MCP.
