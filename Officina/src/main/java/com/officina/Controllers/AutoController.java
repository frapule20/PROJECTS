package com.officina.Controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.officina.Services.AutoService;
import com.officina.Services.ClienteService;

import jakarta.validation.Valid;

import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

import java.util.ArrayList;
import java.util.List;
import com.officina.Models.Auto;
import org.springframework.web.bind.annotation.PutMapping;

@Controller
public class AutoController {
    private AutoService autoService;
    private ClienteService clienteService;

    public AutoController(AutoService autoService, ClienteService clienteService) {
        this.autoService = autoService;
        this.clienteService = clienteService;
    }

    @GetMapping("/automobili")
    public String listAutoimobili(Model model) {
        List<Auto> automobili = autoService.findAllAuto();
        Auto selectedAuto = new Auto();
        model.addAttribute("selectedAuto", selectedAuto);
        model.addAttribute("automobili", automobili);
        return "./automobili/automobili-list";
    }

    @PostMapping("/automobili")
    public String listAutoimobili(
            @ModelAttribute("selectedAuto") Auto selectedAuto,
            @RequestParam(value = "mostraTutti", required = false) Boolean mostraTutti, Model model) {

        if (mostraTutti != null && mostraTutti) {
            // Se "Mostra tutti" è cliccato, mostra tutte le automobili e ignora i filtri di
            // ricerca
            List<Auto> automobili = autoService.findAllAuto();
            model.addAttribute("automobili", automobili);
            model.addAttribute("selectedAuto", new Auto()); // Pulisci i filtri di ricerca
            return "./automobili/automobili-list";
        }
        if (autoService.findAutoByTarga(selectedAuto.getTarga()) == null) {
            List<Auto> automobili = autoService.findAllAuto();
            model.addAttribute("automobili", automobili);
            return "./automobili/automobili-list";
        }
        selectedAuto = autoService.findAutoByTarga(selectedAuto.getTarga());
        List<Auto> automobili = new ArrayList<>();
        automobili.add(selectedAuto);
        model.addAttribute("automobili", automobili);
        return "./automobili/automobili-list";
    }

    @GetMapping("/automobili/{clienteId}/new")
    public String createAutoForm(@PathVariable("clienteId") Long clienteId, Model model) {
        Auto auto = new Auto();
        model.addAttribute("auto", auto);
        model.addAttribute("clienteId", clienteId);
        return "./automobili/automobili-create";
    }

    @GetMapping("/automobili/{autoId}/edit")
    public String editAutoForm(@PathVariable("autoId") Long autoId, Model model) {
        Auto auto = autoService.findAutoById(autoId);
        model.addAttribute("auto", auto);
        return "./automobili/automobili-edit";
    }

    @PostMapping("/automobili/{clienteId}/new")
    public String saveAuto(@PathVariable("clienteId") Long clienteId,
            @Valid @ModelAttribute("auto") Auto auto, BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("auto", auto);
            model.addAttribute("clienteId", clienteId);
            return "./automobili/automobili-create";
        } else if (autoService.findAutoByTarga(auto.getTarga()) != null) {
            model.addAttribute("errorMessage", "Hai provato ad inserire una macchina con una targa già esistente");
            return "./errors/input-error";
        } else {
            auto.setCliente(clienteService.findClienteById(clienteId));
            autoService.saveAuto(auto);
            return "redirect:/automobili";
        }
    }

    @PutMapping("/automobili/{autoid}")
    public String updateAuto(@PathVariable("autoid") Long autoid, @Valid @ModelAttribute("auto") Auto auto,
            BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("auto", auto);
            return "./automobili/automobili-edit";
        } else if (autoService.findAutoByTarga(auto.getTarga()) != null
                && autoService.findAutoByTarga(auto.getTarga()).getId() != auto.getId()) {
            model.addAttribute("errorMessage", "Hai provato ad inserire una macchina con una targa già esistente");
            return "./errors/input-error";
        } else {
            autoService.saveAuto(auto);
            return "redirect:/automobili/{autoid}";
        }
    }

    @DeleteMapping("/automobili/{autoid}")
    public String deleteAuto(@PathVariable("autoid") Long autoid) {
        autoService.delete(autoid);
        return "redirect:/automobili";
    }

    @GetMapping("/automobili/{autoid}")
    public String detailAuto(@PathVariable("autoid") Long autoid, Model model) {
        try {
            Auto auto = autoService.findAutoById(autoid);
            model.addAttribute("auto", auto);
            return "./automobili/automobili-detail";
        } catch (Exception e) {
            return "redirect:/errore";
        }
    }
}
