package com.officina.Services;

import java.util.Date;
import java.util.List;

import com.officina.Models.Intervento;
import com.officina.Models.Meccanico.Specializzazione;

public interface InterventoService {

    void createIntervento(Long autoId, Intervento intervento);

    List<Intervento> findAllInterventi();

    List<Intervento> findByDataInizioDataFineSpecializzazione(Date dataInizio, Date dataFine,
            Specializzazione specializzaazione);

    List<Intervento> findByDataInizioDataFine(Date dataInizio, Date dataFine);

    List<Intervento> findBySpecializzazione(Specializzazione specializzazione);

    Intervento saveIntervento(Intervento intervento);

    Intervento findInterventoById(Long interventoId);

    void updateIntervento(Intervento intervento);

    void delete(Long interventoId);

}
