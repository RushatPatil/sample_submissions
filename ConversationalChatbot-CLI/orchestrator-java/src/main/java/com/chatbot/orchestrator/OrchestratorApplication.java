package com.chatbot.orchestrator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrchestratorApplication {

    public static void main(String[] args) {
        System.out.println("=".repeat(50));
        System.out.println("Java Orchestrator Service Starting...");
        System.out.println("Port: 8080");
        System.out.println("Backend: Python CLI");
        System.out.println("=".repeat(50));
        SpringApplication.run(OrchestratorApplication.class, args);
    }
}
