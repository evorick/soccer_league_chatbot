# Product Requirements Document (PRD): Soccer League AI Helper Chatbot

## 1. Overview

### 1.1 Product Name
Soccer League AI Helper Chatbot

### 1.2 Purpose
The Soccer League AI Helper Chatbot assists parents, coaches, and referees in a local recreational youth soccer league by providing real-time, accurate, and contextually relevant information. The chatbot will:
- Answer questions about league-specific rules using a provided PDF document.
- Offer up-to-date best practices for coaching youth soccer through web searches.
- Help parents identify and shop for appropriate soccer equipment based on league rules via web searches.
- Deliver responses through an intuitive, Flask-based chat interface accessible via a web browser.

### 1.3 Target Audience
- **Parents**: Seeking guidance on league rules and equipment purchases for their children.
- **Coaches**: Looking for rule clarifications and modern coaching techniques for youth soccer.
- **Referees**: Needing quick access to league-specific rules for officiating games.

### 1.4 Problem Statement
Participants in the recreational soccer league often struggle with:
- Understanding nuanced league rules buried in lengthy documentation.
- Keeping up with evolving best practices for coaching youth soccer.
- Identifying equipment that complies with league standards without extensive research.
- Accessing this information conveniently during practices, games, or shopping.

The Soccer League AI Helper Chatbot addresses these challenges by providing a single, conversational point of access to tailored information.

## 2. Goals and Objectives

### 2.1 Goals
- Enhance participant experience by simplifying access to critical league information.
- Empower coaches with current, evidence-based coaching strategies.
- Ensure equipment purchases align with league requirements, saving time and reducing errors.
- Provide a user-friendly chat interface for real-time assistance.

### 2.2 Success Metrics
- **User Engagement**: 75% of league participants (parents, coaches, referees) use the chatbot at least once per season.
- **Accuracy**: 95% of responses correctly reference league rules or provide relevant web-sourced information.
- **Response Time**: Average response time under 5 seconds.
- **Satisfaction**: 80% positive feedback in a post-season survey on usability and helpfulness.

## 3. Features and Functionality

### 3.1 Core Features

#### 3.1.1 League Rules Lookup
- **Description**: The chatbot can interpret and respond to questions about league rules by referencing a provided PDF document (e.g., "What size ball is used for U10 games?").
- **Requirements**:
  - Upload and parse a static PDF containing the league’s rules (e.g., using `PyPDF2` or OpenAI’s document understanding capabilities).
  - Store extracted text in a format accessible to the AI agent (e.g., vectorized embeddings for semantic search).
  - Respond with direct quotes or summaries from the PDF, with context (e.g., "According to Section 2.3 of the rules, U10 games use a size 4 ball.").

#### 3.1.2 Web Search for Coaching Best Practices
- **Description**: The chatbot searches the web for recent best practices in coaching youth soccer (e.g., "What are the latest tips for coaching 8-year-olds?").
- **Requirements**:
  - Integrate a web search capability (e.g., via a custom implementation using `requests` and `beautifulsoup4` or a third-party API) to fetch current articles, blogs, or studies (within the last 1-2 years).
  - Summarize findings in a concise, actionable format (e.g., "Recent articles suggest focusing on small-sided games to improve engagement for 8-year-olds.").

#### 3.1.3 Equipment Recommendations
- **Description**: The chatbot helps parents shop for equipment compliant with league rules by searching the web (e.g., "What cleats should I buy for my U8 player?").
- **Requirements**:
  - Cross-reference league rules from the PDF (e.g., "No metal cleats allowed") with web search results.
  - Provide specific product suggestions or criteria (e.g., "Look for youth soccer cleats with molded plastic studs, available at retailers like Amazon or Dick’s Sporting Goods.").

#### 3.1.4 Flask-Based Chat Interface
- **Description**: A web-based UI built with Flask where users can type questions and receive responses in a conversational format.
- **Requirements**:
  - Simple, responsive HTML/CSS/JavaScript frontend (e.g., a chat window with input box and message history).
  - Backend Flask server to handle user inputs, API calls, and response rendering.
  - Real-time message display without page refresh (e.g., using AJAX or WebSockets).

### 3.2 Non-Functional Requirements
- **Availability**: Accessible whenever local server has been started.
- **Scalability**: Handle up to 100 concurrent users (assuming a small league).
- **Security**: Protect the PDF and user interactions with basic authentication (e.g., username/password for league members).
- **Performance**: Responses delivered within 5 seconds under normal load.

## 4. Technical Requirements

### 4.1 Technology Stack
- **Backend**:
  - Python 3.9+ with Flask for the web server.
  - OpenAI Chat Completions API (via `openai` Python SDK) for AI responses.
  - `PyPDF2` for PDF parsing.
  - `requests` and `beautifulsoup4` for web search functionality.
- **Frontend**:
  - HTML/CSS/JavaScript for the chat UI.
  - Bootstrap for responsive design (optional).
- **Dependencies**:
  - Listed in `requirements.txt`.
- **Hosting**:
  - Local deployment (e.g., on a Raspberry Pi) or cloud (e.g., Heroku, AWS).

### 4.2 API Integration
- **OpenAI Chat Completions API**:
  - Use the `chat.completions.create` endpoint.
  - Example call:
    ```python
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are the latest coaching tips for youth soccer?"}
        ]
    )
    ```
  - Pass the PDF content as part of the system prompt.

### 4.3 Data Sources
- **League Rules PDF**: Static file uploaded by the league administrator.
- **Web Search**: Real-time results via a custom web search implementation (e.g., using DuckDuckGo HTML scraping).

## 5. User Interface Mockup

### 5.1 Chat Interface
- **Layout**:
  - **Top**: Header with title "Soccer League AI Helper".
  - **Middle**: Scrollable chat window showing conversation history.
  - **Bottom**: Text input box with a "Send" button.
- **Example Interaction**:

**User:** What size ball for U12 games?  
**Bot:** According to the league rules PDF (Section 2.2), U12 games use a size 4 ball.

**User:** Best drills for 10-year-olds?  
**Bot:** Recent web sources suggest small-sided games like 3v3 to boost engagement and skill development for 10-year-olds.

**User:** Cleats for U8?  
**Bot:** Per the rules (Section 4.1), no metal cleats are allowed. Search results recommend youth soccer cleats with molded plastic studs, like the Nike Jr. Mercurial, available at Amazon.


## 6. User Stories

1. **As a parent**, I want to ask about equipment rules so I can buy the right gear for my child.
 - **Acceptance**: Bot references the PDF and suggests compliant products.
2. **As a coach**, I want recent coaching tips so I can improve my practice sessions.
 - **Acceptance**: Bot provides summarized web-sourced tips from the last 1-2 years.
3. **As a referee**, I want quick rule clarifications so I can officiate games accurately.
 - **Acceptance**: Bot quotes the exact rule from the PDF with section reference.
4. **As a user**, I want a simple chat interface so I can get answers without technical hassle.
 - **Acceptance**: Flask UI loads in a browser, accepts input, and displays responses.

## 7. Constraints and Assumptions

### 7.1 Constraints
- OpenAI API costs (requires an API key and budget).
- PDF must be provided in a readable format (no scanned images).
- Web search accuracy depends on the custom implementation’s capabilities.

### 7.2 Assumptions
- League rules PDF is static and updated manually by an admin.
- Users have basic internet access and a modern browser.
- The league is small (under 200 participants), limiting scalability needs.

## 8. Milestones and Timeline

### 8.1 Phase 1: Prototype (1 Day)
- Set up Flask server and basic chat UI.
- Integrate OpenAI Chat Completions API with a test prompt.
- Parse and test PDF rule lookup.
- Add web search for coaching tips and equipment.
- Refine response formatting and accuracy.
- Implement basic authentication.
- Deploy locally.
- Test with 10-20 league participants.
- Gather feedback and fix bugs.

### 8.2 Phase 2: Potential Improvements (1 Week)
- Fix any formatting issues from the response.
- Host the chatbot so that it can be accessible outside of localhost.


## 9. Risks and Mitigation

- **Risk**: OpenAI API rate limits or costs exceed budget.
- **Mitigation**: Cache frequent responses; set usage quotas.
- **Risk**: PDF parsing fails for complex layouts.
- **Mitigation**: Pre-process PDF into text manually if needed.
- **Risk**: Web search results are outdated or irrelevant.
- **Mitigation**: Filter results by date; allow manual override with trusted sources.

## 10. Appendix

### 10.1 Sample Code Snippet
Here’s a starting point for the Flask backend:

```python
from flask import Flask, request, jsonify
import openai
import PyPDF2

app = Flask(__name__)
openai.api_key = "your-api-key"

# Load and parse PDF
def load_rules_pdf(file_path):
  with open(file_path, 'rb') as file:
      pdf = PyPDF2.PdfReader(file)
      text = ""
      for page in pdf.pages:
          text += page.extract_text()
  return text

rules_text = load_rules_pdf("league_rules.pdf")

@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  user_input = data.get('message', '').strip()
  
  response = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
          {"role": "system", "content": f"You are a helper for a soccer league. Use this context for rules: {rules_text}"},
          {"role": "user", "content": user_input}
      ]
  )
  
  return jsonify({'response': response.choices[0].message.content})

if __name__ == '__main__':
  app.run(debug=True, port=5000)