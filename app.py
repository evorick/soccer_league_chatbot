import os
import re
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import PyPDF2
from dotenv import load_dotenv
import markdown

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Flask app
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
        with open(file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        app.logger.error(f"Error loading PDF: {str(e)}")
        return f"Error loading PDF: {str(e)}"

# Load the rules once at startup for efficiency
rules_text = load_rules_pdf("league_rules.pdf")
if "Error" in rules_text:
    print(rules_text)

# Define the system prompt with rules context
system_prompt = (
    "You are a helpful chatbot for a recreational youth soccer league. "
    "You assist parents, coaches, and referees by answering questions based on the league rules. "
    "Here are the league rules for reference:\n\n" + rules_text + "\n\n"
    "Use this information to answer questions about league rules. For coaching best practices or equipment recommendations, "
    "use your web search tool to find recent, relevant information. Provide concise, friendly responses."
)

def format_response(text):
    """Formats response text for better display in HTML, handling Markdown, links, and formatting."""
    
    # Convert Markdown to HTML
    text = markdown.markdown(text)

    # Ensure Markdown-style links are correctly formatted: [text](URL) -> <a href="URL">text</a>
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)

    # Ensure raw URLs are also clickable (if not already wrapped in <a> tags)
    text = re.sub(r'(?<!href=")(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', text)

    # Ensure links open in a new tab
    text = re.sub(r'<a ', r'<a target="_blank" ', text)

    return text

@app.route('/')
def index():
    """Route handler for the home page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint to handle chat requests and return AI responses.
    Receives user messages, processes them with OpenAI, and returns responses.
    """
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        user_input = data['message'].strip()
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        response = client.responses.create(
            model="gpt-4o",
            tools=[{"type": "web_search"}],
            input=user_input,
            instructions=system_prompt
        )

        formatted_response = format_response(response.output_text)

        return jsonify({'response': formatted_response})

    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not set in environment variables.")
    else:
        key = os.getenv('OPENAI_API_KEY')
        print(f"Starting server with OpenAI API key (first 5 chars): {key[:5]}...")

    app.run(debug=True, host='127.0.0.1', port=5000)
