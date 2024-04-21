

INSERT INTO Persona (id, email, nome, cognome)
VALUES 
(1, 'meccanico1@email.com', 'Anna Marika', 'Biasco'),
(2, 'meccanico2@email.com', 'Massimo', 'Zarantonello'),
(3, 'meccanico3@email.com', 'Francesca', 'Pulerà'),
(4, 'meccanico4@email.com', 'Mario', 'Rossi'),
(5, 'meccanico5@email.com', 'Roberta', 'Bianchi');

INSERT INTO Meccanico (id, specializzazione, licenza)
VALUES 
(1, 0, true),   -- 'MOTORE'
(2, 1, true),   -- 'ELETTRONICA'
(3, 2, false),  -- 'GOMMISTA'
(4, 3, true),   -- 'CARROZZIERE'
(5, 3, true);   -- 'CARROZZIERE'

-- Inserisci assistenza
INSERT INTO assistenza (assistito_id, assistente_id)
VALUES (1, 2);


-- inserisci clienti

-- Inserisci dati nella tabella Persona
INSERT INTO Persona (id, email, nome, cognome)
VALUES 
(6, 'cliente1@email.com', 'Andrea', 'Rossi'),
(7, 'cliente2@email.com', 'Marta', 'Bianchi'),
(8, 'cliente3@email.com', 'Simone', 'Esposito'),
(9, 'cliente4@email.com', 'Giulia', 'Russo'),
(10, 'cliente5@email.com', 'Francesco', 'Conti');

-- Inserisci dati nella tabella Cliente
INSERT INTO Cliente (id, telefono, data_registrazione)
VALUES 
(6, '3342241426', '2018-01-23'),
(7, '3342241425', '2019-02-14'),
(8, '3343341488', '2020-03-01'),
(9, '3343388488', '2021-04-01'),
(10, '3340045488', '2022-05-01');


-- Inserisci dati nella tabella Auto
INSERT INTO Auto (id, anno_produzione, cilindrata, colore, modello, targa, cliente_id)
VALUES 
(11, 2018, 1500, 'Rosso', 'Fiat 500', 'AB123CD', 6),
(12, 2019, 1800, 'Blu', 'Volkswagen Golf', 'XY456ZA', 7),
(13, 2020, 2000, 'Nero', 'Ford Focus', 'GH789YY', 7),
(14, 2017, 1600, 'Bianco', 'Renault Clio', 'KL012MN', 10),
(15, 2016, 1400, 'Argento', 'Toyota Corolla', 'GP345QR', 10),
(16, 2015, 1900, 'Verde', 'Mercedes-Benz C-Class', 'GV678WX', 8),
(17, 2019, 2200, 'Grigio', 'BMW 3 Series', 'YZ901AB', 9);



-- Inserisci alcuni interventi di esempio con date diverse
INSERT INTO intervento (id, data_inizio, data_fine, auto_id, meccanico_id, descrizione)
VALUES 
    (18, '2022-01-15', '2022-01-16', 11, 1, 'Cambio olio'),
    (19, '2022-02-20', '2022-02-21', 11, 3, 'Sostituzione freni'),
    (20, '2022-03-20', '2022-03-26', 14, 2, 'Controllo impianto elettrico'),
    (21, '2022-04-10', '2022-04-11', 16, 3, 'Riparazione ammortizzatori'),
    (22, '2022-05-08', '2022-05-09', 17, 2, 'Cambio batteria'),
    (23, '2022-06-12', '2022-06-13', 14, 1, 'Sostituzione filtro aria'),
    (24, '2022-02-20', '2022-02-21', 13, 5, 'Verniciatura paraurti posteriore'),
    (25, '2022-03-25', '2022-03-26', 16, 4, 'Riparazione portiera');



-- Inserisci alcuni ricambi di esempio
INSERT INTO ricambio (id, costo_unitario, nome)
VALUES 
    (26, 25.99, 'Filtro olio'),
    (27, 15.50, 'Pastiglie freno anteriori'),
    (28, 30.75, 'Batteria auto'),
    (29, 12.99, 'Candele di accensione'),
    (30, 40.25, 'Amortizzatori posteriori'),
    (31, 18.60, 'Termostato'),
    (32, 8.75, 'Liquido freni'),
    (33, 35.00, 'Kit cinghia di distribuzione'),
    (34, 22.80, 'Filtro aria'),
    (35, 10.45, 'Olio motore sintetico'),
    (36, 19.99, 'Disco freno posteriore'),
    (37, 8.50, 'Spazzole tergicristallo'),
    (38, 45.25, 'Pompa acqua'),
    (39, 14.99, 'Fari anteriori'),
    (40, 32.75, 'Filtro carburante'),
    (41, 22.60, 'Cinghia servizi'),
    (42, 6.75, 'Olio cambio automatico'),
    (43, 29.00, 'Sonda lambda'),
    (44, 16.80, 'Guarnizione testata'),
    (45, 12.45, 'Pastiglie freno posteriori');


-- Associa i ricambi agli interventi nella tabella utilizzo
INSERT INTO utilizzo (ricambio_id, intervento_id)
VALUES 
    -- Intervento 18 (Cambio olio)
    (26, 18), -- Filtro olio
    (35, 18), -- Olio motore sintetico

    -- Intervento 19 (Sostituzione freni)
    (27, 19), -- Pastiglie freno anteriori
    (36, 19), -- Disco freno posteriore

    -- Intervento 20 (Controllo impianto elettrico)
    (28, 20), -- Batteria auto

    -- Intervento 21 (Riparazione ammortizzatori)
    (30, 21), -- Amortizzatori posteriori

    -- Intervento 22 (Cambio batteria)
    (28, 22), -- Batteria auto

    -- Intervento 23 (Sostituzione filtro aria)
    (34, 23), -- Filtro aria

    -- Intervento 24 (Verniciatura paraurti posteriore)
    (39, 24), -- Fari anteriori

    -- Intervento 25 (Riparazione portiera)
    (44, 25); -- Pastiglie freno posteriori