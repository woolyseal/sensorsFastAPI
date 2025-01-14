Aufbautheorie in Django
=======================

Datenbank/Django:
* PostgreSQL wg. Datenmengen (man könnte auch z.B. MariaDB nutzen, allerdings habe ich damit noch keine Erfahrung gesammelt)
* Anbindung an die DB über .env Datei um Login-Daten zu schützen und nicht öffentlich zugänglich zu machen
* Rechte und Nutzer können direkt über Django-Rechtesystem genutzt und weiter verarbeitet werden

Modelle: 
* Evaluation der Sensordaten im Hinblick auf Dateistruktur
* Wiederkehrende Daten sollten eigene Modelle und damit Tabellen kriegen die dann mit Keys verlinkt werden um redundante Daten zu verringern
* Vererbung der Modelle wenn sinnig

Importskript:
* Evaluation der Sensordaten im Hinblick auf Format (JSON, XML, CSV...) und Dateiaufbau
* Managementskript für Import programmieren um dieses mehrfach/regelmäßig ausführen zu können mit z.B. Cron, Celery usw.

Ausgabe:
* direkt per Nutzung von Django-Templates mit entsprechenden Suchen und Routen
* ggf. Nutzung zusätzlicher Librarys wie HTMX für LazyLoading und Ajax-Aufrufe


Aufbau und Infomationen in FastAPI
===================================

Datenbank:
* PostgreSQL wegen potentieller Datenmengen
* SQLAlchemy als ORM: https://www.squash.io/connecting-fastapi-with-postgresql-a-practical-approach/
* Am Besten wäre Import bei großen Datenmengen über COPY Funktion in Bulks von größeren Zahlen 

Modelle:

Importskript:

