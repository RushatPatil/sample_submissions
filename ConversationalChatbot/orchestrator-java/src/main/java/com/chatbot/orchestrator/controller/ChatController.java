package com.chatbot.orchestrator.controller;

import com.chatbot.orchestrator.model.MessageRequest;
import com.chatbot.orchestrator.model.MessageResponse;
import com.chatbot.orchestrator.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")  // Allow requests from React frontend
public class ChatController {

    @Autowired
    private ChatService chatService;

    @PostMapping("/message")
    public ResponseEntity<MessageResponse> sendMessage(@RequestBody MessageRequest request) {
        try {
            if (request.getMessage() == null || request.getMessage().trim().isEmpty()) {
                return ResponseEntity.badRequest()
                    .body(new MessageResponse("Message cannot be empty"));
            }

            // Process message through service layer
            String response = chatService.processMessage(request.getMessage());

            return ResponseEntity.ok(new MessageResponse(response));

        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                .body(new MessageResponse("Error processing message: " + e.getMessage()));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> healthInfo = new HashMap<>();
        healthInfo.put("status", "healthy");
        healthInfo.put("service", "Java Orchestrator");
        healthInfo.put("port", 8080);
        return ResponseEntity.ok(healthInfo);
    }
}
