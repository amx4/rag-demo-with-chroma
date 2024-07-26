import getpass
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  
import google.generativeai as genai
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

app = Flask(__name__)
CORS(app)  

IS_DB_PRESENT = os.path.exists("./chroma_db") or False
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
chroma_db = Chroma(persist_directory='chroma_db', embedding_function=embeddings)

def get_relevant_passage(query: str):
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    docs = db.similarity_search(query)
    if docs:
        result = docs[0].page_content
        return result
    else:
        return None

def make_rag_prompt(query, relevant_passage):
    escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = (
        """You are a helpful and informative bot that answers questions using text from the reference passage included below. \
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
        However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
        strike a friendly and conversational tone. \
        If the passage is irrelevant to the answer, you may ignore it.
        QUESTION: '{query}'
        PASSAGE: '{relevant_passage}'

        ANSWER:
        """).format(query=query, relevant_passage=escaped)

    return prompt

def generate_answer(prompt):
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided. Please provide GOOGLE_API_KEY as an environment variable")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

def run_rag(query):
    relevant_text = get_relevant_passage(query)
    if not relevant_text:
        return "Sorry, I couldn't find any relevant text for your query."
    else:
        prompt = make_rag_prompt(query, relevant_passage="".join(relevant_text))
        answer = generate_answer(prompt)
        return answer


@app.route('/', methods=['GET'])
def index():
    streamlit_url = "http://localhost:8501"
    try:
        response = requests.get(streamlit_url)
        if response.status_code == 200:
            return f'''
            <html>
            <head>
                <title>LangChain Bot</title>
            </head>
            <body>
                <h1>Welcome to the LangChain Bot!</h1>
                <iframe src="{streamlit_url}" width="100%" height="800px"></iframe>
            </body>
            </html>
            '''
        else:
            raise Exception("Streamlit app is not healthy")
    except Exception as e:
        return f'''
        <html>
        <head>
            <title>LangChain Bot</title>
        </head>
        <body>
            <h1>Welcome to the LangChain Bot!</h1>
            <p>Sorry, the Streamlit app is currently unavailable. Please try again later.</p>
        </body>
        </html>
        '''

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        if file.filename.endswith('.pdf'):
            file_path = os.path.join(DATA_DIR, file.filename)
            file.save(file_path)
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
            global IS_DB_PRESENT
            IS_DB_PRESENT = True
            return jsonify({'message': 'File uploaded and ingested into Chroma DB'})
        else:
            return jsonify({'message': 'File must be a PDF!'})
    else:
        return jsonify({'message': 'No file uploaded'})

@app.route('/query', methods=['POST'])
def query_chroma():
    query = request.json.get('query', 'Default query')
    if IS_DB_PRESENT:
        answer = run_rag(query=query)
    else:
        answer = "No Chroma DB present. Please upload a PDF first."
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
