package com.officina.Models;

import java.util.Date;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.util.List;

import org.springframework.format.annotation.DateTimeFormat;

import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Builder
@Table
public class Intervento {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "intervento_seq")
    @SequenceGenerator(name = "intervento_seq", sequenceName = "intervento_seq", initialValue = 100)
    @NotNull(message = "La descrizione non può essere null")
    private String descrizione;

    @NotNull(message = "La data di inizio intervento non può essere null")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date dataInizio;

    @NotNull(message = "La data di fine intervento non può essere null")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date dataFine;

    @ManyToOne
    @JoinColumn(name = "meccanico_id")
    @NotNull(message = "Devi creare almeno un meccanico per creare un intervento")
    private Meccanico meccanico;

    @ManyToOne
    @JoinColumn(name = "auto_id", nullable = false)
    private Auto auto;

    @ManyToMany
    @JoinTable(name = "utilizzo", joinColumns = @JoinColumn(name = "intervento_id"), inverseJoinColumns = @JoinColumn(name = "ricambio_id"))
    private List<Ricambio> ricambi;

    public void setRicambi(List<Ricambio> ricambi) {
        this.ricambi = ricambi;
    }

    public List<Ricambio> getRicambi() {
        return ricambi;
    }
}