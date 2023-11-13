from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import sys
import os
from IPython.display import Markdown, display
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = "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"
file_path = r'C:\Users\Admin\Downloads\dataIR.txt'

def load_qa_pairs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    qa_pairs = {}
    current_question = None

    for line in lines:
        line = line.strip()
        if line.startswith("Q: "):
            current_question = line[3:]
        elif line.startswith("A: ") and current_question:
            qa_pairs[current_question] = line[3:]

    return qa_pairs
qa_pairs = load_qa_pairs(file_path)

questions = list(qa_pairs.keys())
answers = list(qa_pairs.values())

print(questions)

# Get embedding model
embeddings = OpenAIEmbeddings()
# Create vector database
db = FAISS.from_texts(questions,embeddings)

retriever = db.as_retriever(search_type="similarity_score_threshold",search_kwargs={"score_threshold": .9,"k": 5})
print(retriever.search_type)

docs = retriever.get_relevant_documents("Khu vực nào là trung tâm mua sắm?")

print(qa_pairs[docs[0].page_content])

app = Flask(__name__)
CORS(app)
@app.route('/api/add', methods=['POST'])
def add_strings():
    try:
        # Nhận chuỗi từ yêu cầu POST
        data = request.get_json()
        string1 = data['string1']
        docs = retriever.get_relevant_documents(string1)

        # Tính tổng của hai chuỗi
        result = qa_pairs[docs[0].page_content]

        # Tạo đối tượng JSON để trả về
        response = {'result': result}

        return jsonify(response)

    except Exception as e:
        # Trả về lỗi nếu có vấn đề xảy ra
        error_response = {'error': str(e)}
        return jsonify(error_response), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
