package com.example.evaluator;

public class FunctionalCorrectness {
    private int totalPairs;
    private int groundedReplies;
    private int totalCitations;
    private int correctCitations;
    private int missingCitations;
    private int hallucinatedReplies;

    public int getTotalPairs() { return totalPairs; }
    public void setTotalPairs(int totalPairs) { this.totalPairs = totalPairs; }
    public int getGroundedReplies() { return groundedReplies; }
    public void setGroundedReplies(int groundedReplies) { this.groundedReplies = groundedReplies; }
    public int getTotalCitations() { return totalCitations; }
    public void setTotalCitations(int totalCitations) { this.totalCitations = totalCitations; }
    public int getCorrectCitations() { return correctCitations; }
    public void setCorrectCitations(int correctCitations) { this.correctCitations = correctCitations; }
    public int getMissingCitations() { return missingCitations; }
    public void setMissingCitations(int missingCitations) { this.missingCitations = missingCitations; }
    public int getHallucinatedReplies() { return hallucinatedReplies; }
    public void setHallucinatedReplies(int hallucinatedReplies) { this.hallucinatedReplies = hallucinatedReplies; }
}
