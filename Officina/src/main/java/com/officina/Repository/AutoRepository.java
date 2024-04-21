package com.officina.Repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.officina.Models.Auto;
import java.util.Optional;

@Repository
public interface AutoRepository extends JpaRepository<Auto, Long> {
    Optional<Auto> findByTarga(String targa);
}
