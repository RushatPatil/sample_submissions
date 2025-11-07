package com.chatbot.orchestrator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class OrchestratorApplication {

    public static void main(String[] args) {
        System.out.println("=".repeat(50));
        System.out.println("Java Orchestrator Service Starting...");
        System.out.println("Port: 8080");
        System.out.println("=".repeat(50));
        SpringApplication.run(OrchestratorApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
