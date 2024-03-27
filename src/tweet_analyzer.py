from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from dotenv import load_dotenv
import os
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.vectorstores import Milvus
from langchain.text_splitter import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def setup_backend():
    load_dotenv()

    print(os.getenv("OCTOAI_API_TOKEN"))

    llm = OctoAIEndpoint(
        octoai_api_token=os.getenv("OCTOAI_API_TOKEN"),
        endpoint_url="https://text.octoai.run/v1/chat/completions",
        model_kwargs={
            "model": "llama-2-70b-chat-fp32",
            "max_tokens": 256,
            "presence_penalty": 0,
            "temperature": 0.1,
            "top_p": 0.92,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful twitter analyzer assistant. You will be given 2 twitter accounts to analyze based on user prompt. Keep your responses limited to one short paragraph if possible.",
                },
            ],
        },
    )

    embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")

    files = os.listdir("/Users/rhutapea/CodingProjects/TweetAnalyzer/data")

    file_texts = []

    for file in files:
        if (file != ".DS_Store"):
            with open(f"/Users/rhutapea/CodingProjects/TweetAnalyzer/data/{file}") as f:
                file_text = f.read()
            
            # text_splitter = CharacterTextSplitter(
            #     separator="\n",
            #     chunk_size=1000,
            #     chunk_overlap=200,
            #     length_function=len,
            #     is_separator_regex=False,
            # )

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                encoding_name="cl100k_base",
                chunk_size=1024,
                chunk_overlap=256,
            )

            # text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            #     encoding_name="cl100k_base", chunk_size=1024, chunk_overlap=256, 
            # )

            texts = text_splitter.split_text(file_text)
            # texts = text_splitter_new.create_documents([file_text])
            for i, chunked_text in enumerate(texts):
                if (len(chunked_text) < 10000):
                    name =  "Joe Biden tweeted: " if file == "JoeBiden.txt" else "Donald Trump tweeted: "
                    file_texts.append(Document(page_content=name + chunked_text, 
                        metadata={"tweet_source": file.split(".")[0], "chunk_num": i}))
                                        
    vector_store = Milvus.from_documents(
        file_texts,
        embedding=embeddings,
        connection_args={"host": "localhost", "port": 19530},
        collection_name="twitter_user"
    )

    retriever = vector_store.as_retriever()

    template = """Answer the question based only on the following context:
    {context}

    Note that the word "posted" can be used interchangeably with "tweeted"

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
