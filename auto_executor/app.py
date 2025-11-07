from flask import Flask, request, jsonify
import os
import zipfile
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import io
from loguru import logger
from utility.azure_api import AzureOpenAIClient
from utility.extraction import Extraction

app = Flask(__name__)

# Configure loguru
logger.add("logs/auto_executor_{time}.log", rotation="500 MB", retention="10 days", level="INFO")
logger.add("logs/error_{time}.log", rotation="100 MB", retention="30 days", level="ERROR")

# Configuration
UPLOAD_FOLDER = 'uploads'
EXTRACTED_FOLDER = 'extracted_projects'
ALLOWED_EXTENSIONS = {'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACTED_FOLDER'] = EXTRACTED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max file size

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)
os.makedirs('logs', exist_ok=True)

logger.info("Auto Executor application started")


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_zip_file(file_object, extract_to):
    """Extract a zip file from file object to the specified directory"""
    try:
        # Read file object into memory
        file_bytes = io.BytesIO(file_object.read())

        with zipfile.ZipFile(file_bytes, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True, "Extraction successful"
    except zipfile.BadZipFile:
        return False, "Invalid zip file"
    except Exception as e:
        return False, f"Extraction failed: {str(e)}"


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'auto_executor',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/submit-project', methods=['POST'])
def submit_project():
    """
    Endpoint to receive project submission with zip file and metadata

    Expected form data:
    - project_file: zip file containing the project
    - problem_statement: description of the problem
    - problem_statement_id: unique identifier for the problem statement
    - user_story: user story the project is addressing
    """
    logger.info("Received project submission request")

    # Validate that all required fields are present
    if 'project_file' not in request.files:
        logger.warning("Request missing project_file")
        return jsonify({'error': 'No project_file provided'}), 400

    if 'problem_statement' not in request.form:
        logger.warning("Request missing problem_statement")
        return jsonify({'error': 'No problem_statement provided'}), 400

    if 'problem_statement_id' not in request.form:
        logger.warning("Request missing problem_statement_id")
        return jsonify({'error': 'No problem_statement_id provided'}), 400

    if 'user_story' not in request.form:
        logger.warning("Request missing user_story")
        return jsonify({'error': 'No user_story provided'}), 400

    # Get the uploaded file
    file = request.files['project_file']

    if file.filename == '':
        logger.warning("No file selected in upload")
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Only .zip files are allowed'}), 400

    # Get metadata
    problem_statement = request.form['problem_statement']
    problem_statement_id = request.form['problem_statement_id']
    user_story = request.form['user_story']

    logger.info(f"Processing submission for problem_statement_id: {problem_statement_id}")

    try:
        # Create a unique directory for this submission
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        submission_id = f"{problem_statement_id}_{timestamp}"
        submission_dir = os.path.join(app.config['UPLOAD_FOLDER'], submission_id)
        os.makedirs(submission_dir, exist_ok=True)
        logger.info(f"Created submission directory: {submission_id}")

        # Save the zip file to disk
        filename = secure_filename(file.filename)
        zip_file_path = os.path.join(submission_dir, filename)
        file.save(zip_file_path)
        logger.info(f"Saved zip file: {filename} to {submission_dir}")

        # Upload file to Azure OpenAI
        logger.info("Uploading file to Azure OpenAI")
        azure_client = AzureOpenAIClient()
        upload_file = azure_client.upload_file(zip_file_path, purpose='assistants')

        if not upload_file['success']:
            logger.error(f"Failed to upload file to Azure OpenAI: {upload_file['error']}")
            return jsonify({
                'error': f'Failed to upload file to Azure OpenAI: {upload_file["error"]}',
                'submission_id': submission_id
            }), 500

        logger.success(f"File uploaded to Azure OpenAI with file_id: {upload_file['file_id']}")

        # Read the askbit prompt template
        logger.info("Reading instruction prompt template")
        prompt_file_path = os.path.join('prompts', 'instructions', 'analysis' ,'askbit.txt')
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            instruction_template = f.read()

        # Format the instruction with actual values
        instruction = instruction_template.format(
            file_id=upload_file['file_id'],
            problem_statement=problem_statement,
            user_story=user_story
        )

        # User prompt to execute the task
        user_prompt = "Please analyze the submitted project according to the instructions provided."

        # Make LLM call using get_completion
        logger.info("Making first LLM call for project analysis")
        llm_response, llm_status = azure_client.get_completion(
            instruction=instruction,
            user_prompt=user_prompt,
            file_id_list=[upload_file['file_id']],
            eval_=False,
            code_interpreter=True
        )
        logger.info(f"First LLM call completed with status: {llm_status}")

        # Extract reasoning and conclusion from response
        logger.info("Extracting reasoning and conclusion from LLM response")
        reasoning = Extraction.extract_text_from_tag(llm_response, 'reasoning')
        conclusion = Extraction.extract_json_from_tag(llm_response, 'conclusion')
        logger.info(f"Extracted conclusion: {conclusion}")

        # Initialize script generation variables
        script_generation_response = None
        generated_script = None
        extract_dir = None

        # Check if both python conditions are True
        if conclusion and conclusion.get('python') == True and conclusion.get('output_handled_by_python') == True and conclusion.get("path_output"):
            logger.info("Python conditions met, proceeding with script generation")

            # Read the script generation prompt template
            output_path = conclusion.get("path_output")
            logger.info(f"Output path from conclusion: {output_path}")

            # Extract the zip file to get the unzipped folder path
            extract_dir = os.path.join(app.config['EXTRACTED_FOLDER'], submission_id,output_path)
            print(extract_dir)
            os.makedirs(extract_dir, exist_ok=True)
            logger.info(f"Extracting zip file to: {extract_dir}")

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            logger.success(f"Zip file extracted successfully to: {extract_dir}")

            script_gen_prompt_path = os.path.join('prompts', 'instructions' ,'script_gen', 'askbit.txt')
            script_gen_multiple_run_op = os.path.join('test_data', 'askbit.txt')
            with open(script_gen_prompt_path, 'r', encoding='utf-8') as f:
                script_gen_template = f.read()
            with open(script_gen_multiple_run_op, 'r', encoding='utf-8') as f:
                multiple_run_data = f.read()

            # Format the instruction with actual values
            script_gen_instruction = script_gen_template.format(
                file_id=upload_file['file_id'],
                multiple_run_data=multiple_run_data,
                output_file_path=extract_dir,
                # extracted_project_path=extract_dir
            )

            # User prompt for script generation
            script_gen_user_prompt = "Please generate the Python script to execute and test the project."

            # Make second LLM call for script generation
            logger.info("Making second LLM call for script generation")
            script_generation_response, script_gen_status = azure_client.get_completion(
                instruction=script_gen_instruction,
                user_prompt=script_gen_user_prompt,
                file_id_list=[upload_file['file_id']],
                eval_=False,
                code_interpreter=True
            )
            logger.info(f"Second LLM call completed with status: {script_gen_status}")

            # Extract the generated script from <script> tags
            generated_script = Extraction.extract_text_from_tag(script_generation_response, 'script')
            if generated_script:
                logger.success("Successfully extracted generated script")
            else:
                logger.warning("No script found in <script> tags")
        else:
            logger.info("Python conditions not met, skipping script generation")

        # Save metadata
        metadata = {
            'submission_id': submission_id,
            'problem_statement_id': problem_statement_id,
            'problem_statement': problem_statement,
            'user_story': user_story,
            'original_filename': filename,
            'upload_timestamp': timestamp,
            'zip_file_path': zip_file_path,
            'azure_file_id': upload_file['file_id'],
            'azure_file_status': upload_file['status'],
            'file_size_bytes': upload_file['bytes'],
            'llm_analysis': {
                'reasoning': reasoning,
                'conclusion': conclusion,
                'full_response': llm_response,
                'status': llm_status
            },
            'script_generation': {
                'generated': generated_script is not None,
                'script': generated_script,
                'extracted_project_path': extract_dir,
                'full_response': script_generation_response
            } if generated_script else None
        }

        # Save metadata to JSON file
        logger.info("Saving metadata to JSON file")
        metadata_path = os.path.join(submission_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.success(f"Metadata saved successfully to {metadata_path}")

        logger.success(f"Project submission {submission_id} processed successfully")

        return jsonify({
            'status': 'success',
            'message': 'Project submitted, analyzed, and uploaded to Azure OpenAI successfully',
            'submission_id': submission_id,
            'azure_file_id': upload_file['file_id'],
            'analysis': {
                'reasoning': reasoning,
                'conclusion': conclusion
            },
            'metadata': metadata
        }), 200

    except Exception as e:
        logger.exception(f"Error processing submission: {str(e)}")
        return jsonify({
            'error': f'Failed to process submission: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
