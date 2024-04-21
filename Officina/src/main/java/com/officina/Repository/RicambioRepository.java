package com.officina.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.officina.Models.Ricambio;

@Repository
public interface RicambioRepository extends JpaRepository<Ricambio, Long> {
    public Ricambio findById(long id);

    public List<Ricambio> findByNome(String nome);
}
