package com.officina.Services;

import java.util.List;

import com.officina.Models.Cliente;

public interface ClienteService {

    List<Cliente> findAllClientes();

    List<Cliente> findClienteByNomeAndCognome(String nome, String cognome);

    List<Cliente> findClienteByNome(String nome);

    List<Cliente> findClienteByCognome(String cognome);

    Cliente findClienteById(Long clienteId);

    Cliente findClienteByTelefono(String cliente);

    Cliente findClienteByEmail(String email);

    Cliente saveCliente(Cliente cliente);

    void updateAuto(Cliente cliente);

    void delete(Long clienteId);
}
