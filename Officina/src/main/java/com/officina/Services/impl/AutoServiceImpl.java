package com.officina.Services.impl;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import com.officina.Models.Auto;
import com.officina.Repository.AutoRepository;
import com.officina.Services.AutoService;

@Service
public class AutoServiceImpl implements AutoService {
    private AutoRepository autoRepository;

    public AutoServiceImpl(AutoRepository autoRepository) {
        this.autoRepository = autoRepository;
    }

    @Override
    public List<Auto> findAllAuto() {
        return autoRepository.findAll();
    }

    @Override
    public Auto saveAuto(Auto auto) {
        return autoRepository.save(auto);
    }

    @Transactional
    @Override
    public Auto findAutoById(Long autoId) {
        try {
            return autoRepository.findById(autoId).get();
        } catch (Exception e) {
            return null;
        }
    }

    @Override
    public Auto findAutoByTarga(String targa) {
        try {
            return autoRepository.findByTarga(targa).get();
        } catch (Exception e) {
            return null;
        }
    }

    @Transactional(propagation = Propagation.NEVER)
    @Override
    public void updateAuto(Auto auto) {
        autoRepository.save(auto);
    }

    @Transactional(propagation = Propagation.NEVER)
    @Override
    public void delete(Long autoId) {
        autoRepository.deleteById(autoId);
    }

}
