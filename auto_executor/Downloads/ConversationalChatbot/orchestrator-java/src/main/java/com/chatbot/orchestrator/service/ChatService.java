package com.chatbot.orchestrator.service;

import com.chatbot.orchestrator.model.PythonRequest;
import com.chatbot.orchestrator.model.PythonResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Service
public class ChatService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${python.backend.url:http://localhost:5000}")
    private String pythonBackendUrl;

    private static final String LOG_DIR = "logs";
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public ChatService() {
        // Ensure logs directory exists
        try {
            Files.createDirectories(Paths.get(LOG_DIR));
        } catch (IOException e) {
            System.err.println("Failed to create logs directory: " + e.getMessage());
        }
    }

    public String processMessage(String userMessage) {
        try {
            // Log incoming request
            logTransaction("INCOMING", userMessage);

            // Prepare request to Python backend
            PythonRequest pythonRequest = new PythonRequest(userMessage);

            // Set headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<PythonRequest> entity = new HttpEntity<>(pythonRequest, headers);

            // Call Python backend
            String pythonUrl = pythonBackendUrl + "/chat";
            System.out.println("[" + LocalDateTime.now().format(formatter) + "] Forwarding to Python backend: " + pythonUrl);

            ResponseEntity<PythonResponse> response = restTemplate.postForEntity(
                pythonUrl,
                entity,
                PythonResponse.class
            );

            // Extract response
            String assistantResponse = response.getBody() != null
                ? response.getBody().getAssistantResponse()
                : "No response from backend";

            // Log outgoing response
            logTransaction("OUTGOING", assistantResponse);

            System.out.println("[" + LocalDateTime.now().format(formatter) + "] Received from Python: " + assistantResponse);

            return assistantResponse;

        } catch (Exception e) {
            String errorMsg = "Error communicating with Python backend: " + e.getMessage();
            System.err.println("[" + LocalDateTime.now().format(formatter) + "] " + errorMsg);
            logTransaction("ERROR", errorMsg);
            throw new RuntimeException(errorMsg, e);
        }
    }

    private void logTransaction(String type, String message) {
        try {
            String timestamp = LocalDateTime.now().format(formatter);
            String logFile = LOG_DIR + "/orchestrator.log";

            try (PrintWriter writer = new PrintWriter(new FileWriter(logFile, true))) {
                writer.println(String.format("[%s] %s: %s", timestamp, type, message));
            }
        } catch (IOException e) {
            System.err.println("Failed to write to log file: " + e.getMessage());
        }
    }
}
