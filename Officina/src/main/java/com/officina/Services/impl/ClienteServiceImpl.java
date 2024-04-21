package com.officina.Services.impl;

import java.util.List;

import org.springframework.stereotype.Service;

import com.officina.Models.Cliente;
import com.officina.Repository.ClienteRepository;
import com.officina.Services.ClienteService;

@Service
public class ClienteServiceImpl implements ClienteService {

    ClienteRepository clienteRepository;

    public ClienteServiceImpl(ClienteRepository clienteRepository) {
        this.clienteRepository = clienteRepository;
    }

    @Override
    public List<Cliente> findAllClientes() {
        return clienteRepository.findAll();
    }

    @Override
    public List<Cliente> findClienteByNomeAndCognome(String nome, String cognome) {
        return clienteRepository.findByNomeAndCognome(nome, cognome);
    }

    @Override
    public List<Cliente> findClienteByNome(String nome) {
        return clienteRepository.findByNome(nome);
    }

    @Override
    public List<Cliente> findClienteByCognome(String cognome) {
        return clienteRepository.findByCognome(cognome);
    }

    @Override
    public Cliente saveCliente(Cliente cliente) {
        return clienteRepository.save(cliente);
    }

    @Override
    public Cliente findClienteByTelefono(String telefono) {
        return clienteRepository.findByTelefono(telefono);
    }

    @Override
    public Cliente findClienteByEmail(String email) {
        return clienteRepository.findByEmail(email);
    }

    @Override
    public void updateAuto(Cliente cliente) {
        clienteRepository.save(cliente);
    }

    @Override
    public Cliente findClienteById(Long clienteId) {
        return clienteRepository.findById(clienteId).get();
    }

    @Override
    public void delete(Long clienteId) {
        clienteRepository.deleteById(clienteId);
    }

}
