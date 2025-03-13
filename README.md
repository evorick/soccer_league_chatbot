# Soccer League AI Helper Chatbot

## Overview

The Soccer League AI Helper Chatbot is a web-based conversational tool designed to assist parents, coaches, and referees in a recreational youth soccer league. Built with Flask and powered by OpenAI's Responses API, it provides real-time answers to questions about league rules, coaching best practices, and equipment recommendations.

### Features
- **League Rules Lookup**: Answers questions based on a provided `league_rules.pdf` (e.g., "What size ball for U10 games?").
- **Coaching Best Practices**: Searches the web for recent youth soccer coaching tips (e.g., "Best drills for 8-year-olds?").
- **Equipment Recommendations**: Suggests gear compliant with league rules using web searches (e.g., "Cleats for U8?").
- **Chat Interface**: A simple, responsive web UI for interacting with the chatbot.

### Technologies
- **Backend**: Python 3.9+, Flask, OpenAI Responses API, PyPDF2
- **Frontend**: HTML, CSS, JavaScript
- **Dependencies**: Listed in `requirements.txt`

---

## Prerequisites

- **Python 3.9+**: [Download here](https://www.python.org/downloads/)
- **OpenAI API Key**: Obtain from [OpenAI Platform](https://platform.openai.com/)
- **Text-Based PDF**: A `league_rules.pdf` file with readable text (not scanned images)

---

## Setup Instructions

### 1. Clone or Download the Project
- If using Git:
  ```bash
  git clone <repository-url>
  cd soccer_league_chatbot

---

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set in the `.env` file
- **Module Not Found Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## License

This project is licensed under the MIT License - see the LICENSE file for details.