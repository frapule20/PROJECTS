package com.officina.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.officina.Models.Meccanico;
import com.officina.Models.Meccanico.Specializzazione;

@Repository
public interface MeccanicoRepository extends JpaRepository<Meccanico, Long> {
    public Meccanico findById(long id);

    public Meccanico findByEmail(String email);

    public List<Meccanico> findBySpecializzazione(Specializzazione specializzazione);

}
