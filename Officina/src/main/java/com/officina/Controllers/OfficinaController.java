package com.officina.Controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.ui.Model;

@Controller
public class OfficinaController {

    @GetMapping("/officina")
    public String officina(Model model) {
        return "layout.html";
    }

    @GetMapping("/contattaci")
    public String contattaci(Model model) {
        return "contattaci.html";
    }

    @GetMapping("/privacy")
    public String privacy(Model model) {
        return "privacy.html";
    }

    @GetMapping("/errore")
    public String errore(Model model) {
        return "./errors/risorsa-non-trovata.html";
    }
}
