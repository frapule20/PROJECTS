

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; 01/2022
; Linguaggi di programmazione
;     Prof. M. Antoniotti
;     Prof. P. Braione
;     Prof. G. Pasi
;     Prof. R. N. Penaloza
;     Prof. G. Vizzari
; Universita' degli studi di Milano-Bicocca
; autori:
;     Alberto Sormani   MAT 869019
;     Francesca Pulera' MAT 870005
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; STRUTTURA URI
; definisco la truttura dell'uri
(defstruct uri scheme userinfo host port path query fragment)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; FUNZIONI RICHIESTE
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; URI-USERINFO
; URI-HOST
; URI-PORT
; URI-PATH
; URI-QUERY
; URI-FRAGMENT
; sono implementati automaticametne grazie a (uri-* <uri-struct>)


; URI-PARSE
; trasforma una stringa in una struttura uri se corretta, altrimenti NIL
(defun uri-parse (s)
  ; rememorizzo le variabili
  (setq scheme nil)
  (setq userinfo nil)
  (setq host nil)
  (setq port nil)
  (setq path nil)
  (setq query nil)
  (setq fragment nil)
  (cond 
   ; converto la stringa in una lista di caratteri
   ; e salto allo stato iniziale dell'automa
   ; attraversando i vari stati. Vengono inoltre settate 
   ; le variabili.
   ; Se uno dei controlli ritorna NIL termino
   ((null (fun-scheme (coerce s 'list))) nil)
   ; altrimenti creo una struttura uri con i valori ricavati
   (t (make-uri
       ; se il parametro e' NIL allora memorizzo NIL
       :scheme (if scheme (coerce scheme 'string) nil)
       :userinfo (if userinfo (coerce userinfo 'string) nil)
       :host (if host (coerce host 'string) nil)
       ; port ha 80 di default
       :port (if port (coerce port 'string) 80)
       :path (if path (coerce path 'string) nil)
       :query (if query (coerce query 'string) nil)
       :fragment (if fragment (coerce fragment 'string) nil)))))


; URI-DISPLAY
; accetta una struttura uri e uno stream opzionale
; e li stampa a video
(defun uri-display (s &optional stream)
  ; creo una "struttura" per l'uri
  (format t
          "Scheme:   ~a
           Userinfo: ~a
           Host:     ~a
           Port:     ~a
           Path:     ~a
           Query:    ~a
           Fragment: ~a~%~%"
          ; inserisco i pezzi dell'uri in questa struttura
          (uri-scheme s)
          (uri-userinfo s)
          (uri-host s)
          (uri-port s)
          (uri-path s)
          (uri-query s)
          (uri-fragment s))
  ; se c'e' lo stream lo stampo
  (if (null stream) nil (format t "~a~%~%" stream)) t)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; AUTOMA
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; qualunque stato puo' saltare a NIL


; SCHEME
; possibili stati precedenti:
; possibili stati successivi: userinfo, userinfo mailto,
;   userinfo tel fax, host special
; stato d'accettazione: si
(defun fun-scheme (lista)
  ; riceve l'intera lista
  ; se non ci sono i ":" allora NIL
  (if (not (search '(#\:) lista)) nil
    ; altrimenti memorizzo in scheme la sottolista fino ai ":"
    (and (setq scheme (sottolista lista (- (search '(#\:) lista) 1)))
         ; controllo che scheme non contenga caratteri non ammessi...
         (cond ((or (null scheme)
                    (search '(#\/) scheme)
                    (search '(#\?) scheme)
                    (search '(#\#) scheme)
                    (search '(#\@) scheme)) nil)
                    ; ...nel caso li contenesse stampo NIL
               ; se dopo ":"  non c'e' nulla, accetto, tranne nel caso zos
               ((and (null (sottolista lista (- (length lista) 1) 
                                       (+ 1 (search '(#\:) lista))))
                     (not (string= "zos" (string-downcase
                                       (coerce scheme 'string))))) t)
               ; se scheme e' "mailto" salto allo stato "userinfo mailto"
               ; gli passo la sottolista da dopo ":"
               ((string= "mailto" (string-downcase (coerce scheme 'string)))
                (fun-userinfo-mailto (sottolista lista (- (length lista) 1) 
                                                    (+ 1 (search '(#\:)
                                                    lista)))))
               ; se scheme e' "news" salto allo stato "host special"
               ; gli passo la sottolista da dopo ":"
               ((string= "news" (string-downcase (coerce scheme 'string)))
                (fun-host-special (sottolista lista (- (length lista) 1) 
                                              (+ 1 (search '(#\:) lista)))))
               ; se scheme e' "tel" o "fax" salto allo stato "userinfo tel fax"
               ; gli passo la sottolista da dopo ":"
               ((or (string= "tel" (string-downcase (coerce scheme 'string)))
                    (string= "fax" (string-downcase (coerce scheme 'string))))
                (fun-userinfo-tel (sottolista lista (- (length lista) 1) 
                                              (+ 1 (search '(#\:) lista)))))
               ; altrimenti salto allo stato "userinfo"
               ; gli passo la sottolista da dopo ":"
               (t (fun-userinfo (sottolista lista (- (length lista) 1) 
                                            (+ 1 (search '(#\:) lista)))))))))


; USERINFO
; possibili stati precedenti: scheme
; possibili stati successivi: host, path
; stato d'accettazione: no
(defun fun-userinfo (lista)
  ; riceve una sottolista da dopo ":" 
  (cond ; se c'e' l'autorithy...
   ((and (equal (first lista) #\/) (equal (second lista) #\/))
    ; allora conrollo se c'e' "@"
    (cond ((search '(#\@) lista)
           ; se la trovo memorizzo userinfo con i caratteri tra "//" e "@"
           (and (setq userinfo (sottolista lista
                                           (- (search '(#\@) lista) 1)
                                           (+ (search '(#\/ #\/) lista) 2)))
                ; verifico che userinfo abbia i caratteri giusti...
                (if (or (null userinfo)
                        (search '(#\/) userinfo)
                        (search '(#\?) userinfo)
                        (search '(#\#) userinfo)
                        (search '(#\@) userinfo)
                        (search '(#\:) userinfo))
                    ; ...nel caso avesse caratteri non ammessi ritorna NIL
                    nil
                  ; altrimenti salto allo stato "host"
                  ; gli passo la sottolista da dopo "@"
                  (fun-host (sottolista lista (- (length lista) 1)
                                        (+ 1 (search '(#\@) lista)))))))
          ; se non trovo "@" allora salto allo stato "host" e
          ; gli passo la sottolista da dopo "//"
          (t (fun-host (sottolista lista (- (length lista) 1) 2)))))
   ; se non trovo l'autority, ma trovo il path
   ; allora salto allo stato "path" e
   ; gli passo la sottolista da dopo "/"
   ((equal #\/ (first lista)) (fun-path (sottolista lista
                                                    (- (length lista) 1) 
                                                    (+ 1 (search '(#\/)
                                                    lista)))))
   ; altrimenti ritorno nil
   (t nil)))


; USERINFO MAILTO
; possibili stati precedenti: scheme
; possibili stati successivi: userinfo tel fax, host special
; stato d'accettazione: no
;   (perche' per accettare salto allo stato "userinfo tel")
(defun fun-userinfo-mailto (lista)
  ; riceve da dopo i ":" dello scheme
  ; se trovo "@"
  (if (search '(#\@) lista)
      ; memorizzo l'userinfo a cio' che c'e' prima
      (and (setq userinfo (sottolista lista (- (search '(#\@) lista) 1)))
           ; verifico che userinfo abbia i caratteri giusti...
           (if (or (null userinfo)
                   (search '(#\/) userinfo)
                   (search '(#\?) userinfo)
                   (search '(#\#) userinfo)
                   (search '(#\@) userinfo))
               ; ...nel caso avesse caratteri non ammessi ritorna NIL
               nil
             ; altrimenti salto allo stato "host special"
             ; gli passo la sottolista da dopo "@"
             (fun-host-special (sottolista lista (- (length lista) 1)
                                           (+ 1 (search '(#\@) lista))))))
    ; se non trovo "@" allora salto allo stato "userinfo tel"
    (fun-userinfo-tel lista)))


; USERINFO TEL e FAX
; possibili stati precedenti: scheme, userinfo tel fax
; possibili stati successivi: 
; stato d'accettazione: si
(defun fun-userinfo-tel (lista)
  ; riceve da dopo i ":" dello scheme
  (if (or (null lista) ; controllo che contenga solo caratteri ammessi...
          (search '(#\/) lista)
          (search '(#\?) lista)
          (search '(#\#) lista)
          (search '(#\@) lista))
      ; ...altrimenti ritorno NIL
      nil
    ; se va bene allora memorizzo userinfo e accetto
    (setq userinfo lista)))


; HOST
; possibili stati precedenti: userinfo
; possibili stati successivi: host special, path, port
; stato d'accettazione: no
;   (perche' per accettare salto allo stato fun-host-special)
(defun fun-host (lista)
  (cond ; se c'e' il port e quindi i ":"...
   ((search '(#\:) lista)
    ; ...memorizzo host fino ai ":"
    (and (setq host (sottolista lista (- (search '(#\:) lista) 1)))
         ; controllo che i ":" siano  veramente l'inizio del port e
         ; non un carattere di query o fragment
         (cond ((search '(#\/) host)
                ; quindi se compare "/" allora
                ; memorizzo nuovamente host fino a "/"
                (and (setq host (sottolista lista 
                                            (- (search '(#\/) lista) 1)))
                     ; controllo i caratteri dell'host
                     (host-ctrl host)
                     ; poi vado a vedere se c'e' il path
                     ; passandogli la lista da dopo lo "/"
                     (fun-path (sottolista lista
                                           (- (length lista) 1)
                                           (+ (search '(#\/) lista) 1)))))
               ; se invece i ":" sono veramenti l'inizio del port
               ; allora salto allo stato "port"
               (t (and (host-ctrl host)
                       (fun-port (sottolista lista (- (length lista) 1)
                                             (+ (search '(#\:) lista) 1))))))))
   ; se non c'e' il port ma c'e' il path o la query o il fragment...
   ((search '(#\/) lista)
    ; allora memorizzo l'host fino a "/"
    (and (setq host (sottolista lista (- (search '(#\/) lista) 1)))
         ; controllo che l'host sia giusto
         (host-ctrl host)
         ; vado allo stato path
         ; passandogli la lista da dopo "/"
         (fun-path (sottolista lista (- (length lista) 1)
                               (+ (search '(#\/) lista) 1)))))
   ; altrimenti la lista e' tutta host
   ; quindi vado allo stato "host special"
   (t (fun-host-special lista))))


; HOST SPECIAL (oppure host seguito da niente)
; possibili stati precedenti: scheme, userinfo mailto, host
; possibili stati successivi: 
; stato d'accettazione: si
(defun fun-host-special (lista)
  ; controllo la lista
  ; se e' corretta la assegno ad host e accetto
  (if (null (host-ctrl lista)) nil (setq host lista)))


; PORT
; possibili stati precedenti: host
; possibili stati successivi: path
; stato d'accettazione: si
(defun fun-port (lista)
  ; controllo che la lista non sia vuota
  (cond ((null lista) nil)
        ; se c'e' il path, o la query o il fragment...
        ((search '(#\/) lista)            
            ; ... memorizzo port fino a "/"
            (and (setq port (sottolista lista (- (search '(#\/) lista) 1)))
                 ; controllo che il port sia corretto
                 (if (and (numeri port) (not (null port)) (< (length port) 6))                   
                     ; se lo e' salto allo sato "path"
                     ; passandogli la sottolista da "/" in poi
                     (fun-path (sottolista lista (- (length lista) 1)
                                           (+ 1 (search '(#\/) lista))))
                   nil))) ; altrimenti ritorno NIL
        ; se non ci sono path, query e fragment
        ; memorizzo direttamente port fino alla fine della lista
        (t (if (and (numeri lista) (< (length lista) 6))
            (setq port lista) nil))))


; PATH
; possibili stati precedenti: userinfo, host
; possibili stati successivi: path zos, query, fragment
; stato d'accettazione: si
(defun fun-path (lista)
  ; se lo scheme e' zos allora salto allo stato dedicato
  (cond ((string= "zos" (string-downcase (coerce scheme 'string)))
         (fun-path-zos lista))
        ; se c'e' "?" come primo carattere allora salto a query
        ((equal #\? (first lista)) (fun-query (sottolista lista
                                                          (- (length lista) 1) 
                                                          (+ 1 (search '(#\?)
                                                          lista)))))
        ; se c'e' "#" come primo carattere allora salto a fragment
        ((equal #\# (first lista)) (fun-fragment (sottolista lista
                                                      (- (length lista) 1) 
                                                      (+ 1 (search '(#\#)
                                                      lista)))))
        ; se invece c'e' il path
        ; e se c'e' la query dopo il path...
        ((search '(#\?) lista)
         ; ... allora il path arriva fino a "?"
         (and (setq path (sottolista lista (- (search '(#\?) lista) 1)))
              ; controllo che "?" sia davvero prima della query e 
              ; non sia invece un carattere del fragment...
              (cond ((search '(#\#) path) 
                     ; nel caso rimemorizzo path
                     (and (setq path (sottolista path 
                                                 (- (search '(#\#) path) 1)))
                          ; controllo che sia giusto
                          (if (or (search '(#\@) path)
                                  (search '(#\:) path)
                                  (search '(#\/) path))
                              nil
                            ; e salta a "fragment"
                            (fun-fragment (sottolista lista
                                                      (- (length lista) 1)
                                                      (+ 1 (search '(#\#)
                                                      lista)))))))
                    ; se "?" non e' parte del path, controllo che sia giusto
                    ; se non lo e' interrompo
                    ((or (search '(#\@) path)
                         (search '(#\:) path)
                         (equal '(#\/) (last path))) nil)
                    ; altrimenti salto allo satato "query"
                    ; passandogli la sottolista da dopo "?"
                    (t (fun-query (sottolista lista (- (length lista) 1)
                                              (+ 1 (search '(#\?) lista))))))))
        ; se non c'e' la query ma c'e' il fragment...
        ((search '(#\#) lista)
         ; ... allora il path arriva fino a "#"
         (and (setq path (sottolista lista (- (search '(#\#) lista) 1)))
              ; controllo che il path sia correttamente formato...
              (if (or (search '(#\@) path)
                      (search '(#\:) path)
                      (equal '(#\/) (last path)))
                  nil ; ...se non lo e' stampo NIL
                ; altrimenti salto allo satato "fragment"
                ; passandogli la sottolista da dopo "#"
                (fun-fragment (sottolista lista (- (length lista) 1)
                                          (+ 1 (search '(#\#) lista)))))))
        ; se invece il path non e' seguito da niente
        ; controllo prima che sia corretto...
        (t (if (or (search '(#\?) lista)
                   (search '(#\#) lista)
                   (search '(#\@) lista)
                   (search '(#\:) lista)
                   (equal '(#\/) (last lista)))
               nil ; ...se non lo e' stampo NIL,
             ; altrimenti assegno la lista a path e accetto
             (setq path lista)))))


; PATH ZOS
; possibili stati precedenti: path
; possibili stati successivi: query, fragment
; stato d'accettazione: si
(defun fun-path-zos (lista)
  ; controllo che la lista non sia vuota
  (cond ((null lista) nil)
        ; controllo che il path di zos abbia almeno un carattere
        ((equal #\? (first lista)) nil)
        ((equal #\# (first lista)) nil)
        ; controllo che id44 abbia almeno un carattere
        ((equal #\( (first lista)) nil)
        ((equal #\) (first lista)) nil)
        ; se trovo una parentesi aperta...
        ((search '(#\() lista) 
         ; ...memorizzo id44 dentro path
         (and (setq path (sottolista lista (- (search '(#\() lista) 1)))
              (cond ; controllo che non sia parte della query
               ((search '(#\?) path)
                ; memorizzo nuovamente id44 correttamente
                (and (setq path (sottolista lista
                                            (- (search '(#\?) lista) 1)))
                     ; controllo i caratteri di id44
                     (fun-id44 path)
                     ; salto allo stato "query"
                     ; passandogli la sottolista da dopo la "?"                      
                     (fun-query (sottolista lista (- (length lista) 1)
                                            (+ 1 (search '(#\?) lista))))))
               ; controllo che non sia parte del fragment...
               ((search '(#\#) path)
                ; memorizzo nuovamente id44 correttamente
                (and (setq path (sottolista lista
                                            (- (search '(#\#) lista) 1)))
                     ; controllo i caratteri di id44
                     (fun-id44 path)
                     ; salto allo stato "fragment"
                     ; passandogli la sottolista da dopo "#"
                     (fun-fragment (sottolista lista (- (length lista) 1)
                                                (+ 1 (search '(#\#) lista))))))
               ; controllo che esista la parentesi chiusa
               ((not (search '(#\)) lista)) nil)
               ; se esiste allora
               (t ; controllo id44
                (and (fun-id44 path)
                     ; controllo id8
                     ; passandogli la sottolista racchiusa tra le parentesi
                     (fun-id8 (sottolista lista (- (search '(#\)) lista) 1)
                                          (+ (search '(#\() lista) 1)))
                     ; dopo la parentesi chiusa
                     (cond
                      ; CASO QUERY
                      ; salto allo stato "query"
                      ; passandogli la sottolista da dopo "?"
                      ((equal #\? (first (sottolista lista
                                                     (- (length lista) 1)
                                                     (+ 1 (search '(#\))
                                                     lista)))))
                       (fun-query (sottolista lista (- (length lista) 1)
                                              (+ 1 (search '(#\?) lista)))))
                      ; CASO FRAGMENT
                      ; salto allo stato "fragment"
                      ; passandogli la sottolista da dopo "#"
                      ((equal #\# (first (sottolista lista
                                                     (- (length lista) 1)
                                                     (+ 1 (search '(#\))
                                                     lista)))))
                       (fun-fragment (sottolista lista
                                                 (- (length lista) 1)
                                                 (+ 1 (search '(#\#)
                                                 lista)))))
                      ; se non ci sono ne' query ne' fragment,
                      ; controllo che non ci sia niente dopo
                      ; la parentesi chiusa e accetto
                      ((null (sottolista lista (- (length lista) 1)
                                         (+ 1 (search '(#\)) lista)))) t)
                      ; se invece trovo altri caratteri,
                      ; ritorno NIL
                      (t nil)))))))
        ; se non c'e' la "("
        (t (cond ; CASO QUERY
                 ; salto allo stato "query"
                 ; passandogli la sottolista da dopo la "?"
            ((search '(#\?) lista)
             (and (setq path (sottolista lista (+ (search '(#\?) 1))))
                  (fun-id44 path)
                  (fun-query (sottolista lista (- (length lista) 1)
                                         (+ 1 (search '(#\?) lista))))))
            ; CASO FRAGMENT
            ; salto allo stato "fragment"
            ; passandogli la sottolista da dopo "#"
            ((search '(#\#) lista)
             (and (setq path (sottolista lista (+ (search '(#\#) 1))))
                  (fun-id44 path)
                  (fun-fragment (sottolista lista (- (length lista) 1)
                                            (+ 1 (search '(#\?) lista))))))
            ; se non ci sono ne' query ne' fragment,
            ; controllo che non ci sia niente dopo
            ; la parentesi chiusa e accetto
            (t (and (setq path lista)
                    (fun-id44 path)))))))


; QUERY
; possibili stati precedenti: path, path zos
; possibili stati successivi: fragment
; stato d'accettazione: si
(defun fun-query (lista)
  ; controllo che la lista contenga almeno un carattere
  (cond ((null lista) nil)
        ; controllo che la query abbia almeno un carattere
        ((equal (first lista) #\#) nil)
        ; se e' seguita dal fragment...
        ((search '(#\#) lista)
         ; salto allo stato "fragment"
         ; passandogli la sottolista da dopo "#"
         (and (setq query (sottolista lista (- (search '(#\#) lista) 1)))
              (fun-fragment (sottolista lista (-(length lista) 1)
                                        (+ (search '(#\#) lista) 1)))))
        ; altrimenti la query e' l'ultimo componente di questo uri
        ; allora memorizzo in query fino a "#" e accetto
        (t (setq query lista))))


; FRAGMENT
; possibili stati precedenti: path, path zos
; possibili stati successivi:
; stato d'accettazione: si
(defun fun-fragment (lista)
    ; controllo che la lista non sia vuota,
    ; la memorizzo in fragment e accetto
    (if (null lista) nil (setq fragment lista)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ALTRE FUNZIONI
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; controllo che i caratteri di host siano corretti
(defun host-ctrl (lista)
  (if (or (null lista)
          (equal #\. (first lista))
          (equal '(#\.) (last lista))
          (search '(#\/) lista)
          (search '(#\?) lista)
          (search '(#\#) lista)
          (search '(#\@) lista)
          (search '(#\:) lista))
      nil t)) ; in caso di problemi ritorno NIL


; controllo che i caratteri di id44 siano corretti
(defun fun-id44 (lista)
  (if (or (null lista)
          (> (length lista) 44)
          (not (lettere (list (first lista))))
          (equal '(#\.) (last lista))
          (not (alfanumerica. lista)))
      nil t)) ; in caso di problemi ritorno NIL


; controllo che i caratteri di id8 siano corretti
(defun fun-id8 (id8)
  (if  (or (null id8)
           (> (length id8) 8)
           (not (lettere (list (first id8))))
           (not (alfanumerica id8)))
      nil ; in caso di problemi ritorno NIL
    ; se invece sono giusti memorizzo path = id44(id8)
    (setq path (append path '(#\() id8 '(#\))))))


; ritorna la sottolista dall'indice opzionale "inizio" all'indice "fine"
(defun sottolista (lista fine &optional (inizio 0))
  (cond ((null lista) nil)
        ((> fine (length lista)) nil)
        ((< fine inizio) nil)
        ((zerop fine) (list (car lista)))
        ((zerop inizio) (append (list (car lista))
                                (sottolista (cdr lista) (- fine 1) 0)))
        (t (sottolista (cdr lista) (- fine 1) (- inizio 1)))))


; funzione che determina se tutti gli elementi di una lista sono numeri
(defun numeri (lista)
  (cond ((null lista) t)
        ((digit-char-p (car lista)) (numeri (cdr lista)))
        (t nil)))


; funzione che determina se tutti gli elementi di una lista
; sono caratteri alfanumerici
(defun alfanumerica (lista)
  (cond ((null lista) t)
        ((or (alpha-char-p (car lista))
             (digit-char-p (car lista)))
         (alfanumerica (cdr lista)))
        (t nil)))


; funzione che determina se tutti gli elementi di una lista
; sono caratteri alfanumerici o "."
(defun alfanumerica. (lista)
  (cond ((null lista) t)
        ((or (alpha-char-p (car lista))
             (digit-char-p (car lista))
             (eql (car lista) #\.))
         (alfanumerica. (cdr lista)))
        (t nil)))


; funzione che determina se gli elementi di una lista sono lettere
(defun lettere (lista)
  (cond ((null lista) t)
        ((alpha-char-p (car lista)) (lettere (cdr lista)))
        (t nil)))