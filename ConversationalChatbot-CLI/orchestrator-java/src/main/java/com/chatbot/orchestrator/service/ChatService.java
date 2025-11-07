package com.chatbot.orchestrator.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.TimeUnit;

@Service
public class ChatService {

    @Value("${python.cli.path:../backend-python-cli/chatbot_cli.py}")
    private String pythonCliPath;

    @Value("${python.executable:python}")
    private String pythonExecutable;

    private static final String LOG_DIR = "logs";
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private final ObjectMapper objectMapper = new ObjectMapper();

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

            // Build command to execute Python CLI
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                pythonCliPath,
                "-m",
                userMessage
            );

            // Set working directory to the Python CLI directory
            String cliDirectory = Paths.get(pythonCliPath).getParent().toString();
            processBuilder.directory(new java.io.File(cliDirectory));

            System.out.println("[" + LocalDateTime.now().format(formatter) +
                "] Executing Python CLI: " + pythonExecutable + " " + pythonCliPath);

            // Start the process
            Process process = processBuilder.start();

            // Read stdout (JSON response)
            BufferedReader stdoutReader = new BufferedReader(
                new InputStreamReader(process.getInputStream())
            );

            // Read stderr (logs) in a separate thread
            BufferedReader stderrReader = new BufferedReader(
                new InputStreamReader(process.getErrorStream())
            );

            // Start thread to read stderr
            Thread stderrThread = new Thread(() -> {
                try {
                    String line;
                    while ((line = stderrReader.readLine()) != null) {
                        System.err.println("[Python CLI] " + line);
                    }
                } catch (IOException e) {
                    System.err.println("Error reading stderr: " + e.getMessage());
                }
            });
            stderrThread.start();

            // Read JSON response from stdout
            StringBuilder jsonOutput = new StringBuilder();
            String line;
            while ((line = stdoutReader.readLine()) != null) {
                jsonOutput.append(line);
            }

            // Wait for process to complete (with timeout)
            boolean finished = process.waitFor(10, TimeUnit.SECONDS);
            if (!finished) {
                process.destroyForcibly();
                throw new RuntimeException("Python CLI process timed out");
            }

            // Check exit code
            int exitCode = process.exitValue();
            if (exitCode != 0) {
                throw new RuntimeException("Python CLI exited with code: " + exitCode);
            }

            // Parse JSON response
            String jsonResponseStr = jsonOutput.toString().trim();
            if (jsonResponseStr.isEmpty()) {
                throw new RuntimeException("Python CLI returned empty response");
            }

            JsonNode jsonResponse = objectMapper.readTree(jsonResponseStr);

            // Check for error in response
            if (jsonResponse.has("error")) {
                String errorMsg = jsonResponse.get("error").asText();
                logTransaction("ERROR", errorMsg);
                throw new RuntimeException("Python CLI error: " + errorMsg);
            }

            // Extract assistant response
            String assistantResponse = jsonResponse.has("assistant_response")
                ? jsonResponse.get("assistant_response").asText()
                : "No response from CLI";

            // Log outgoing response
            logTransaction("OUTGOING", assistantResponse);

            System.out.println("[" + LocalDateTime.now().format(formatter) +
                "] Received from Python CLI: " + assistantResponse);

            return assistantResponse;

        } catch (Exception e) {
            String errorMsg = "Error communicating with Python CLI: " + e.getMessage();
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
