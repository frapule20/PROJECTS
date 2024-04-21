# Inizializzazione del database
Installazione di PostgreSQL
Per iniziare, è necessario scaricare e installare PostgreSQL. È possibile ottenere il software dal sito ufficiale: https://www.postgresql.org/.

Durante l'installazione, prendere nota dell'username e della password scelti per l'accesso al database. Si consiglia anche di considerare la porta di accesso, nel caso si desideri utilizzare una diversa da quella di default.

## Installazione delle estensioni su Visual Studio Code (VSCode)
Per questo tutorial, useremo l'IDE VSCode, che offre un'ottima integrazione con le estensioni necessarie per lavorare con PostgreSQL. Assicurarsi di installare l'estensione per PostgreSQL dal marketplace di VSCode.

## Inizializzazione dell'applicazione
Prima di accedere all'applicazione, è essenziale inizializzare il database utilizzando VSCode. Questo processo va eseguito solo una volta, in quanto il database è persistente tra le varie sessioni.

Aprire l'estensione di PostgreSQL in VSCode e aggiungere un nuovo database cliccando sull'icona "+" nella barra laterale.

Successivamente, compilare i seguenti campi:

Hostname: localhost
User: [nome utente scelto durante l'installazione]
Password: [password utente scelta]
Selezionare la connessione standard
Mostrare tutti i database
Display name: localhost PostgreSQL DB

## Creazione del database
Dopo aver creato la connessione al database, è necessario inizializzarlo creando un nuovo database attraverso delle query.

Eseguire la seguente query SQL:

    CREATE DATABASE officina;

Con questa istruzione, il database "officina" sarà creato e sarà pronto per essere utilizzato dall'applicazione. Successivamente, sarà l'applicazione stessa a occuparsi della creazione delle tabelle e delle relazioni all'interno di questo database.







