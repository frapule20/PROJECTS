package com.officina.Services.impl;

import org.springframework.stereotype.Service;
import com.officina.Services.RicambioService;
import com.officina.Repository.RicambioRepository;
import com.officina.Models.Ricambio;

import java.util.List;

@Service
public class RicambioServiceImpl implements RicambioService {
    private RicambioRepository ricambioRepository;

    public RicambioServiceImpl(RicambioRepository ricambioRepository) {
        this.ricambioRepository = ricambioRepository;
    }

    @Override
    public List<Ricambio> findAllRicambi() {
        return ricambioRepository.findAll();
    }

    @Override
    public List<Ricambio> findByNome(String nome) {
        return ricambioRepository.findByNome(nome);
    }

    @Override
    public Ricambio saveRicambio(Ricambio ricambio) {
        return ricambioRepository.save(ricambio);
    }

    @Override
    public Ricambio findRicambioById(Long ricambioId) {
        return ricambioRepository.findById(ricambioId).get();
    }

    @Override
    public void updateRicambio(Ricambio ricambio) {
        ricambioRepository.save(ricambio);
    }

    @Override
    public void delete(Long ricambioId) {
        ricambioRepository.deleteById(ricambioId);
    }
}
