# LX Textbook — utrzymanie pakietu

Źródłem workflow jest skills/lx-textbook/SKILL.md. Wszystkie zasoby generowanego projektu znajdują się w skills/lx-textbook/assets/project/, a pedagogika w references/pedagogy.md tego skilla. Nie odtwarzaj kopii agentów, adapterów ani serwera MCP w katalogu głównym repozytorium.

Przy zmianach pakietu zachowaj samodzielność skilla i ochronę istniejących projektów. Uruchom python3 -m unittest discover -s tests -v. Przy zmianach ról uaktualnij ich natywne odpowiedniki w assets/project/. Nie uruchamiaj generowania lekcji podczas samego utrzymywania pakietu. Zakres i autoryzacja lekcji pochodzą z bieżącej prośby i briefu projektu.
