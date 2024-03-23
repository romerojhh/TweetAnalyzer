from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from dotenv import load_dotenv
import os
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.vectorstores import Milvus
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def setup_backend():
    load_dotenv()

    OCTOAI_API_TOKEN = os.environ.get("OCTOAI_API_TOKEN")

    os.environ["OCTOAI_API_TOKEN"] = os.getenv("OCTOAI_API_TOKEN")

    template = """Below is an instruction that describes a task. Write a response that appropriately completes the request.\n Instruction:\n{question}\n Response: """
    prompt = PromptTemplate.from_template(template)

    llm = OctoAIEndpoint(
        endpoint_url="https://text.octoai.run/v1/chat/completions",
        model_kwargs={
            "model": "mixtral-8x7b-instruct-fp16",
            "max_tokens": 128,
            "presence_penalty": 0,
            "temperature": 0.01,
            "top_p": 0.9,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful twitter analyzer assistant. You will be given 2 twitter accounts to analyze based on user prompt. Keep your responses limited to one short paragraph if possible.",
                },
            ],
        },
    )

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")

    files = os.listdir("/Users/rhutapea/CodingProjects/TweetAnalyzer/data")

    file_texts = []

    for file in files:
        if (file != ".DS_Store"):
            with open(f"/Users/rhutapea/CodingProjects/TweetAnalyzer/data/{file}") as f:
                file_text = f.read()
            
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                encoding_name="cl100k_base", chunk_size=1024, chunk_overlap=256, 
            )
            texts = text_splitter.split_text(file_text)
            for i, chunked_text in enumerate(texts):
                if (len(chunked_text) < 10000):
                    name =  "Joe Biden tweeted: " if file == "JoeBiden.txt" else "Donald Trump tweeted: "
                    file_texts.append(Document(page_content=name + chunked_text, 
                        metadata={"twitter_user": file.split(".")[0], "chunk_num": i}))
                    
    vector_store = Milvus.from_documents(
        file_texts,
        embedding=embeddings,
        connection_args={"host": "localhost", "port": 19530},
        collection_name="twitter_user"
    )

    retriever = vector_store.as_retriever()

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = PromptTemplate.from_template(template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
