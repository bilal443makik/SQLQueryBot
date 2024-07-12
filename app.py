import os
import pandas as pd
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from flask import Flask, request, jsonify, render_template, abort
from werkzeug.utils import secure_filename

# Initialize Flask application
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Max file size 16MB

# Function to load CSV into SQL agent and return agent_executor
def load_csv_to_sql_agent(csv_path, db_path):
    os.environ["OPENAI_API_KEY"] = "OPEN_AI_API_KEY"
    model_name = "gpt-3.5-turbo-0125"
    
    df = pd.read_csv(csv_path)
    
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql("store", engine, index=False, if_exists='replace')
    
    db = SQLDatabase(engine=engine)
    
    llm = ChatOpenAI(model=model_name)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
    
    return agent_executor

# # Function to invoke SQL agent with a single query
# def invoke_sql_agent(agent_executor, user_query):
#     result = agent_executor.invoke({"input": user_query})
#     return result
# Function to invoke SQL agent with a single query
def invoke_sql_agent(agent_executor, user_query):
    # Example usage:
    prompt = '''These are the names of my DataFrame Table. first take the users prompt and match the users Query with the table
    name (with which it matches the most) 
    "itemName"	"Item-Subcategory"	"Price (USD)"	"Promotion"	"BranchName"	"Rak-Location"'''
    FinalPrompt = f" instructions: {prompt}/n  Query:{user_query}"

    # Invoke the SQL agent with the user query
    result = agent_executor.invoke({"input": FinalPrompt})
    return result

# Route to serve the HTML interface
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle CSV uploads
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csvFile' not in request.files:
        return jsonify(error='No file part'), 400
    
    file = request.files['csvFile']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Load the uploaded CSV into the SQL agent
        db_path = "store.db"
        agent = load_csv_to_sql_agent(file_path, db_path)
        
        return jsonify(message='File successfully uploaded and processed'), 200
    
    return jsonify(error='File upload failed'), 400

# API endpoint to handle POST requests containing queries
@app.route('/query', methods=['POST'])
def handle_query():
    request_data = request.get_json()
    
    if not request_data or 'queries' not in request_data:
        abort(400, description='No valid JSON data or queries provided')
    
    queries = request_data['queries']
    
    # Assume the CSV has already been loaded
    db_path = "store.db"
    agent = load_csv_to_sql_agent("SupppperrStore.csv", db_path)  # This would be dynamic in real implementation
    
    results = []
    for query in queries:
        result = invoke_sql_agent(agent, query)
        results.append(result)
    
    return jsonify(results=results)

if __name__ == '__main__':
    app.run(debug=True)
