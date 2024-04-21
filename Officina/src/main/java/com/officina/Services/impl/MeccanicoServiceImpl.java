package com.officina.Services.impl;

import java.util.List;

import org.springframework.stereotype.Service;

import com.officina.Models.Meccanico;
import com.officina.Models.Meccanico.Specializzazione;
import com.officina.Repository.MeccanicoRepository;
import com.officina.Services.MeccanicoService;

@Service
public class MeccanicoServiceImpl implements MeccanicoService {

    MeccanicoRepository meccanicoRepository;

    public MeccanicoServiceImpl(MeccanicoRepository meccanicoRepository) {
        this.meccanicoRepository = meccanicoRepository;
    }

    @Override
    public List<Meccanico> findAllMeccanici() {
        return meccanicoRepository.findAll();
    }

    @Override
    public List<Meccanico> findMeccaniciBySpecializzazione(Specializzazione specializzazione) {
        return meccanicoRepository.findBySpecializzazione(specializzazione);
    }

    @Override
    public Meccanico findMeccanicoById(Long meccanicoId) {
        return meccanicoRepository.findById(meccanicoId).get();
    }

    @Override
    public Meccanico findMeccanicoByEmail(String email) {
        return meccanicoRepository.findByEmail(email);
    }

    @Override
    public Meccanico saveMeccanico(Meccanico meccanico) {
        return meccanicoRepository.save(meccanico);
    }

    @Override
    public void updateMeccanico(Meccanico meccanico) {
        meccanicoRepository.save(meccanico);
    }

    @Override
    public void delete(Long meccanicoId) {
        meccanicoRepository.deleteById(meccanicoId);
    }

}
