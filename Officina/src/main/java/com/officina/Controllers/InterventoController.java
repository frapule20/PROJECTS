package com.officina.Controllers;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.officina.Models.Intervento;
import com.officina.Models.Meccanico;
import com.officina.Models.Ricambio;
import com.officina.Models.Meccanico.Specializzazione;
import com.officina.Services.AutoService;
import com.officina.Services.InterventoService;
import com.officina.Services.MeccanicoService;
import com.officina.Services.RicambioService;

import jakarta.validation.Valid;

import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

@Controller
public class InterventoController {

    private InterventoService interventoService;
    private RicambioService ricambioService;
    private AutoService autoService;
    private MeccanicoService meccanicoService;

    public InterventoController(InterventoService interventoService, RicambioService ricambioService,
            AutoService autoService, MeccanicoService meccanicoService) {
        this.interventoService = interventoService;
        this.ricambioService = ricambioService;
        this.autoService = autoService;
        this.meccanicoService = meccanicoService;
    }

    @GetMapping("/interventi")
    public String interventoList(Model model) {
        List<Intervento> interventi = interventoService.findAllInterventi();
        Intervento selectedIntervento = new Intervento();
        List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
        model.addAttribute("allSpecializzazioni", allSpecializzazioni);
        model.addAttribute("selectedIntervento", selectedIntervento);
        model.addAttribute("interventi", interventi);
        return "./interventi/interventi-list";
    }

    @PostMapping("/interventi")
    public String searchInterventi(@ModelAttribute("selectedIntervento") Intervento selectedIntervento,
            @RequestParam(value = "mostraTutti", required = false) Boolean mostraTutti, Model model) {
        List<Intervento> interventi = new ArrayList<>();
        if (mostraTutti != null && mostraTutti) {
            // Se "Mostra tutti" è cliccato, mostra tutti gli interventi e ignora i filtri
            // di ricerca
            interventi = interventoService.findAllInterventi();
            List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
            model.addAttribute("allSpecializzazioni", allSpecializzazioni);
            model.addAttribute("selectedIntervento", new Intervento()); // Pulisci i filtri di ricerca
            model.addAttribute("interventi", interventi);
            return "./interventi/interventi-list";
        }
        Date dataInizio = selectedIntervento.getDataInizio();
        Date dataFine = selectedIntervento.getDataFine();
        Specializzazione specializzazione = selectedIntervento.getMeccanico().getSpecializzazione();
        if (specializzazione == null && dataInizio != null && dataFine != null) {
            interventi = interventoService.findByDataInizioDataFine(dataInizio, dataFine);
        } else if (specializzazione != null && dataInizio == null && dataFine == null) {
            interventi = interventoService.findBySpecializzazione(specializzazione);
        } else if (specializzazione != null && dataInizio != null && dataFine != null) {
            interventi = interventoService.findByDataInizioDataFineSpecializzazione(dataInizio, dataFine,
                    specializzazione);
        }
        List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
        model.addAttribute("allSpecializzazioni", allSpecializzazioni);
        model.addAttribute("selectedIntervento", selectedIntervento);
        model.addAttribute("interventi", interventi);
        return "./interventi/interventi-list";
    }

    @GetMapping("/interventi/{autoId}/new")
    public String createInterventoFormAuto(@PathVariable("autoId") Long autoId, Model model) {
        Intervento intervento = new Intervento();
        List<Ricambio> ricambi = ricambioService.findAllRicambi();
        List<Meccanico> allMeccanici = meccanicoService.findAllMeccanici();
        List<Meccanico> meccanici = new ArrayList<>();
        for (Meccanico m : allMeccanici) {
            if (m.getLicenza()) {
                meccanici.add(m);
            }
        }
        model.addAttribute("ricambi", ricambi);
        model.addAttribute("meccanici", meccanici);
        model.addAttribute("intervento", intervento);
        model.addAttribute("autoId", autoId);
        return "./interventi/interventi-create";
    }

    @PostMapping("/interventi/{autoId}")
    public String saveIntervento(@PathVariable("autoId") Long autoId,
            @Valid @ModelAttribute("intervento") Intervento intervento, BindingResult result,
            Model model) {
        List<Ricambio> ricambi = ricambioService.findAllRicambi();
        List<Meccanico> allMeccanici = meccanicoService.findAllMeccanici();
        List<Meccanico> meccanici = new ArrayList<>();
        for (Meccanico m : allMeccanici) {
            if (m.getLicenza()) {
                meccanici.add(m);
            }
        }
        model.addAttribute("meccanici", meccanici);
        model.addAttribute("ricambi", ricambi);
        model.addAttribute("autoId", autoId);
        if (result.hasErrors()) {
            return "./interventi/interventi-create";
        }
        intervento.setAuto(autoService.findAutoById(autoId));
        interventoService.saveIntervento(intervento);
        return "redirect:/interventi";
    }

    @GetMapping("/interventi/{interventoId}/edit")
    public String editInterventoForm(@PathVariable("interventoId") Long interventoId, Model model) {
        Intervento intervento = interventoService.findInterventoById(interventoId);
        List<Ricambio> ricambi = ricambioService.findAllRicambi();
        List<Ricambio> currentRicambi = intervento.getRicambi();
        model.addAttribute("intervento", intervento);
        model.addAttribute("allRicambi", ricambi);
        model.addAttribute("currentRicambi", currentRicambi);
        return "./interventi/interventi-edit";
    }

    @PutMapping("/interventi/{interventoId}")
    public String updateIntervento(@PathVariable("interventoId") Long interventoId,
            @Valid @ModelAttribute("intervento") Intervento intervento, BindingResult result,
            Model model) {
        Intervento oldIntervento = interventoService.findInterventoById(interventoId);
        if (result.hasErrors()) {
            List<Ricambio> allRicambi = ricambioService.findAllRicambi();
            List<Ricambio> currentRicambi = intervento.getRicambi();
            List<Long> currentRicambiId = new ArrayList<>();
            for (Ricambio ricambio : currentRicambi) {
                currentRicambiId.add(ricambio.getId());
            }
            model.addAttribute("intervento", intervento);
            model.addAttribute("allRicambi", allRicambi);
            model.addAttribute("currentRicambi", currentRicambiId);
            System.out.println("CASA");
            return "./interventi/interventi-edit";
        }
        intervento.setMeccanico(oldIntervento.getMeccanico());
        interventoService.updateIntervento(intervento);
        return "redirect:/interventi";
    }

    @GetMapping("/interventi/filtro")
    public String filtroInterventi(Model model) {
        return "./interventi/interventi-filter";
    }

    @DeleteMapping("/interventi/{interventoId}")
    public String deleteIntervento(@PathVariable("interventoId") Long interventoId) {
        interventoService.delete(interventoId);
        return "redirect:/interventi";
    }

    @GetMapping("/interventi/{interventoId}")
    public String viewDetailIntervento(@PathVariable("interventoId") Long interventoId, Model model) {
        try {
            Intervento intervento = interventoService.findInterventoById(interventoId);
            List<Meccanico> meccanici = meccanicoService.findAllMeccanici();
            meccanici.remove(intervento.getMeccanico());
            model.addAttribute("intervento", intervento);
            model.addAttribute("allMeccanici", meccanici);
            return "./interventi/interventi-detail";
        } catch (Exception e) {
            return "redirect:/errore";
        }
    }
}
