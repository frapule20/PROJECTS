package com.officina.Models;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.OneToMany;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@AllArgsConstructor
@Entity
public class Meccanico extends Persona {
    @Enumerated(EnumType.ORDINAL)
    @NotNull(message = "Inserisci specializzazione del meccanico")
    private Specializzazione specializzazione;
    private boolean licenza;

    @ManyToMany(mappedBy = "assistente", cascade = { CascadeType.REMOVE })
    private List<Meccanico> assistito;

    @ManyToMany
    @JoinTable(name = "assistenza", joinColumns = @JoinColumn(name = "assistito_id"), inverseJoinColumns = @JoinColumn(name = "assistente_id"))
    private List<Meccanico> assistente;

    @OneToMany(mappedBy = "meccanico", cascade = CascadeType.REMOVE)
    private List<Intervento> interventiList;

    public boolean getLicenza() {
        return this.licenza;
    }

    @Override
    public String toString() {
        return "ToString() di Meccanico";
    }

    public enum Specializzazione {
        MOTORE,
        ELETTRONICA,
        GOMMISTA,
        CARROZZIERE,
        VERNICIATORE,
    }

    public Long getId() {
        return super.getId();
    }
}
