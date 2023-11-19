from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.llm import LLMChain
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import sys
import os
from IPython.display import Markdown, display
from langchain.vectorstores import FAISS
os.environ["OPENAI_API_KEY"] = "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"
file_path = r'D:\Code\IRchatBot\my-app\dataIR2.txt'

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

retriever = db.as_retriever(search_type="similarity_score_threshold",search_kwargs={"score_threshold": .8,"k": 1})
print(retriever.search_type)

docs = retriever.get_relevant_documents("Khu vực nào là trung tâm mua sắm?")

print(qa_pairs[docs[0].page_content])
openai = OpenAI(
    model_name="text-davinci-003",
    openai_api_key="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",
    temperature = 0.2
)
# param input là do người dùng nhập để hỏi
def get_answer(input):
  template = """Answer as a professional, friendly and enthusiastic tour guide for the question based on the context below. If the question cannot be answered using the information provided answer with "I don't know".Context: {qa}.Question: {query}. Answer: """
  prompt = PromptTemplate.from_template(
    template = template,
    input_variable = ["qa", "query"]
    )
  answer = openai(
    prompt.format(
        qa = qa_pairs[retriever.get_relevant_documents(input)[0].page_content],
        query=input
    ))
  return answer
app = Flask(__name__)
CORS(app)
@app.route('/api/add', methods=['POST'])
def add_strings():
    try:
        # Nhận chuỗi từ yêu cầu POST
        data = request.get_json()
        string1 = data['string1']

        # Tính tổng của hai chuỗi
        result = get_answer(string1)

        # Tạo đối tượng JSON để trả về
        response = {'result': result}

        return jsonify(response)

    except Exception as e:
        # Trả về lỗi nếu có vấn đề xảy ra
        error_response = {'error': str(e)}
        return jsonify(error_response), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
