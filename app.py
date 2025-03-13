import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows us to keep sensitive information like API keys outside of our code
load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
# Using the client pattern is the recommended approach for the latest OpenAI SDK
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Flask app
# This creates a new web application instance
app = Flask(__name__)

# Function to load and parse the league rules PDF
def load_rules_pdf(file_path):
    """
    Loads and extracts text from a PDF file containing league rules.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF or an error message
    """
    try:
        # Open the PDF file in binary mode
        with open(file_path, 'rb') as file:
            # Create a PDF reader object
            pdf = PyPDF2.PdfReader(file)
            text = ""
            # Iterate through each page and extract text
            for page in pdf.pages:
                # The 'or ""' handles cases where extract_text returns None
                text += page.extract_text() or ""
            return text
    except Exception as e:
        # Log the error and return an error message
        app.logger.error(f"Error loading PDF: {str(e)}")
        return f"Error loading PDF: {str(e)}"

# Load the rules once at startup for efficiency
# This avoids having to read the PDF for each user request
rules_text = load_rules_pdf("league_rules.pdf")
if "Error" in rules_text:
    # Print the error to the console if PDF loading fails
    print(rules_text)

# Define the system prompt with rules context
# This provides instructions to the AI model about its role and knowledge base
system_prompt = (
    "You are a helpful chatbot for a recreational youth soccer league. "
    "You assist parents, coaches, and referees by answering questions based on the league rules. "
    "Here are the league rules for reference:\n\n" + rules_text + "\n\n"
    "Use this information to answer questions about league rules. For coaching best practices or equipment recommendations, "
    "use your web search tool to find recent, relevant information. Provide concise, friendly responses."
)

@app.route('/')
def index():
    """
    Route handler for the home page.
    Renders the chat interface template.
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint to handle chat requests and return AI responses.
    Receives user messages, processes them with OpenAI, and returns responses.
    """
    try:
        # Extract JSON data from the request
        data = request.json
        
        # Validate that we received data with a message field
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        # Get the user's message and remove whitespace
        user_input = data['message'].strip()
        
        # Check for empty messages after stripping
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Call OpenAI Responses API (synchronous call)
        # This is using the newer "Responses" API from OpenAI which combines web search
        # and chat capabilities for simpler implementation
        response = client.responses.create(
            model="gpt-4o",  # Using GPT-4o model for better quality responses
            tools=[{"type": "web_search"}],  # Enable web search capability
            input=user_input,  # The user's question
            instructions=system_prompt  # Context and instructions for the AI
        )

        # Extract the response text from the API response
        # The Responses API provides output in a simplified format
        response_text = response.output_text

        # Return the AI response as JSON
        return jsonify({'response': response_text})

    except Exception as e:
        # Log any errors that occur
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        # Return a user-friendly error message
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# This section only runs if this file is executed directly (not imported)
if __name__ == '__main__':
    # Check if the API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not set in environment variables.")
    else:
        # Show confirmation that the API key is loaded (first 5 chars for security)
        key = os.getenv('OPENAI_API_KEY')
        print(f"Starting server with OpenAI API key (first 5 chars): {key[:5]}...")
    
    # Start the Flask development server
    # debug=True enables automatic reloading when code changes
    app.run(debug=True, host='127.0.0.1', port=5000)