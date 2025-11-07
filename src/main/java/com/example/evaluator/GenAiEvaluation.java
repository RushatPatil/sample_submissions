package com.example.evaluator;

import java.util.Map;

public class GenAiEvaluation {
    private Map<String, String> criteriaQuality;

    public Map<String, String> getCriteriaQuality() { return criteriaQuality; }
    public void setCriteriaQuality(Map<String, String> criteriaQuality) { this.criteriaQuality = criteriaQuality; }

    public double averageQualityScore() {
        if (criteriaQuality == null || criteriaQuality.isEmpty()) return 0.0;
        double sum = 0.0;
        for (String q : criteriaQuality.values()) {
            sum += mapQuality(q);
        }
        return sum / criteriaQuality.size();
    }

    public static double mapQuality(String q) {
        if (q == null) return 0.5;
        switch (q.toLowerCase()) {
            case "excellent": return 1.0;
            case "good": return 0.8;
            case "average": return 0.6;
            case "bad": return 0.4;
            default: return 0.5;
        }
    }
}
