"""Test script to directly test the evaluation orchestrator"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from evaluators.evaluation_orchestrator import EvaluationOrchestrator
from loguru import logger

def test_evaluation():
    """Test the evaluation with the provided parameters"""

    # Test parameters
    team_name = "Team A"
    language = "python"
    problem_statement = "Problem statement : TO Solve the conversion use-case for conversion"
    zip_file_path = r"C:\Users\rushatp\Downloads\graph_conversion 2.zip"

    # Check if file exists
    if not Path(zip_file_path).exists():
        logger.error(f"Zip file not found at: {zip_file_path}")
        return

    logger.info("="*80)
    logger.info("STARTING TEST EVALUATION")
    logger.info("="*80)
    logger.info(f"Team Name: {team_name}")
    logger.info(f"Language: {language}")
    logger.info(f"Problem Statement: {problem_statement}")
    logger.info(f"Zip File: {zip_file_path}")
    logger.info("="*80)

    try:
        # Initialize orchestrator
        logger.info("Initializing EvaluationOrchestrator...")
        orchestrator = EvaluationOrchestrator()

        logger.info(f"Loaded {len(orchestrator.criteria_prompts)} criteria")
        for criteria_name in orchestrator.criteria_prompts.keys():
            logger.info(f"  - {criteria_name}")

        # Run evaluation
        logger.info("\nStarting evaluation...")
        result = orchestrator.evaluate_submission(
            team_name=team_name,
            zip_file_path=zip_file_path,
            language=language,
            problem_statement=problem_statement
        )

        # Print results
        logger.info("\n" + "="*80)
        logger.info("EVALUATION COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"Team: {result.get('team_name')}")
        logger.info(f"Language: {result.get('language')}")
        logger.info(f"Status: {result.get('status')}")
        logger.info(f"Criteria Count: {result.get('criteria_count')}")
        logger.info(f"Average Score: {result.get('average_score')}")

        logger.info("\n" + "-"*80)
        logger.info("CRITERIA RESULTS:")
        logger.info("-"*80)
        for criteria_name, criteria_result in result.get('criteria_results', {}).items():
            logger.info(f"\n{criteria_name}:")
            logger.info(f"  Status: {criteria_result.get('status')}")
            logger.info(f"  Human Approval: {criteria_result.get('human_approval')}")
            if 'error' in criteria_result:
                logger.error(f"  Error: {criteria_result.get('error')}")

        logger.info("\n" + "-"*80)
        logger.info("CLUBBED RESPONSE:")
        logger.info("-"*80)
        print(result.get('clubbed_response', 'No clubbed response available'))

        logger.info("\n" + "="*80)
        logger.info("TEST COMPLETED")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"\n{'='*80}")
        logger.error(f"ERROR DURING EVALUATION")
        logger.error(f"{'='*80}")
        logger.exception(e)
        raise

if __name__ == "__main__":
    test_evaluation()
