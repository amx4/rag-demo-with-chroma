# Chroma Demo with Google Generative AI

This is a Flask application that demonstrates the use of Chroma vector store and Google Generative AI for question-answering tasks. The application allows users to upload PDF files, which are then ingested into the Chroma vector store. Users can then submit queries, and the application will retrieve relevant passages from the uploaded PDF files and generate an answer using Google Generative AI.

## Prerequisites

Before running the application, make sure you have the following:
- Python 3.x installed
- Google API key (for Google Generative AI)

## Installation

1. Clone the repository:
   
   git clone 'this repository'
   

2. Navigate to the project directory:
   
   cd chroma-demo
   

3. Create a virtual environment (optional but recommended):
   
   python -m venv venv
   source venv/bin/activate
   

   On Windows, use:
   
   venv\Scripts\activate
   

4. Install the required dependencies:
   
   pip install -r requirements.txt
   

5. Set the GOOGLE_API_KEY environment variable with your Google API key:
   
   export GOOGLE_API_KEY=your_google_api_key
   

   On Windows, use:
   
   set GOOGLE_API_KEY=your_google_api_key
   

## Usage

### Using Docker
1. Build the app.
`docker build -t rag-demo .`

2. Run the docker command to start the app.
`docker run -p 8000:8000 8501:8501 rag-demo`

3. You can access the Flask API server om http://localhost:8000 and Streamlit UI on http://localhost:8501 (default).

### Using API
1. Run the Flask application:
   
   python3 main.py
   

2. Upload a PDF file by sending a POST request to http://localhost:8000/upload with the file in the request body.

3. Query the Chroma vector store by sending a POST request to http://localhost:5000/query with the query in the request body as JSON:
   
   {
       "query": "your query here"
   }
   

   The application will return a JSON response with the generated answer.

### Using Streamlit UI app
1. Run the Flask application:
2. Ran the Streamlit app. The page will run at `localhost:8501` by default.
3. Upload a PDF file by clicking the "Upload" button.
4. Query the Chroma vector store by entering the query in the "Query" text box and click submit.


## File Structure

- main.py: The main Flask application file.
- data/: Directory for storing uploaded PDF files.
- chroma_db/: Directory for storing the Chroma vector store.

## Dependencies

The application uses the following main dependencies:
- Flask
- Google Generative AI
- Langchain
- Chroma

For a complete list of dependencies, see the requirements.txt file.

