from langchain.prompts import PromptTemplate
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from dotenv import load_dotenv
import os
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.vectorstores import Zilliz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def setup_backend():
    load_dotenv()

    llm = OctoAIEndpoint(
        octoai_api_token=os.getenv("OCTOAI_API_TOKEN"),
        endpoint_url="https://text.octoai.run/v1/chat/completions",
        model_kwargs={
            "model": "nous-hermes-2-mixtral-8x7b-dpo-fp16",
            "max_tokens": 4000,
            "presence_penalty": 0,
            "temperature": 0.1,
            "top_p": 0.92,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful twitter analyzer assistant. You will be given a twitter account tweet to analyze based on user prompt. Keep your responses limited to one short paragraph if possible.",
                },
            ],
        },
    )

    embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")
                                        
    vector_store = Zilliz(
        collection_name="biden_tweets",
        embedding_function=embeddings,
        connection_args={"uri": os.getenv("ZILLIZ_ENDPOINT"), "token": os.getenv("ZILLIZ_API_TOKEN")},
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
