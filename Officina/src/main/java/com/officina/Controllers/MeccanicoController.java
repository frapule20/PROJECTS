package com.officina.Controllers;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.officina.Models.Intervento;
import com.officina.Models.Meccanico;
import com.officina.Models.Meccanico.Specializzazione;
import com.officina.Services.InterventoService;
import com.officina.Services.MeccanicoService;

import jakarta.validation.Valid;

@Controller
public class MeccanicoController {

    MeccanicoService meccanicoService;
    InterventoService interventoService;

    public MeccanicoController(MeccanicoService meccanicoService, InterventoService interventoService) {
        this.meccanicoService = meccanicoService;
        this.interventoService = interventoService;
    }

    @GetMapping("/meccanici")
    public String listMeccanici(Model model) {
        List<Meccanico> meccanici = meccanicoService.findAllMeccanici();
        Meccanico selectedMeccanico = new Meccanico();
        List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
        model.addAttribute("allSpecializzazioni", allSpecializzazioni);
        model.addAttribute("selectedMeccanico", selectedMeccanico);
        model.addAttribute("meccanici", meccanici);
        return "./meccanici/meccanici-list";
    }

    @PostMapping("/meccanici")
    public String searchMeccanici(@ModelAttribute("selectedMeccanico") Meccanico selectedMeccanico,
            @RequestParam(value = "mostraTutti", required = false) Boolean mostraTutti, Model model) {
        List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
        model.addAttribute("allSpecializzazioni", allSpecializzazioni);
        model.addAttribute("selectedMeccanico", new Meccanico()); // Pulisci i filtri di ricerca
        if (mostraTutti != null && mostraTutti) {
            // Se "Mostra tutti" è cliccato, mostra tutti i meccanici e ignora i filtri di
            // ricerca
            List<Meccanico> meccanici = meccanicoService.findAllMeccanici();
            model.addAttribute("meccanici", meccanici);
            return "./meccanici/meccanici-list";
        }

        Specializzazione specializzazione = selectedMeccanico.getSpecializzazione();
        List<Meccanico> meccanici = meccanicoService.findMeccaniciBySpecializzazione(specializzazione);
        model.addAttribute("meccanici", meccanici);
        // Reimposta il campo specializzazione a null
        return "./meccanici/meccanici-list";
    }

    @GetMapping("/meccanici/new")
    public String createMeccanicoForm(Model model) {
        Meccanico meccanico = new Meccanico();
        List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
        model.addAttribute("allSpecializzazioni", allSpecializzazioni);
        model.addAttribute("meccanico", meccanico);

        return "./meccanici/meccanici-create";
    }

    @PostMapping("/meccanici/new")
    public String saveMeccanico(@Valid @ModelAttribute("meccanico") Meccanico meccanico, BindingResult result,
            Model model) {
        if (result.hasErrors()) {
            model.addAttribute("meccanico", meccanico);
            return "./meccanici/meccanici-create";
        } else if (meccanicoService.findMeccanicoByEmail(meccanico.getEmail()) != null) {
            model.addAttribute("errorMessage",
                    "Hai provato ad inserire un meccanico con una mail o numero di telefono già esistente");
            return "./errors/input-error";
        } else {
            meccanicoService.saveMeccanico(meccanico);
            return "redirect:/meccanici";
        }
    }

    @GetMapping("/meccanici/{meccanicoId}/edit")
    public String editMeccanicoForm(@PathVariable("meccanicoId") Long meccanicoId, Model model) {
        Meccanico mainMeccanico = meccanicoService.findMeccanicoById(meccanicoId);
        List<Meccanico> allMeccanici = meccanicoService.findAllMeccanici();
        Long id = mainMeccanico.getId();
        for (Meccanico meccanico : meccanicoService.findAllMeccanici()) {
            if (meccanico.getAssistente().contains(mainMeccanico) && meccanico.getId() != id) {
                allMeccanici.remove(meccanico);
            }
        }
        allMeccanici.remove(mainMeccanico);
        List<Specializzazione> allSpecializzazioni = Arrays.asList(Specializzazione.values());
        model.addAttribute("allSpecializzazioni", allSpecializzazioni);
        model.addAttribute("meccanico", mainMeccanico);
        model.addAttribute("allMeccanici", allMeccanici);
        return "./meccanici/meccanici-edit";
    }

    @PutMapping("/meccanici/{meccanicoId}")
    public String updateMeccanico(@PathVariable("meccanicoId") Long meccanicoId,
            @Valid @ModelAttribute("meccanico") Meccanico meccanico,
            BindingResult result, Model model) {
        long firstId = meccanico.getId();
        long secondId = meccanicoService.findMeccanicoByEmail(meccanico.getEmail()).getId();
        if (result.hasErrors()) {
            model.addAttribute("meccanico", meccanico);
            return "./meccanici/meccanici-edit";
        } else if (meccanicoService.findMeccanicoByEmail(meccanico.getEmail()) != null
                && firstId != secondId) {
            model.addAttribute("errorMessage",
                    "Hai provato ad inserire un meccanico con una mail o numero di telefono già esistente");
            return "./errors/input-error";
        } else {
            // Controlla se l'attributo "licenza" è impostato a false
            if (!meccanico.getLicenza()) {
                // Se la licenza è false, rimuovi tutti gli assistenti
                meccanico.setAssistente(new ArrayList<>());
            }

            meccanicoService.saveMeccanico(meccanico);
            return "redirect:/meccanici/{meccanicoId}";
        }
    }

    @PostMapping("/meccanici/{meccanicoId}/assistenti")
    public String addAssistente(@PathVariable("meccanicoId") Long meccanicoId,
            @Valid @ModelAttribute("meccanico") Meccanico meccanico, Model model) {
        meccanicoService.saveMeccanico(meccanico);
        return "redirect:/meccanici";
    }

    @GetMapping("/meccanici/{meccanicoId}")
    public String viewDetailMeccanico(@PathVariable("meccanicoId") Long meccanicoId, Model model) {
        try {
            Meccanico meccanico = meccanicoService.findMeccanicoById(meccanicoId);
            model.addAttribute("meccanico", meccanico);
            return "./meccanici/meccanici-detail";
        } catch (Exception e) {
            return "redirect:/errore";
        }
    }

    @DeleteMapping("/meccanici/{meccanicoId}")
    public String deleteMeccanico(@PathVariable("meccanicoId") Long meccanicoId) {
        Meccanico m = meccanicoService.findMeccanicoById(meccanicoId);
        List<Meccanico> assistiti = m.getAssistito();

        HashMap<Meccanico, List<Intervento>> mi = new HashMap<Meccanico, List<Intervento>>();

        for (Meccanico a : assistiti) {
            mi.put(a, a.getInterventiList());
        }
        meccanicoService.delete(meccanicoId);

        for (Meccanico a : assistiti) {
            List<Intervento> l1 = mi.get(a);
            a.setInterventiList(null);
            meccanicoService.saveMeccanico(a);
            for (Intervento i : l1) {
                i.setMeccanico(a);
                interventoService.saveIntervento(i);
            }
        }

        return "redirect:/meccanici";
    }

}
