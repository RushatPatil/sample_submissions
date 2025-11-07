package com.example.evaluator;

public class LinterValidation {
    private int totalFiles;
    private int filesWithErrors;
    private int totalPylintWarnings;

    public int getTotalFiles() { return totalFiles; }
    public void setTotalFiles(int totalFiles) { this.totalFiles = totalFiles; }
    public int getFilesWithErrors() { return filesWithErrors; }
    public void setFilesWithErrors(int filesWithErrors) { this.filesWithErrors = filesWithErrors; }
    public int getTotalPylintWarnings() { return totalPylintWarnings; }
    public void setTotalPylintWarnings(int totalPylintWarnings) { this.totalPylintWarnings = totalPylintWarnings; }
}
