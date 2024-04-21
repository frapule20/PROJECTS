package com.officina.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.officina.Models.Cliente;

@Repository
public interface ClienteRepository extends JpaRepository<Cliente, Long> {
    public Cliente findById(long id);

    public List<Cliente> findByNomeAndCognome(String nome, String cognome);

    public List<Cliente> findByNome(String nome);

    public List<Cliente> findByCognome(String cognome);

    public Cliente findByEmail(String email);

    public Cliente findByTelefono(String telefono);

}