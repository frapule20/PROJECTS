package com.officina.Repository;

import java.util.Date;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.officina.Models.Intervento;
import com.officina.Models.Meccanico.Specializzazione;

@Repository
public interface InterventoRepository extends JpaRepository<Intervento, Long> {
        public Intervento findById(long id);

        @Query("SELECT i FROM Intervento i INNER JOIN Meccanico m ON i.meccanico.id = m.id WHERE i.dataInizio >= :dataInizio AND i.dataFine <= :dataFine AND m.specializzazione = :specializzazione") // VA
        public List<Intervento> findByDataInizioDataFineSpecializzazione(@Param("dataInizio") Date dataInizio,
                        @Param("dataFine") Date dataFine, @Param("specializzazione") Specializzazione specializzazione);

        @Query("SELECT i FROM Intervento i WHERE i.dataInizio >= :dataInizio AND i.dataFine <= :dataFine")
        public List<Intervento> findByDataInizioDataFine(@Param("dataInizio") Date dataInizio,
                        @Param("dataFine") Date dataFine);

        @Query("SELECT i FROM Intervento i INNER JOIN Meccanico m ON i.meccanico.id = m.id WHERE m.specializzazione = :specializzazione")
        public List<Intervento> findByMeccanicoSpecializzazione(
                        @Param("specializzazione") Specializzazione specializzazione);

}
