package com.officina.Services.impl;

import org.springframework.stereotype.Service;

import com.officina.Models.Auto;
import com.officina.Models.Intervento;
import com.officina.Models.Meccanico.Specializzazione;
import com.officina.Repository.AutoRepository;
import com.officina.Repository.InterventoRepository;
import com.officina.Repository.RicambioRepository;
import com.officina.Services.InterventoService;

import jakarta.transaction.Transactional;

import java.util.Date;
import java.util.List;

@Service
public class InterventoServiceImpl implements InterventoService {
    private InterventoRepository interventoRepository;
    private AutoRepository autoRepository;

    public InterventoServiceImpl(InterventoRepository interventoRepository, AutoRepository autoRepository,
            RicambioRepository ricambioRepository) {
        this.interventoRepository = interventoRepository;
        this.autoRepository = autoRepository;
    }

    @Transactional
    @Override
    public void createIntervento(Long autoId, Intervento intervento) {
        Auto auto = autoRepository.findById(autoId).get();
        intervento.setAuto(auto);
        interventoRepository.save(intervento);
    }

    @Override
    public List<Intervento> findAllInterventi() {
        return interventoRepository.findAll();
    }

    @Override
    public List<Intervento> findByDataInizioDataFineSpecializzazione(Date dataInizio, Date dataFine,
            Specializzazione specializzazione) {
        return interventoRepository.findByDataInizioDataFineSpecializzazione(dataInizio, dataFine, specializzazione);
    }

    @Override
    public List<Intervento> findByDataInizioDataFine(Date dataInizio, Date dataFine) {
        return interventoRepository.findByDataInizioDataFine(dataInizio, dataFine);
    }

    @Override
    public List<Intervento> findBySpecializzazione(Specializzazione specializzazione) {
        return interventoRepository.findByMeccanicoSpecializzazione(specializzazione);
    }

    @Override
    public Intervento findInterventoById(Long id) {
        return interventoRepository.findById(id).get();
    }

    @Override
    public Intervento saveIntervento(Intervento intervento) {
        return interventoRepository.save(intervento);
    }

    @Override
    public void updateIntervento(Intervento intervento) {
        interventoRepository.save(intervento);
    }

    @Override
    public void delete(Long id) {
        interventoRepository.deleteById(id);
    }
}
