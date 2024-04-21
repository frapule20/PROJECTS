package com.officina.Services;

import java.util.List;

import com.officina.Models.Meccanico;
import com.officina.Models.Meccanico.Specializzazione;

public interface MeccanicoService {

    List<Meccanico> findAllMeccanici();

    List<Meccanico> findMeccaniciBySpecializzazione(Specializzazione specializzazione);

    Meccanico findMeccanicoById(Long meccanicoId);

    Meccanico findMeccanicoByEmail(String email);

    Meccanico saveMeccanico(Meccanico meccanico);

    void updateMeccanico(Meccanico meccanico);

    void delete(Long meccanicoId);
}
