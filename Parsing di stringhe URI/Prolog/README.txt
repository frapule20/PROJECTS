PROLOG

Non richiede configurazione.
Non richiede installazione.
 
ELENCO DEI FILE CONTENUTI NEL PACCHETTO:
	uri-parse.pl

La licenza è libera per qualsiasi uso.

Realizzato da Alberto Sormani (869019) e Francesca Pulerà (870005).

Lo scopo di questo progetto è di realizzare due librerie che costruiscono 
delle strutture che rappresentino internamente delle URI a partire dalla loro 
rappresentazione come stringhe.

ELENCO FUNZIONI
• uri-parse: 		string → uri-structure
	Riceve in input un URI rappresentata come stringa. Restituisce l'URI
	sottoforma di struttura, oppure NIL qualora l'URI passata in ingresso
	fosse errata.
• uri-display: 		uri-structure &optional stream → T
	Riceve in input una struttura URI e uno stream opzionale.
	Stampa i campi della struttura etichettandoli e se presente
	anche lo stream, ritorna TRUE.


Le funzioni "nascoste" implementano un automa.











