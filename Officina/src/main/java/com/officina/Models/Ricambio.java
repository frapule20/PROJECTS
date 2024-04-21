package com.officina.Models;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.SequenceGenerator;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Builder
public class Ricambio {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ricambio_seq")
    @SequenceGenerator(name = "ricambio_seq", sequenceName = "ricambio_seq", initialValue = 100)
    private Long id;
    @NotEmpty(message = "Inserisci il nome del pezzo di ricambio")
    private String nome;
    private double costoUnitario;

    @ManyToMany(mappedBy = "ricambi", cascade = CascadeType.REMOVE)
    private List<Intervento> interventoList;

    public void setInterventoList(List<Intervento> interventoList) {
        this.interventoList = interventoList;
    }

    public List<Intervento> getInterventoList() {
        return interventoList;
    }

    @Override
    public String toString() {
        return "Ricambio{" +
                "id=" + id +
                ", nome='" + nome + '\'' +
                ", costoUnitario=" + costoUnitario +
                '}';
    }
}
