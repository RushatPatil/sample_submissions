package com.example.evaluator;

public class ScoreResult {
    private double staticScore;
    private double functionalScore;
    private double usecaseScore;
    private double finalScore;
    private String summary;

    public double getStaticScore() { return staticScore; }
    public void setStaticScore(double staticScore) { this.staticScore = staticScore; }
    public double getFunctionalScore() { return functionalScore; }
    public void setFunctionalScore(double functionalScore) { this.functionalScore = functionalScore; }
    public double getUsecaseScore() { return usecaseScore; }
    public void setUsecaseScore(double usecaseScore) { this.usecaseScore = usecaseScore; }
    public double getFinalScore() { return finalScore; }
    public void setFinalScore(double finalScore) { this.finalScore = finalScore; }
    public String getSummary() { return summary; }
    public void setSummary(String summary) { this.summary = summary; }
}
