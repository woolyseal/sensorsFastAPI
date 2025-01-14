# Sensorprojekt

Erste Umsetzung einer FastAPI App für Sensordaten und Überlegungen zur Umsetzung. Da ich bisher noch keine Erfahrungen mit FastAPI gesammelt habe, fange ich erst einmal mit einer möglichen Umsetzungsidee auf Grundlage des Systems "Django" an. Danach wird diese mit Hilfe von einem Tutorial und verschiedenen Webseiten auf FastAPI übertragen bzw. neu aufgebaut.

## Aufbautheorie in Django
==========================

Erste Überlegungen zu einer Umsetzung von einer Sensordatenbank mit Django als Grundlage:

Aufteilung:
* Abgeschlossene Bereiche werden in "Apps" zusammen gefasst z.B. Users, Sensors...

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


## Aufbau und Infomationen in FastAPI
=====================================

Überlegungen und erste Umsetzung zu einer FastAPI App für das importieren, speichern und ausgeben von Sensordaten. 

Aufteilung:
* Aufteilung verschiedener Bereiche in zusammenhängende Dateien/Dateibereiche z.B.: Hauptebene mit main.py, dependencies.py, danach Ordnersturktur mit einschlägiger Benamung und den entsprechenden Clustern von Dateien und Funktionen

Datenbank:
* Entscheidung für PostgreSQL wegen potentieller Datenmengen; andere wie z.B. MariaDB würden auch gehen, damit habe ich bisher noch nicht gearbeitet
* SQLAlchemy als ORM: https://www.squash.io/connecting-fastapi-with-postgresql-a-practical-approach/

Nutzermanagement:
* Beispiele selbst programmieren: https://dev.to/mochafreddo/building-a-modern-user-permission-management-system-with-fastapi-sqlalchemy-and-mariadb-5fp1 ; https://www.restack.io/p/fastapi-answer-user-management 
* FastAPI Security: https://mathison.ch/de-ch/blog/sicheres-benutzermanagement-in-fastapi-freischalte/
* Je nach Anwendungsfall könnte vermutlich beides nützlich sein, allerdings wäre bei größeren Projekten mit komplexen Persmissions vermutlich eine der selbst implementierten Lösungen so wie ich es verstehe sinniger

Modelle:
* Herangesehensweise für mich bisher ähnlich zu Django-Modellen: Evaluierung der Datenstrukturen und Aufteilung in entsprechende Päckchen
* Eintragung der Modelle als z.B. SQLAlchemy Modelle für die Erstellung der Tabellen in der Datenbank durch Programmstart
* Eintragung der Modelle als Pydantic Modelle für die Nutzung in Funktionen der FastAPI

Importskript:
* Import als aufrufbarer Endpunkt, so dass auch hier die Möglichkeit besteht diesen regelmäßig oder automatisiert auszuführen
* große Datensätze sollten möglichst mit COPY Funktion oder in größeren Bulks von z.B. 1000 durchgeführt werden

Ausgabe:
* Nutzung der API in einem gesonderten Frontend z.B. statisch, React, Next oder Einbindung in bestehende Frontend-Lösungen
* Bereitstellung als API

Rollout:
* https://medium.com/@ramanbazhanau/preparing-fastapi-for-production-a-comprehensive-guide-d167e693aa2b

