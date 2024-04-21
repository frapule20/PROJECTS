package com.officina.Services;

import java.util.List;

import com.officina.Models.Ricambio;

public interface RicambioService {
    List<Ricambio> findAllRicambi();

    List<Ricambio> findByNome(String nome);

    Ricambio saveRicambio(Ricambio ricambio);

    Ricambio findRicambioById(Long ricambioId);

    void updateRicambio(Ricambio ricambio);

    void delete(Long ricambioId);

}
