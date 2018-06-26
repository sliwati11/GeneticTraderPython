# GeneticTrader in Python
## Datenstruktur in Redis
#### Was ist Redis
>Redis (**Re**mote **DI**ctionary **S**erver)ist eine In-Memory-Datenbank aber Sie persistiert auf der Festplatte mit einer einfachen Schlüssel-werte Datenstruktur.
>Es ist eine No-SQl Datenbank, die sich besser für weniger komplexe daten geeignet und aus diesem Grund ist Sie schneller als als >relationale Datenbanken 
#### Redis Persistance
>**RDB**(Redis Datenbank) ist eine sehr kompakte Point-in-Time-Darstellung Ihrer Redis-Daten in einer Datei.
>**RDB**-Files sind perfekt für Backups.
#### Redis Data Structure
>Redis ist ein Datenstrukturserver, die viele arten von Values unterstützt.
* Strings
* Lists
* Sets
* Hashes
* Bit arrays
#### Installing Redis auf Linux
```
apt-get install redis-server
```
* Redis starten
>Die einfachste art und weise um Redis zu starten ist die Redis-Server-Binärdatei ohne irgendein Argument auszuführen
>im Terminal in Linux eingeben:
``` 
redis-server
```
* Überprüfen Sie, ob Redis funktioniert
>redis-cli: Command-line Interface, um mit Redis zu sprechen
>Im Terminal in Linux eingeben:
``` 
redis-cli ping
pong
```
* Redis ausmachen
```
SHUTDOWN 
```
#### Format von den gepushten Nachrichten

>Output:AgentenAnzahl/GenerationsAnzahl/
>buy_range_von/buy_range_bis/
>sell_range_von/sell_range_bis/
>buy_stoplos_von/buy_stoplos_bis/
>sell_stoplos_von/sell_stoplos_bis/dateiName

