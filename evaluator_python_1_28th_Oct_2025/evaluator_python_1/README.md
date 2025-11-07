# GenAI-Based Evaluator

A Python-based evaluation system using Azure OpenAI APIs (GPT-4.1 Assistant API and GPT-5 Response API) to evaluate GenAI projects written in multiple programming languages.

## Supported Languages

- Java
- JavaScript/TypeScript
- Python
- C#

## Features

- Evaluation using Azure OpenAI GPT-4.1 (Assistant API)
- Advanced analysis using GPT-5 (Response API)
- Multi-language support for code evaluation
- Configurable evaluation criteria
- Detailed scoring and feedback system
- Asynchronous processing for better performance

## Project Structure

```
evaluator_python/
├── config/
│   └── config.yaml          # Main configuration file
├── logs/                     # Application logs
├── results/                  # Evaluation results
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── azure_client.py  # Azure OpenAI API clients
│   ├── evaluators/
│   │   ├── __init__.py
│   │   └── base_evaluator.py  # Base evaluator class
│   ├── models/              # Data models (future)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py        # Logging configuration
│   └── main.py              # Main entry point
├── tests/                   # Unit tests
├── venv/                    # Virtual environment
├── .env.example             # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.9 or higher
- Azure OpenAI API access with GPT-4.1 and GPT-5 deployments

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd evaluator_python
   ```

2. Create and activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your Azure OpenAI credentials
   ```

5. Update configuration in `config/config.yaml` as needed.

## Usage

### Basic Usage

```bash
python src/main.py <project_path> <language> [options]
```

### Examples

Evaluate a Java project:
```bash
python src/main.py /path/to/java/project java
```

Evaluate a Python project with output:
```bash
python src/main.py /path/to/python/project python -o results/evaluation.json
```

### Command-line Arguments

- `project_path`: Path to the project directory to evaluate (required)
- `language`: Programming language (choices: java, javascript, python, csharp) (required)
- `-o, --output`: Output path for evaluation results in JSON format (optional)

## Configuration

### Environment Variables (.env)

```env
# Azure OpenAI Configuration for GPT-4.1 (Assistant API)
AZURE_OPENAI_ASSISTANT_ENDPOINT=your_assistant_endpoint_here
AZURE_OPENAI_ASSISTANT_KEY=your_assistant_key_here
AZURE_OPENAI_ASSISTANT_DEPLOYMENT=gpt-4-1

# Azure OpenAI Configuration for GPT-5 (Response API)
AZURE_OPENAI_RESPONSE_ENDPOINT=your_response_endpoint_here
AZURE_OPENAI_RESPONSE_KEY=your_response_key_here
AZURE_OPENAI_RESPONSE_DEPLOYMENT=gpt-5
```

### Evaluation Criteria

The system evaluates projects based on:

- **Code Quality** (25%): Clean code, readability, maintainability
- **Design Patterns** (20%): Appropriate use of design patterns
- **Error Handling** (20%): Exception handling and edge cases
- **Performance** (20%): Efficiency and optimization
- **Security** (15%): Security best practices

Weights can be adjusted in `config/config.yaml`.

## Development

### Running Tests

```bash
pytest tests/
```

### Adding a New Language Evaluator

1. Create a new evaluator class in `src/evaluators/`
2. Extend `BaseEvaluator` class
3. Implement required methods: `extract_code()`, `analyze_structure()`, `evaluate()`
4. Add language configuration in `config/config.yaml`

## Architecture

### API Clients

- **AzureAssistantClient**: Handles GPT-4.1 Assistant API interactions
- **AzureResponseClient**: Handles GPT-5 Response API interactions

### Evaluators

Base evaluator class provides common functionality for language-specific evaluators.

### Utilities

- Logger configuration using `loguru`
- Configuration management using YAML

## Roadmap

- [ ] Implement language-specific evaluators (Java, JavaScript, Python, C#)
- [ ] Add code parsing and static analysis
- [ ] Implement parallel evaluation processing
- [ ] Add detailed report generation (HTML/PDF)
- [ ] Create web interface for evaluations
- [ ] Add support for more languages
- [ ] Implement evaluation caching
- [ ] Add CI/CD integration

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

[Your Contact Information]
