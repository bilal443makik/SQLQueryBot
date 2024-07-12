# SQLQueryBot
SQLQueryBot is a powerful web-based application designed to simplify data interaction for users by leveraging the capabilities of OpenAI's GPT-3.5-turbo model. It offers an intuitive interface where users can easily upload CSV files and query the data using natural language, eliminating the need for complex SQL knowledge. 
# app.py:
app.py is the main application file for SQLQueryBot. It sets up a Flask web server to handle CSV uploads and user queries. The script uses OpenAI's GPT-3.5-turbo model to convert natural language queries into SQL commands, which are then executed against the uploaded CSV data stored in an SQLite database. Key functionalities include handling file uploads, processing the CSV data, creating the SQL agent, and managing query requests.
# index.html:
index.html is the main user interface for the SQLQueryBot application. It provides a form for users to upload CSV files and another form to enter natural language queries. The HTML file includes necessary styling and JavaScript functions to handle file uploads and query submissions, displaying results directly on the page.
# requirements.txt:
requirements.txt lists all the Python dependencies required to run the SQLQueryBot application. This includes Flask for the web framework, pandas for handling CSV data, SQLAlchemy for database interactions, and various langchain libraries for the integration with OpenAI's language model.
# sample_data.csv:
sample_data.csv is an example CSV file that can be used to test the application. It contains sample data to demonstrate how SQLQueryBot processes and queries the uploaded CSV data.
# Technologies Used
**Flask**: For the web framework.
**Pandas:** For CSV data manipulation.
**SQLAlchemy: **For database interactions.
**OpenAI GPT-3.5-turbo: **For converting natural language queries into SQL commands.
**JavaScript:** For handling file uploads and query submissions.

## Steps to Run This Project

**Clone the Repository:**
   
   git clone https://github.com/your_username/SQLQueryBot.git

   cd SQLQueryBot

   python -m venv venv

   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   pip install -r requirements.txt

   export OPENAI_API_KEY="your_openai_api_key"  # On Windows, use `set OPENAI_API_KEY=your_openai_api_key`

   python app.py





This `README.md` provides a comprehensive overview of the project, instructions for setting it up and running it, descriptions of the key files, and additional project details.
