package com.officina.Controllers;

import org.springframework.stereotype.Controller;

import com.officina.Services.InterventoService;
import com.officina.Services.RicambioService;

import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

import java.util.List;

import com.officina.Models.Intervento;
import com.officina.Models.Ricambio;

@Controller
public class RicambioController {

    private RicambioService ricambioService;
    private InterventoService interventoService;

    public RicambioController(RicambioService ricambioService, InterventoService interventoService) {
        this.ricambioService = ricambioService;
        this.interventoService = interventoService;
    }

    @GetMapping("/ricambi")
    public String listRicambi(Model model) {
        List<Ricambio> ricambi = ricambioService.findAllRicambi();
        Ricambio selectedRicambio = new Ricambio();
        model.addAttribute("ricambi", ricambi);
        model.addAttribute("selectedRicambio", selectedRicambio);
        return "./ricambi/ricambi-list";
    }

    @PostMapping("/ricambi")
    public String searchRicambi(@ModelAttribute("selectedRicambio") Ricambio selectedRicambio,
            @RequestParam(value = "mostraTutti", required = false) Boolean mostraTutti, Model model) {
        if (mostraTutti != null && mostraTutti) {
            // Se "Mostra tutti" è cliccato, mostra tutti i clienti e ignora i filtri di
            // ricerca
            List<Ricambio> ricambi = ricambioService.findAllRicambi();
            model.addAttribute("ricambi", ricambi);
            model.addAttribute("selectedRicambio", new Ricambio()); // Pulisci i filtri di ricerca
            return "./ricambi/ricambi-list";
        }

        String nome = selectedRicambio.getNome();
        List<Ricambio> ricambi = ricambioService.findByNome(nome);
        model.addAttribute("ricambi", ricambi);
        return "./ricambi/ricambi-list";
    }

    @GetMapping("/ricambi/new")
    public String createRicambioForm(Model model) {
        Ricambio ricambio = new Ricambio();
        model.addAttribute("ricambio", ricambio);
        return "./ricambi/ricambi-create";
    }

    @PostMapping("/ricambi/new")
    public String saveRicambio(@Valid @ModelAttribute("ricambio") Ricambio ricambio, BindingResult result,
            Model model) {
        if (result.hasErrors()) {
            model.addAttribute("ricambio", ricambio);
            return "./ricambi/ricambi-create";
        } else {
            ricambioService.saveRicambio(ricambio);
            return "redirect:/ricambi";
        }
    }

    @GetMapping("/ricambi/{ricambioId}/edit")
    public String editRicambioForm(@PathVariable("ricambioId") Long ricambioId, Model model) {
        Ricambio ricambio = ricambioService.findRicambioById(ricambioId);
        model.addAttribute("ricambio", ricambio);
        return "./ricambi/ricambi-edit";
    }

    @PutMapping("/ricambi/{ricambioId}")
    public String updateRicambio(@Valid @ModelAttribute("ricambio") Ricambio ricambio,
            BindingResult result,
            Model model) {
        if (result.hasErrors()) {
            model.addAttribute("ricambio", ricambio);
            return "./ricambi/ricambi-edit";
        } else {
            ricambioService.saveRicambio(ricambio);
            return "redirect:/ricambi";
        }
    }

    @GetMapping("/ricambi/{ricambioId}")
    public String viewDetailCliente(@PathVariable("ricambioId") Long ricambioId, Model model) {
        try {
            Ricambio ricambio = ricambioService.findRicambioById(ricambioId);
            model.addAttribute("ricambio", ricambio);
            return "./ricambi/ricambi-detail";
        } catch (Exception e) {
            return "redirect:/errore";
        }
    }

    @DeleteMapping("/ricambi/{ricambioId}")
    public String deleteRicambio(@PathVariable("ricambioId") Long ricambioId) {
        Ricambio r = ricambioService.findRicambioById(ricambioId);
        List<Intervento> interventiList = r.getInterventoList();
        for (Intervento i : interventiList) {
            i.getRicambi().remove(r);
        }
        interventoService.delete(ricambioId);
        ricambioService.delete(ricambioId);
        for (Intervento intervento : interventiList) {
            interventoService.saveIntervento(intervento);
        }
        return "redirect:/ricambi";

    }
}
