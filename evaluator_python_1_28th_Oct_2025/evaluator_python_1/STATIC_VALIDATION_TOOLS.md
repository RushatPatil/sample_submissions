# Static Validation Tools Guide

This document explains the static validation tools available for different programming languages, their equivalents, and installation instructions.

---

## Overview

Static validation consists of three main categories:
1. **Compilation/Syntax Check** - Ensures code compiles and has no syntax errors
2. **Code Quality & Style** - Enforces coding standards and detects code smells
3. **Security Analysis** - Identifies security vulnerabilities

---

## Python

### Tools Used
| Category | Tool | Purpose |
|----------|------|---------|
| Compilation | `py_compile` | Syntax and import error detection |
| Code Quality | `pylint` | PEP 8 style, code smells, potential bugs |
| Security | `bandit` | Security vulnerability scanning |

### Installation
```bash
pip install pylint>=3.0.0
pip install bandit>=1.7.0
```

### Usage in Code
```python
# Pylint
cmd = ["python", "-m", "pylint", str(file_path), "--output-format=json"]

# Bandit
cmd = ["python", "-m", "bandit", "-f", "json", str(file_path)]
```

### Output Example
- **pylint**: JSON with error_count, warning_count, convention_count, refactor_count
- **bandit**: JSON with high/medium/low severity issues

---

## Java

### Tools Used
| Category | Tool | Purpose |
|----------|------|---------|
| Compilation | `javac` | Compilation and syntax errors |
| Code Quality | `checkstyle` | Java coding standards (Google/Sun style) |
| Code Quality | `PMD` | Bug patterns, unused code, performance |
| Bug Detection | `SpotBugs` | Bytecode analysis for bugs |
| Security | `SpotBugs + Find Security Bugs` | Security-focused static analysis |

### Installation

#### javac (Built into JDK)
```bash
# Verify installation
javac -version
```

#### Checkstyle
```bash
# Download checkstyle JAR
wget https://github.com/checkstyle/checkstyle/releases/download/checkstyle-10.12.0/checkstyle-10.12.0-all.jar

# Or install via package manager
# Ubuntu/Debian
sudo apt install checkstyle

# macOS
brew install checkstyle

# Windows (with Chocolatey)
choco install checkstyle
```

#### PMD
```bash
# Download PMD
wget https://github.com/pmd/pmd/releases/download/pmd_releases/7.0.0/pmd-bin-7.0.0.zip
unzip pmd-bin-7.0.0.zip

# Or install via package manager
brew install pmd  # macOS
```

#### SpotBugs + Find Security Bugs
```bash
# Download SpotBugs
wget https://github.com/spotbugs/spotbugs/releases/download/4.7.3/spotbugs-4.7.3.zip
unzip spotbugs-4.7.3.zip

# Download Find Security Bugs plugin
wget https://github.com/find-sec-bugs/find-sec-bugs/releases/download/version-1.12.0/findsecbugs-plugin-1.12.0.jar
```

### Usage in Code
```bash
# javac
javac -Xlint:all -encoding UTF-8 MyFile.java

# Checkstyle
checkstyle -f json MyFile.java

# Or with JAR
java -jar checkstyle.jar -c /google_checks.xml -f json MyFile.java

# PMD
pmd check -d src/ -R rulesets/java/quickstart.xml -f json

# SpotBugs (requires compiled .class files)
spotbugs -textui -output report.xml MyProject.jar
```

### Configuration Files
- **Checkstyle**: `checkstyle.xml` (Google Style Guide, Sun Checks)
- **PMD**: Built-in rulesets or custom `pmd.xml`
- **SpotBugs**: `spotbugs.xml` for exclusions

---

## JavaScript/TypeScript

### Tools Used
| Category | Tool | Purpose |
|----------|------|---------|
| Syntax Check | `node --check` | JavaScript syntax validation |
| Compilation | `tsc` | TypeScript type checking |
| Code Quality | `ESLint` | Linting and code quality |
| Code Quality | `JSHint` | Alternative linter |
| Security | `npm audit` | Dependency vulnerability scanning |
| Security | `Snyk` | Comprehensive security scanning |

### Installation
```bash
# ESLint
npm install -g eslint

# Initialize ESLint config
eslint --init

# ESLint security plugins
npm install --save-dev eslint-plugin-security
npm install --save-dev eslint-plugin-no-unsanitized

# TypeScript
npm install -g typescript

# Snyk
npm install -g snyk
snyk auth
```

### Usage in Code
```bash
# Syntax check
node --check script.js

# TypeScript
tsc --noEmit file.ts

# ESLint
eslint file.js --format json

# npm audit
npm audit --json

# Snyk
snyk test --json
```

### ESLint Configuration Example
```json
{
  "extends": ["eslint:recommended", "plugin:security/recommended"],
  "plugins": ["security", "no-unsanitized"],
  "rules": {
    "security/detect-object-injection": "warn",
    "no-unsanitized/method": "error"
  }
}
```

---

## C#

### Tools Used
| Category | Tool | Purpose |
|----------|------|---------|
| Compilation | `csc` / `dotnet build` | Compilation errors |
| Code Quality | Roslyn Analyzers | Built-in .NET analyzers |
| Code Quality | StyleCop | C# style guidelines |
| Code Quality | FxCop | .NET code analysis |
| Security | Security Code Scan | Security vulnerability detection |

### Installation
```bash
# .NET SDK (includes csc and Roslyn)
# Download from https://dotnet.microsoft.com/download

# Security Code Scan (NuGet package)
dotnet add package SecurityCodeScan.VS2019
```

### Usage in Code
```bash
# Compilation
csc /target:library MyFile.cs

# Or with dotnet
dotnet build

# With analyzers enabled
dotnet build /p:RunAnalyzers=true /p:TreatWarningsAsErrors=true

# SonarQube (for comprehensive analysis)
dotnet sonarscanner begin /k:"project-key"
dotnet build
dotnet sonarscanner end
```

### Configuration
- **Roslyn Analyzers**: `.editorconfig` file
- **StyleCop**: `stylecop.json`
- **Security Code Scan**: Automatically runs with build

---

## Comparison Matrix

| Feature | Python | Java | JavaScript | C# |
|---------|--------|------|------------|-----|
| **Compilation Check** | py_compile | javac | node --check / tsc | csc / dotnet build |
| **Style/Quality** | pylint | checkstyle, PMD | ESLint | Roslyn, StyleCop |
| **Bug Detection** | pylint | SpotBugs | ESLint | FxCop, Roslyn |
| **Security** | bandit | Find Security Bugs | npm audit, Snyk | Security Code Scan |
| **JSON Output** | ✅ | ✅ | ✅ | ✅ |
| **Module Invocation** | python -m | java -jar / CLI | npx | dotnet |

---

## Implementation in Generic Evaluator

### Current Status
- ✅ **Python**: Fully implemented (`python_validator.py`)
- ✅ **Java**: Implemented (`java_validator.py`) - javac & checkstyle
- ⏳ **JavaScript**: Not yet implemented
- ⏳ **C#**: Not yet implemented

### Architecture
```
src/validators/
├── __init__.py
├── python_validator.py   ✅ Complete
├── java_validator.py     ✅ Complete
├── javascript_validator.py  (TODO)
└── csharp_validator.py      (TODO)
```

### Usage in generic_evaluator.py
```python
if language_lower == "python":
    return self.python_validator.validate_project(project_path)
elif language_lower == "java":
    return self.java_validator.validate_project(project_path)
elif language_lower == "javascript":
    return self.javascript_validator.validate_project(project_path)
elif language_lower == "csharp":
    return self.csharp_validator.validate_project(project_path)
```

---

## Tool Installation Quick Reference

### Python
```bash
pip install pylint bandit
```

### Java
```bash
# Ubuntu/Debian
sudo apt install default-jdk checkstyle

# macOS
brew install openjdk checkstyle

# Windows (Chocolatey)
choco install openjdk checkstyle
```

### JavaScript
```bash
npm install -g eslint snyk
```

### C#
```bash
# Download .NET SDK from https://dotnet.microsoft.com/download
# Security Code Scan via NuGet
dotnet add package SecurityCodeScan.VS2019
```

---

## Alternative Tools

### Multi-Language Tools
1. **SonarQube** - Supports multiple languages (Python, Java, JS, C#)
   - Self-hosted or cloud
   - Comprehensive quality and security analysis
   - Command: `sonar-scanner`

2. **Semgrep** - Static analysis for multiple languages
   - Fast and customizable
   - Command: `semgrep --config auto --json`

3. **CodeQL** - GitHub's code analysis engine
   - Deep semantic analysis
   - Command: `codeql database analyze`

### Cloud-Based Options
- **Snyk** - Dependency and code security
- **Veracode** - Enterprise security scanning
- **Checkmarx** - SAST and DAST
- **WhiteSource/Mend** - Open source security

---

## Best Practices

### 1. Incremental Analysis
- Run fast checks first (compilation)
- Run style checks next
- Run security analysis last (often slowest)

### 2. Timeout Management
- Set reasonable timeouts (30-60 seconds per file)
- Handle timeouts gracefully

### 3. Result Aggregation
- Provide file-level and project-level summaries
- Count issues by severity

### 4. Error Handling
- Gracefully handle missing tools (return "not_installed" status)
- Continue validation even if one tool fails

### 5. Performance
- Consider caching results
- Run tools in parallel where possible
- Limit scope to changed files in incremental builds

---

## Troubleshooting

### Tool Not Found
**Problem**: `FileNotFoundError` when running tool
**Solution**:
- Check tool is installed: `which <tool>` or `where <tool>`
- Use module invocation: `python -m pylint` instead of `pylint`
- Add tool to PATH
- Use full path to tool

### JSON Parsing Errors
**Problem**: Cannot parse tool output
**Solution**:
- Verify tool supports JSON output (`--format json` or `-f json`)
- Check for stderr output mixed with stdout
- Validate JSON before parsing

### Timeout Issues
**Problem**: Tool takes too long
**Solution**:
- Increase timeout limit
- Exclude large files or generated code
- Use faster alternatives or limit rules

### Permission Errors
**Problem**: Cannot execute tool
**Solution**:
- Check file permissions
- Run as appropriate user
- Use `chmod +x` on Unix systems

---

## Future Enhancements

### Short Term
1. Implement JavaScript validator (ESLint + npm audit)
2. Implement C# validator (Roslyn + Security Code Scan)
3. Add caching for repeated validations

### Long Term
1. Integrate SonarQube for unified analysis
2. Add support for more languages (Go, Rust, Ruby)
3. Implement incremental analysis
4. Add custom rule configurations
5. Generate HTML reports

---

## Resources

### Documentation
- **Python**: [pylint](https://pylint.pycqa.org/), [bandit](https://bandit.readthedocs.io/)
- **Java**: [checkstyle](https://checkstyle.org/), [SpotBugs](https://spotbugs.github.io/), [PMD](https://pmd.github.io/)
- **JavaScript**: [ESLint](https://eslint.org/), [Snyk](https://snyk.io/)
- **C#**: [Roslyn Analyzers](https://docs.microsoft.com/en-us/visualstudio/code-quality/roslyn-analyzers-overview), [Security Code Scan](https://security-code-scan.github.io/)

### Tool Comparison Sites
- [OWASP Source Code Analysis Tools](https://owasp.org/www-community/Source_Code_Analysis_Tools)
- [Analysis Tools](https://analysis-tools.dev/)

---

**Last Updated**: 2025-10-17
**Version**: 1.0.0
