# Human-in-the-Loop Evaluation

## Overview

The evaluation system includes a human-in-the-loop feature that allows manual review and feedback for each evaluation criteria. This ensures that the AI assistant fully meets the evaluation goals before moving to the next criteria.

## How It Works

### 1. Automatic Evaluation
The system runs the AI assistant to evaluate code based on the defined criteria.

### 2. CLI Prompt Display
Once the assistant completes its evaluation, a CLI prompt appears showing:

```
================================================================================
EVALUATION COMPLETED: TECHNICAL
================================================================================

ASSISTANT RESPONSE:
--------------------------------------------------------------------------------
{Full response from the assistant with proper formatting}
--------------------------------------------------------------------------------

HUMAN EVALUATION:
  - Type 'APPROVE' or 'OK' to accept this evaluation and move to next criteria
  - Type any feedback/comments to continue the conversation with the assistant
================================================================================

Your response: _
```

### 3. Two Options

#### Option A: Approve and Continue
If you're satisfied with the evaluation:
- Type: `APPROVE`, `OK`, `YES`, or `Y`
- System moves to the next criteria
- Current response is saved as the final evaluation

#### Option B: Provide Feedback
If the evaluation is incomplete or needs improvement:
- Type your feedback/comments
- Examples:
  - "Please provide more specific line numbers for the code issues"
  - "Can you elaborate on the design patterns section?"
  - "The security analysis seems incomplete, please check for SQL injection risks"
- Your feedback is added as a user message to the thread
- Assistant runs again with your feedback
- New response is displayed for your review
- Process repeats until you approve

### 4. Recursive Feedback Loop
The system supports multiple rounds of feedback:
```
Initial Response → Human Feedback → Revised Response → More Feedback → Final Response → Approve
```

## Example Interaction

### First Response
```
================================================================================
EVALUATION COMPLETED: TECHNICAL
================================================================================

ASSISTANT RESPONSE:
--------------------------------------------------------------------------------
{
    "criteria": "Technical Implementation",
    "total_score": 75,
    "breakdown": {
        "code_structure": {
            "score": 18,
            "feedback": "Code is well organized..."
        },
        ...
    }
}
--------------------------------------------------------------------------------

Your response: The error handling section needs more detail. Can you check each function for try-catch blocks?
```

### After Feedback
```
Adding your feedback to the conversation and re-running evaluation...
Please wait...

================================================================================
EVALUATION COMPLETED: TECHNICAL
================================================================================

ASSISTANT RESPONSE:
--------------------------------------------------------------------------------
{
    "criteria": "Technical Implementation",
    "total_score": 72,
    "breakdown": {
        "code_structure": {
            "score": 18,
            "feedback": "Code is well organized..."
        },
        "error_handling": {
            "score": 12,
            "feedback": "Checked all functions. Found try-catch in main.py:42, utils.py:15..."
        },
        ...
    }
}
--------------------------------------------------------------------------------

Your response: APPROVE
```

## Benefits

### 1. Quality Assurance
- Ensures evaluations are thorough and accurate
- Catches cases where AI might miss important details
- Allows domain experts to guide the evaluation

### 2. Iterative Refinement
- Assistant can dig deeper based on human feedback
- Enables clarification of ambiguous points
- Improves evaluation quality through collaboration

### 3. Context Preservation
- All feedback is added to the same thread
- Assistant maintains context across iterations
- File attachments remain accessible throughout

### 4. Flexibility
- Skip review for simple cases (just type APPROVE)
- Deep dive on complex evaluations with multiple feedback rounds
- Control the evaluation depth per criteria

## Technical Implementation

### Location
`src/evaluators/evaluation_orchestrator.py` - `_human_evaluation_prompt()` method (lines 279-350)

### Flow

1. **Display Response**
   - Formats and prints the assistant's response
   - Shows clear instructions for user input

2. **Accept User Input**
   - Checks for approval keywords (case-insensitive)
   - If not approved, treats input as feedback

3. **Process Feedback**
   - Adds feedback as user message to thread
   - Creates new run with same assistant
   - Polls until completion

4. **Recursive Review**
   - Calls itself with the new response
   - Continues until user approves

5. **Error Handling**
   - If re-evaluation fails, uses previous response
   - Logs all actions for debugging

### Integration Point
Line 234-254: After `run_result["status"] == "completed"`

```python
if run_result["status"] == "completed":
    # Human evaluation prompt
    is_approved, final_response = self._human_evaluation_prompt(
        criteria_name=criteria_name,
        response_text=run_result["response"],
        thread_id=thread_id,
        assistant_id=assistant
    )

    # Parse the final approved response
    evaluation_result = self._parse_evaluation_response(final_response)
```

## Approval Keywords

The following keywords (case-insensitive) approve the evaluation:
- `APPROVE`
- `OK`
- `YES`
- `Y`

Any other input is treated as feedback for the assistant.

## Use Cases

### Use Case 1: Quick Approval
```
Your response: ok
```
Fast-track through evaluations that look good on first pass.

### Use Case 2: Request More Detail
```
Your response: Can you provide specific file:line references for each issue found?
```
Ask for more detailed analysis.

### Use Case 3: Point Out Missing Items
```
Your response: I don't see any analysis of the database connection handling. Please check that.
```
Guide the assistant to areas it might have missed.

### Use Case 4: Ask for Clarification
```
Your response: What do you mean by "suboptimal design pattern"? Can you explain which pattern should be used instead?
```
Get clearer explanations.

### Use Case 5: Request Code Examples
```
Your response: For the recommendations section, can you provide code examples showing the improvements?
```
Make recommendations more actionable.

## Best Practices

1. **Be Specific**: Give clear, actionable feedback
   - ❌ "This is incomplete"
   - ✅ "Please analyze the authentication module in auth.py"

2. **One Round at a Time**: Focus on one aspect per feedback round
   - Better to iterate multiple times than overwhelm with feedback

3. **Use Context**: Reference specific parts of the response
   - "In the code_quality section, you mentioned..."

4. **Quick Approve**: If it's good enough, approve quickly
   - Don't over-perfect every evaluation

5. **Trust But Verify**: The assistant has already analyzed the code
   - Use feedback to redirect, not micromanage

## Logging

All human interactions are logged:
```
INFO: Run completed, prompting human for evaluation...
INFO: Human approved evaluation for criteria: technical
INFO: Human provided feedback for criteria: prompt_engineering
INFO: Re-evaluation completed for criteria: prompt_engineering
```

## Future Enhancements

Potential improvements:
- Save human feedback for training/analysis
- Show diff between responses after feedback
- Add "SKIP" option to skip criteria
- Timeout for long waits
- Support for automated approval mode
