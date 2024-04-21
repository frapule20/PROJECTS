package com.officina.Models;

import java.util.Date;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.PastOrPresent;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.util.List;

import org.springframework.format.annotation.DateTimeFormat;

import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@AllArgsConstructor
@Entity

public class Cliente extends Persona {
    @Pattern(regexp = "^(\\((00|\\+)39\\)|(00|\\+)39)?(38[890]|34[1-90]|36[680]|33[1-90]|32[89]|32[1-90]|39[1-90])\\d{7}$", message="Numero di telefono non valido")
    private String telefono;

    @NotNull(message = "La data di inizio intervento non può essere null")
    @PastOrPresent(message = "Data non valida")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date dataRegistrazione;

    @OneToMany(mappedBy = "cliente", cascade = CascadeType.REMOVE)
    private List<Auto> autoList;

    @Override
    public String toString() {
        return "Cliente";
    }

    public Long getId() {
        return super.getId();
    }
}
