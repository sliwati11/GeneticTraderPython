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
###Asyncio [intro-to-asyncio](https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/).
Asynco ist eine Module in Python3.4.
Laut Documentation asyncio bietet Infrastruktur für das Schreiben von single-threaded Code unter Verwendung von Coroutinen, multiplexen des I/O-Zugriffs über Sockets und andere Ressourcen, Ausführen von Netzwerkclients und -servern und anderer verwandter Primitive".
Das asyncio-Modul bietet einen Rahmen, der sich um die event loop dreht.
####async and await
async und await schlüsselworte sind in Python3.5
mit ** async def ** definieren wir eine coroutine funktion

>import asyncio
>async def test():
>  await another()
