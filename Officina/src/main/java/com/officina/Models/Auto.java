package com.officina.Models;

import java.util.List;

import lombok.Builder;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.SequenceGenerator;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
public class Auto {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "auto_seq")
    @SequenceGenerator(name = "auto_seq", sequenceName = "auto_seq", initialValue = 100)
    private Long id;

    @NotEmpty(message = "La targa della macchina non dovrebbe essere vuoto")
    @Pattern(regexp = "(?!EE)(?!Ee)(?!eE)(?!ee)[A-HJ-NPR-TV-Za-hj-npr-tv-z]{2}\\d{3}[A-HJ-NPR-TV-Za-hj-npr-tv-z]{2}\\b", message = "Formato della targa non valido")
    @Size(min = 7, max = 7, message = "Lunghezza della targa non valida")
    private String targa;

    @NotEmpty(message = "Il modello della macchina non dovrebbe essere vuoto")
    private String modello;

    @NotNull(message = "L'anno di produzione non dovrebbe essere vuoto")
    @Min(value = 1886, message = "L'anno di produzione deve essere maggiore o uguale a 1886")
    @Max(value = 2024, message = "L'anno di produzione non è corretto")
    private int annoProduzione;

    @NotEmpty(message = "Il colore non dovrebbe essere vuoto")
    private String colore;

    @NotNull(message = "Il campo cilindrata non dovrebbe essere vuoto")
    private int cilindrata;

    @ManyToOne
    @JoinColumn(name = "cliente_id")
    private Cliente cliente;

    @OneToMany(mappedBy = "auto", cascade = CascadeType.REMOVE)
    private List<Intervento> interventoList;

    @Override
    public String toString() {
        return "Auto";
    }
}