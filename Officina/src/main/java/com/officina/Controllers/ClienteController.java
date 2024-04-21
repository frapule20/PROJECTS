package com.officina.Controllers;

import java.util.ArrayList;
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

import com.officina.Models.Cliente;
import com.officina.Services.ClienteService;

import jakarta.validation.Valid;

@Controller
public class ClienteController {
    ClienteService clienteService;

    public ClienteController(ClienteService clienteService) {
        this.clienteService = clienteService;
    }

    @GetMapping("/clienti")
    public String listClienti(Model model) {
        List<Cliente> clienti = clienteService.findAllClientes();
        Cliente selectedCliente = new Cliente();
        model.addAttribute("selectedCliente", selectedCliente);
        model.addAttribute("clienti", clienti);
        return "./clienti/clienti-list";
    }

    @PostMapping("/clienti")
    public String searchClienti(@ModelAttribute("selectedCliente") Cliente selectedCliente,
            @RequestParam(value = "mostraTutti", required = false) Boolean mostraTutti, Model model) {
        if (mostraTutti != null && mostraTutti) {
            // Se "Mostra tutti" è cliccato, mostra tutti i clienti e ignora i filtri di
            // ricerca
            List<Cliente> clienti = clienteService.findAllClientes();
            model.addAttribute("clienti", clienti);
            model.addAttribute("selectedCliente", new Cliente()); // Pulisci i filtri di ricerca
            return "./clienti/clienti-list";
        }
        String nome = selectedCliente.getNome();
        String cognome = selectedCliente.getCognome();
        List<Cliente> clienti = new ArrayList<>();
        if (nome != null && !nome.isEmpty() && (cognome != null && !cognome.isEmpty())) {
            // Se è fornito sia il nome che il cognome
            clienti = clienteService.findClienteByNomeAndCognome(nome, cognome);
        } else if (nome != null && !nome.isEmpty() && (cognome == null || cognome.isEmpty())) {
            // Se è fornito solo il nome
            clienti = clienteService.findClienteByNome(nome);
        } else if ((nome == null || nome.isEmpty()) && cognome != null && !cognome.isEmpty()) {
            // Se è fornito solo il cognome
            clienti = clienteService.findClienteByCognome(cognome);
        }
        model.addAttribute("clienti", clienti);
        return "./clienti/clienti-list";

    }

    @GetMapping("/clienti/new")
    public String createClienteForm(Model model) {
        Cliente cliente = new Cliente();
        model.addAttribute("cliente", cliente);
        return "./clienti/clienti-create";
    }

    @PostMapping("/clienti/new")
    public String saveCliente(@Valid @ModelAttribute("cliente") Cliente cliente, BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("cliente", cliente);
            return "./clienti/clienti-create";
        } else if (clienteService.findClienteByEmail(cliente.getEmail()) != null
                || clienteService.findClienteByTelefono(cliente.getTelefono()) != null) {
            model.addAttribute("errorMessage",
                    "Hai provato ad inserire un cliente con una email o numero di telefono già esistente");
            return "./errors/input-error";
        } else {
            clienteService.saveCliente(cliente);
            return "redirect:/clienti";
        }
    }

    @GetMapping("/clienti/{clienteId}/edit")
    public String editClienteForm(@PathVariable("clienteId") Long clienteId, Model model) {
        Cliente cliente = clienteService.findClienteById(clienteId);
        model.addAttribute("cliente", cliente);
        return "./clienti/clienti-edit";
    }

    @PutMapping("/clienti/{clienteId}")
    public String updateCliente(@PathVariable("clienteId") Long clienteId,
            @Valid @ModelAttribute("cliente") Cliente cliente,
            BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("cliente", cliente);
            return "./clienti/clienti-edit";
        } else if ((clienteService.findClienteByEmail(cliente.getEmail()) != null
                && clienteService.findClienteByEmail(cliente.getEmail()).getId().longValue() != cliente.getId()
                        .longValue())
                || (clienteService.findClienteByTelefono(cliente.getTelefono()) != null
                        && clienteService.findClienteByTelefono(cliente.getTelefono()).getId() != cliente.getId()
                                .longValue())) {
            model.addAttribute("errorMessage",
                    "Hai provato ad inserire un cliente con una email o numero di telefono già esistente");
            return "./errors/input-error";
        } else {
            clienteService.saveCliente(cliente);
            return "redirect:/clienti";
        }
    }

    @GetMapping("/clienti/{clienteId}")
    public String viewDetailCliente(@PathVariable("clienteId") Long clienteId, Model model) {
        try {
            Cliente cliente = clienteService.findClienteById(clienteId);
            model.addAttribute("cliente", cliente);
            return "./clienti/clienti-detail";
        } catch (Exception e) {
            return "redirect:/errore";
        }
    }

    @DeleteMapping("/clienti/{clienteId}")
    public String deleteCliente(@PathVariable("clienteId") Long clienteId) {
        clienteService.delete(clienteId);
        return "redirect:/clienti";
    }
}
