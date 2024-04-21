package com.officina.Services;

import java.util.List;

import com.officina.Models.Auto;

public interface AutoService {
    List<Auto> findAllAuto();

    Auto saveAuto(Auto auto);

    Auto findAutoById(Long autoId);

    Auto findAutoByTarga(String targa);

    void updateAuto(Auto auto);

    void delete(Long autoId);
}
