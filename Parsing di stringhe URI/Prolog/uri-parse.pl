

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 01/2022
% Linguaggi di programmazione
%     Prof. M. Antoniotti
%     Prof. P. Braione
%     Prof. G. Pasi
%     Prof. R. N. Penaloza
%     Prof. G. Vizzari
% Universita' degli studi di Milano-Bicocca
% autori:
%     Alberto Sormani
%     Francesca Pulera'
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% METODI RICHIESTI
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

uri_parse(URIString, URI) :-
	% Trasformo la stringa in una lista di codici (numero del carattere)
	string_to_list(URIString, URICodeList),
	% Trasformo la lista di codici in una lista di caratteri
	code_list_to_char_list(URICodeList, URIList),
	% Salto allo stato iniziale ("scheme")
	% Scheme, Userinfo, Host, Port, Path, Fragment, Query
	% sono tutti valori di ritorno
	fun_scheme(URIList, Scheme, Userinfo, Host, Port, Path, Query, Fragment),
	% Percorso l'automa,
	% converto tutte le parti dell'URI da List a String
	list_to_string(Scheme, SchemeOut),
	list_to_string(Userinfo, UserinfoOut),
        list_to_string(Host, HostOut),
	list_to_string(Port, PortOut),
	list_to_string(Path, PathOut),
	list_to_string(Fragment, FragmentOut),
	list_to_string(Query, QueryOut),
	% Imposto il port a 80 di default se Port = []
	port_default(PortOut, PortOut1),
	% Output delle componenti dell'URI
	URI = uri(SchemeOut,
		  UserinfoOut,
		  HostOut,
		  PortOut1,
		  PathOut,
		  QueryOut,
		  FragmentOut).


% da implementare
% URI-DISPLAY
uri_display(URI) :-
	URI =.. [_, Scheme, Userinfo, Host, Port, Path, Query, Fragment | _],
	write('\n'),
	write('\n'),
	write('Scheme: '), write(Scheme), write('\n'),
	write('Userinfo: '), write(Userinfo), write('\n'),
	write('Host: '), write(Host), write('\n'),
	write('Port: '), write(Port), write('\n'),
	write('Path: '), write(Path), write('\n'),
	write('Query: '), write(Query), write('\n'),
	write('Fragment: '), write(Fragment), write('\n'),
	!.
uri_display(URI, Stream) :-
	uri_display(URI),
	write('\n'),
	write(Stream),
	write('\n'), write('\n'),
	!.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% AUTOMA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% SCHEME
fun_scheme(URIList, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	% Riceve l'uri completo
	% Controllo che esistano i ":", altrimenti interrompo l'esecuzione
	member(':', URIList), !,
	% Separo lo Scheme dal resto dell'uri
	split_list(URIList, ':', Scheme, Lista),
	% Controllo che Scheme contenga caretteri accettati, altrimenti interrompo
	ctrl_id(Scheme), !,
	% Se trovo uno schema speciale, salto allo stato corrispondente
	% Se invece Lista e' vuota accetto
	% Altrimenti salto allo stato "userinfo"
	is_special_scheme(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment).


% Se trovo uno dei seguenti schemi speciali
% salto allo stato corrispondente
is_special_scheme(Lista, Scheme, Userinfo, Host, [], [], [], []) :-
	Scheme = ['m', 'a', 'i', 'l', 't', 'o'], !,
	fun_userinfo_mailto(Lista, Userinfo, Host).
is_special_scheme(Lista, Scheme, [], Host, [], [], [], []) :-
	Scheme = ['n', 'e', 'w', 's'], !,
	fun_host_special(Lista, Host).
is_special_scheme(Lista, Scheme, Userinfo, [], [], [], [], []) :-
	Scheme = ['t', 'e', 'l'], !,
	fun_userinfo_tel(Lista, Userinfo).
is_special_scheme(Lista, Scheme, Userinfo, [], [], [], [], []) :-
	Scheme = ['f', 'a', 'x'], !,
	fun_userinfo_tel(Lista, Userinfo).
is_special_scheme(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	% Se invece Lista e' vuota accetto,
	% altrimenti salto allo stato "userinfo"
	Scheme \= ['m', 'a', 'i', 'l', 't', 'o'], !,
	Scheme \= ['n', 'e', 'w', 's'], !,
	Scheme \= ['t', 'e', 'l'], !,
	Scheme \= ['f', 'a', 'x'], !,
	goto_userinfo(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment).


% Se Lista e' vuota accetto
goto_userinfo([], Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	Scheme \== ['z', 'o', 's'], !,
	Userinfo = [],
	Host = [],
	Port = [],
	Path = [],
	Query = [],
	Fragment = [].
% altrimenti salto allo stato "userinfo"
goto_userinfo(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	fun_userinfo(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment).


% USERINFO
% Riceve l'uri da dopo i ":"
% l'userinfo deve avere l'authorithy
fun_userinfo(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	% Controllo la presenza dell'authorithy
	nth1(1, Lista, /),
	nth1(2, Lista, /),
	!,

	% Se la trovo, rimuovo "//" dell'authorithy
	split_list(Lista, /, _, NL),
	split_list(NL, /, _, NNL),

	% Controllo la presenza di "@",
	% se la trovo memorizzo Userinfo fino a "@",
	% altrimenti salto direttamente allo stato "host"
	goto_host(NNL, Scheme, Userinfo, Host, Port, Path, Query, Fragment).
% o il path
fun_userinfo(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	% Se trovo lo "/"
	nth1(1, Lista, /), !,
	% allora salto direttamente allo stato "path",
	Userinfo = [],
	Host = [],
	Port = [],
	split_list(Lista, '/', _, NewLista),
	goto_path(NewLista, Scheme, Path, Query, Fragment).
% altrimenti c'e' un errore e interrompo
fun_userinfo(_, _, _, _, _, _, _, _) :-
	false.


% Controllo la presenza di "@"
% se la trovo memorizzo Userinfo fino a "@"
goto_host(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	member('@', Lista), !,
	% Memorizzo Userinfo
	split_list(Lista, '@', Userinfo, NewLista),
	% Controllo che sia corretto
	ctrl_id(Userinfo), !,
	fun_host(NewLista, Scheme, Host, Port, Path, Query, Fragment).
% altrimenti salto direttamente allo stato "host"
goto_host(Lista, Scheme, Userinfo, Host, Port, Path, Query, Fragment) :-
	not_member('@', Lista), !,
	% userinfo non c'e'
	Userinfo = [],
	fun_host(Lista, Scheme, Host, Port, Path, Query, Fragment).


% USERINFO MAILTO
fun_userinfo_mailto(Lista, Userinfo, Host) :-
	% Se trovo la "@"
	member('@', Lista), !,
	% Memorizzo Userinfo
	split_list(Lista, '@', Userinfo, NewLista),
	% Controllo che sia corretto
	ctrl_id(Userinfo), !,
	% e salto allo sato "host special"
	fun_host_special(NewLista, Host).
fun_userinfo_mailto(Lista, Userinfo, Host) :-
	% Se invece non trovo la "@"
	not_member('@', Lista), !,
	% allora non c'e' host
	Host = [],
	% e salto direttamente allo stato "userinfo tel"
	fun_userinfo_tel(Lista, Userinfo), !.


% USERNFO TEL E FAX
fun_userinfo_tel(Lista, Userinfo) :-
	% Controllo la lista (che e' tutto l'userinfo)
	ctrl_id(Lista), !,
	% Se e' corretta, memorizzo Userinfo e accetto
	Userinfo = Lista.


% HOST
% Controllo se c'e' il port
fun_host(Lista, Scheme, Host, Port, Path, Query, Fragment) :-
	% Se trovo i ":"
	member(':', Lista), !,
	% Controllo che i ":" siano veramente l'inizio di port
	% e non parte del path/query/fragment
	check_host(Lista, Scheme, Host, Port, Path, Query, Fragment).
% Controllo se c'e' invece il path
fun_host(Lista, Scheme, Host, [], Path, Query, Fragment) :-
	% Se trovo lo "/"
	member('/', Lista), !,
	% memorizzo Host
	split_list(Lista, '/', Host, NewLista),
	% Controllo se e' corretto
	ctrl_id_host(Host), !,
	% e salto allo stato "path"
	goto_path(NewLista, Scheme, Path, Query, Fragment).
% Altrimenti e' tutto host
fun_host(Lista, _, Host, [], [], [], []) :-
	% Quindi salto allo satato "host special"
	fun_host_special(Lista, Host).


% Se ":" e' parte del path allora
check_host(Lista, Scheme, Host, [], Path, Query, Fragment) :-
	split_list(Lista, ':', Temp, _),
	% Se trovo lo "/"
	member('/', Temp), !,
	% Rimemorizzo Host
	split_list(Lista, '/', Host, NewLista),
	% Controllo che sia corretto
	ctrl_id_host(Host), !,
	% Salto allo stato "path"
	goto_path(NewLista, Scheme, Path, Query, Fragment).
% Altrimenti
check_host(Lista, Scheme, Host, Port, Path, Query, Fragment) :-
	% Memorizzo Host
	split_list(Lista, ':', Host, NewLista),
	% Se invece non trovo lo "/"
	not_member('/', Host), !,
	% Controllo che sia corretto
	ctrl_id_host(Host), !,
	% Salto allo stato "port"
	fun_port(NewLista, Scheme, Port, Path, Query, Fragment).


% Se e' zos allosa salta allo stato "path zos"
goto_path(Lista, Scheme, Path, Query, Fragment) :-
	Scheme = ['z','o','s'], !,
	fun_path_zos(Lista, Path, Query, Fragment).
goto_path(Lista, Scheme, Path, Query, Fragment) :-
	Scheme \= ['z','o','s'], !,
	fun_path(Lista, Path, Query, Fragment).


% HOST SPECIAL
fun_host_special(Lista, Host) :-
	% Se la lista rispetta i parametri di
	% identificatore-host, allora accetto
	ctrl_id_host(Lista), !,
	Host = Lista.


% PORT
fun_port(Lista, Scheme, Port, Path, Query, Fragment) :-
	% Controllo che ci sia path/query/fragment
	member('/', Lista), !,
	% Memorizzo Port
	split_list(Lista, '/', Port, NewLista),
	% Controllo che Port sia corretto
	ctrl_port(Port), !,
	% Salto allo stato "path"
	goto_path(NewLista, Scheme, Path, Query, Fragment).
fun_port(Lista, _, Port, [], [], []) :-
	% Se invece il port non e' seguito da ninte
	not_member('/', Lista),
	% Allora e' tutto port
	% Lo controllo
	ctrl_port(Lista), !,
	% E accetto
	Port = Lista.


% PATH
% Controllo se c'e' subito la query
fun_path([H | Ts], Path, Query, Fragment) :-
	% Se trovo "?" come primo carattere
	'?' == H, !,
	% Allora Path e' nullo
	Path = [],
	% E salto allo stato "query"
	split_list([H | Ts], '?', _, NewLista),
	fun_query(NewLista, Query, Fragment).
% Controllo se c'e' subito il fragment
fun_path([H | Ts], Path, Query, Fragment) :-
	% Se trovo "#" come primo carattere
	'#' == H, !,
	% Allora Path e' nullo
	Path = [],
	% E anche Query
	Query = [],
	% E salto allo stato "fragment"
	fun_fragment([H | Ts], Fragment).
% Se incece c'e' una query dopo il path
fun_path(Lista, Path, Query, Fragment) :-
	% Se trovo "?" ma non come primo carattere
	member('?', Lista), !,
	% Allora memorizzo Path
	split_list(Lista, '?', TempPath, NewLista),
	% Controllo che "?" non sia parte del fragment
	check_path(Lista, NewLista, TempPath, Path, Query, Fragment).
fun_path(Lista, Path, Query, Fragment) :-
	% Se trovo "#" ma non come primo carattere
	member('#', Lista), !,
	% Allora memorizzo Path
	split_list(Lista, '#', Path, NewLista),
	% Quindi Query e' nulla
	Query = [],
	% Controllo che Path sia corretto
	ctrl_path(Path), !,
	% E salto allo stato "fragment"
	fun_fragment(NewLista, Fragment).
% Altrimenti se il path non e' seguito da niente
fun_path(Lista, Path, [], []) :-
	% Controllo che sia corretto
	% \+ Scheme = ['z','o','s'], !,
	ctrl_path(Lista),
	% E accetto
	Path = Lista.


check_path(Lista, _, TempPath, Path, Query, Fragment) :-
	% Se trovo "#" prima di "?"
	member('#', TempPath), !,
	% Rimemorizzo path
	split_list(Lista, '#', Path, NewLista),
	% Lo controllo
	ctrl_path(Path), !,
	% Quindi Query e' nulla
	Query = [],
	% Salto allo stato "fragment"
	fun_fragment(NewLista, Fragment).
check_path(_, NewLista, TempPath, Path, Query, Fragment) :-
	% Se invece non c'e' "#" prima di "?"
	not_member('#', TempPath), !,
	% Controllo Path
	ctrl_path(TempPath), !,
	Path = TempPath,
	% Salto allo stato "fragment"
	fun_query(NewLista, Query, Fragment).


% PATH ZOS
% Se la lista e' vuota, interrompo
% Se c'e' "?" come primo carattere, interrompo
% Se c'e' "#" come primo carattere, interrompo
% Se c'e' "(" come primo carattere, interrompo
fun_path_zos([H | Ts], Path, Query, Fragment) :-
	[] \= [H | Ts], !,
	'?' \= H, !,
	'#' \= H, !,
	'(' \= H, !,
	fun_path_zos_bis([H | Ts], Path, Query, Fragment).
% Se invece c'e' "(" ma non come primo carattere
fun_path_zos_bis(Lista, Path, Query, Fragment) :-
	member('(', Lista), !,
	% Memorizzo ID44
	split_list(Lista, '(', Id44, NewLista),
	% Controllo che ci sia anche ")"
	member(')', NewLista), !,
	% Se lo trovo, controllo che non sia parte di query/fragment
	check_id44(Lista, NewLista, Id44, Path, Query, Fragment), !.
% Altrimenti non c'e' l'ID8
fun_path_zos_bis(Lista, Path, Query, Fragment) :-
	goto_qf_bis(Lista, Path, Query, Fragment).


% Se "(" e parte di query
check_id44(OldLista, _, Id44, Path, Query, Fragment) :-
	member('?', Id44), !,
	% Rimemorizzo Id44, e quindi Path
	split_list(OldLista, '?', Path, NewLista),
	% Poi salto allo stato "query"
	fun_query(NewLista, Query, Fragment).
% Se "(" e parte di fragment
check_id44(_, Lista, Id44, Path, Query, Fragment) :-
	member('#', Id44), !,
	% Rimemorizzo Id44, e quindi Path
	split_list(Lista, '#', Path, NewLista),
	% Dunque Query e' nulla
	Query = [],
	% Poi salto allo stato "fragment"
	fun_fragment(NewLista, Fragment).
% Altrimenti se ID44 e' "corretto"
check_id44(OldLista, Lista, Id44, Path, Query, Fragment) :-
	% Controllo che Id44 sia effettivamente corretto
	% E nel caso non lo sia interrompo
	ctrl_id44(Id44), !,
	% Poi controllo Id8
	% E nel caso non lo sia interrompo
	split_list(Lista, ')', Id8, NewLista),
	ctrl_id8(Id8), !,
	% Memorizzo Path
	OldLista = Path,
	% Dopo controllo se ci sono query o fragment
	% Se invece ci sono altri caratteri, interrompo
	goto_qf(NewLista, Query, Fragment).


% Se e' nulla accetto
goto_qf([], [], []).
% Se c'e' la query
goto_qf([H | Ts], Query, Fragment) :-
	% Se il primo carattere e' "?"
	% Altrimenti interrompo
	'?' == H, !,
	split_list([H | Ts], '?', _, NewLista),
	% Salto allo stato "query"
	fun_query(NewLista, Query, Fragment).
% Se c'e' il fragment
goto_qf([H | Ts], Query, Fragment) :-
	% Se il primo carattere e' "#"
	% Altrimenti interrompo
	'#' == H, !,
	split_list([H | Ts], '#', _, NewLista),
	% Quindi Query e' nulla
	Query = [],
	% Salto allo stato "fragment"
	fun_fragment(NewLista, Fragment).
% Altrimenti se ci sono altri caratteri, interrompo
goto_qf(_, _, _) :- false.


% Se trovo "?" come primo carattere,
% oppure se trovo "#" come primo carattere,
% allora path zos e' nullo, quindi interrompo
goto_qf_bis([X | Xs], Path, Query, Fragment) :-
	'?' \= X, !,
	'#' \= X, !,
	goto_qf_bis_bis([X | Xs], Path, Query, Fragment).
% Se trovo query
goto_qf_bis_bis(Lista, Path, Query, Fragment) :-
	member('?', Lista), !,
	% Memorizzo Path (Id44)
	split_list(Lista, '?', Path, NewLista),
	% Controllo che sia corretto
	ctrl_id44(Path), !,
	% Salto allo stato "query"
	fun_query(NewLista, Query, Fragment).
% Se trovo fragment
goto_qf_bis_bis(Lista, Path, Query, Fragment) :-
	member('#', Lista), !,
	% Memorizzo Path (Id44)
	split_list(Lista, '?', Path, NewLista),
	% Controllo che sia corretto
	ctrl_id44(Path), !,
	% Quindi Query e' nullo
	Query = [],
	% Salto allo stato "fragment"
	fun_fragment(NewLista, Fragment), !.
% Altrimenti e' tutto Id44
goto_qf_bis_bis(Lista, Path, [], []) :-
	% Controllo che sia corretto
	ctrl_id44(Lista), !,
	% E accetto
	Path = Lista.

% QUERY
% Se e' nulla interrompo
fun_query([], _, _) :- !.
% Se il primo carattere e' "#", interrompo
fun_query([X | _], _ , _) :-
	'#' == X,
	fail.
% Altrimenti controllo se c'e' il fragment
fun_query(Lista, Query, Fragment) :-
	member('#', Lista), !,
	% Memorizzo Query
	split_list(Lista, '#', Query, NewLista),
	% Controllo che Query sia corretta
	ctrl_query(Query), !,
	% Salto allo stato "fragment"
	fun_fragment(NewLista, Fragment), !.
% Se invece non c'e' fragment allora
fun_query(Lista, Query, Fragment) :-
	% Controllo che Query sia corretta
	ctrl_query(Lista), !,
	% E accetto
	Query = Lista,
	% Naturalmente Fragment sara' nullo
	Fragment = [].


% FRAGMENT
% Altrimenti accetto
fun_fragment(Lista, Fragment) :-
	% Se e' nullo, interrompo
	Lista \= [], !,
	% Altrimenti accetto
	Fragment = Lista.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ALTRI METODI
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Converte una lista di codici numerici di cartatteri in caratteri reali
code_list_to_char_list([], []) :- !.
code_list_to_char_list([X | Xs], [Y | Ys]) :-
	char_code(Y, X),
	code_list_to_char_list(Xs, Ys).


% Converte una lista in una stringa
list_to_string(L, S) :-
	L = [],
	S = L,
	!.
list_to_string(L, S) :-
	string_to_atom(L, S),
	!.


% Divido una lista in due sottoliste grazie ad un carattere sentinella
% slpit_list(Lista, Sentinella, Sottolista pre sentinella, Sottolista
% post sentinella).
split_list([Sentinella|Ls], Sentinella, [], Ls) :- !.
split_list([L|Ls], Sentinella, [L|Xs], R) :-
	L \== Sentinella,
	split_list(Ls, Sentinella, Xs, R),
	!.


% IDENTIFICATORE
% Controllo che l'identificatore non contenga caratteri errati
% se ne trovo, interrompo
ctrl_id(X) :-
	X \= [], !,
	ctrl_id_bis(X), !.
ctrl_id_bis([]) :- !.
ctrl_id_bis([X | Xs]) :-
	X \= '/', !,
	X \= '?', !,
	X \= '#', !,
	X \= '@', !,
	X \= ':', !,
	ctrl_id_bis(Xs), !.
ctrl_id_bis(X) :-
	length(X, 1), !,
	nth0(0, X, Y), !,
	Y \= '/', !,
	Y \= '?', !,
	Y \= '#', !,
	Y \= '@', !,
	Y \= ':', !.


% IDENTIFICATORE-HOST
ctrl_id_host([]) :- false.
ctrl_id_host([X | Xs]) :-
	% Controllo il primo carattere
	X \= '.', !,
	% Controllo tutti i caratteri
	ctrl_id([X | Xs]), !,
	% Controllo ultimo carattere
	ctrl_id_host_bis(Xs), !.
ctrl_id_host_bis([X]) :-
	X == '.', false.
ctrl_id_host_bis([X]) :-
	X \= '.', !.
ctrl_id_host_bis([_ | Xs]) :-
	ctrl_id_host_bis(Xs).



% PORT
% Verifico che sia una lista di cifre
ctrl_port(C) :-
	C \= [], !,
	length(C, Temp),
	Temp < 6, !,
	ctrl_port_bis(C).
ctrl_port_bis([]) :- !.
ctrl_port_bis([C | Cs]) :-
	digit(C), !,
	ctrl_port_bis(Cs), !.
ctrl_port_bis([C]) :-
	digit(C).

digit('1').
digit('2').
digit('3').
digit('4').
digit('5').
digit('6').
digit('7').
digit('8').
digit('9').
digit('0').


% IDENTIFICATORE-PATH
% Controllo che l'identificatore non contenga caratteri errati
% se ne trovo, interrompo
ctrl_path([]).
ctrl_path([X]) :-
	X \= '/', !.
ctrl_path([X | Xs]) :-
	% Controllo il primo carattere
	X \= '/', !,
	% Controllo tutti i caratteri
	ctrl_path_body([X | Xs]), !,
	% Vado a controllare l'ultimo carattere
	ctrl_path_last(Xs), !.

ctrl_path_body([]).
ctrl_path_body([X | Xs]) :-
        X \= '?',
	X \= '#',
	X \= '@',
	X \= ':',
	ctrl_path_body(Xs), !.
ctrl_path_body(X) :-
	length(X, 1),
	X \= '?',
	X \= '#',
	X \= '@',
	X \= ':'.


ctrl_path_last([X]) :-
	X \= '/', !.
ctrl_path_last([_ | Xs]) :-
	ctrl_path_last(Xs).


% ID44
ctrl_id44([X]) :-
	is_alpha(X).
ctrl_id44([X | Xs]) :-
	[X | Xs] \= [],
	length([X | Xs], Temp),
	Temp < 45,
	is_alpha(X),
	ctrl_id44_body(Xs),
	ctrl_id44_last(Xs).


ctrl_id44_body([]).
ctrl_id44_body([X | Xs]) :-
	ctrl_id44_body(X), !,
	ctrl_id44_body(Xs), !.
ctrl_id44_body(X) :-
	is_digit(X).
ctrl_id44_body(X) :-
	is_alpha(X).
ctrl_id44_body(X) :-
	X = '.'.


ctrl_id44_last([X]) :-
	X \= '.', !.
ctrl_id44_last([_ | Xs]) :-
	ctrl_id44_last(Xs).


% ID8
ctrl_id8([]) :- false.
ctrl_id8([X]) :-
	ctrl_id8_bis(X).
ctrl_id8([X | Xs]) :-
	length([X | Xs], Temp),
	Temp < 9,
	ctrl_id8_bis(X),
	ctrl_id8(Xs).


ctrl_id8_bis(X) :-
	is_digit(X), !.
ctrl_id8_bis(X) :-
	is_alpha(X), !.


% QUERY
ctrl_query(X) :-
	X \= [],
	not_member('#', X).


% NOT member
not_member(_,[]).
not_member(Arg,[Arg|_]) :-
	!,
	fail.
not_member(Arg,[_|Tail]) :-
	!,
	not_member(Arg,Tail).

% Se il port e' vuoto gli assegna il valore di default
port_default([], 80) :- !.
port_default(P, P) :- !.


% Definisco la struttura dell'URI
uri([], _, _, _, _, _, _) :- false.
uri( _, _, _, _, _, _, _).















