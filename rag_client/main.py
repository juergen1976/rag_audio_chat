import streamlit as st
from langchain.retrievers import EnsembleRetriever
from langchain_community.chat_models import ChatOllama
from langchain_community.retrievers import BM25Retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from AB_AudioChat.database import AudioChatDatabase

st.set_page_config(page_title="AudioGPT Chat", page_icon="🎤", layout="wide")

st.header("AudioGPT Chat")

st.image("./ai_bot.jpg", width=300)

audio_database = AudioChatDatabase()
teams = audio_database.get_teams()

# Streamlit Selectbox
selected_team = st.selectbox("Select a team", options=teams, format_func=lambda team: team[1])

# get topics for teams
topics = audio_database.get_topics_for__team_id(selected_team[0])

selected_topic = st.selectbox("Select a topic", options=topics, format_func=lambda topic: topic[1])

collection_name = f"{selected_team[1][0:2]}_{selected_topic[1]}"

st.write(f"Collection name used for vector search: {collection_name}")

# User prompt in multiple lines
question = st.text_area("Enter your question", height=100)

# submit button
if st.button("Ask"):

    model = ChatOllama(model="llama3")

    prompt = PromptTemplate.from_template(
                """
                <s> [INST]Answer the question based on the information in the given context. If there is no context, say you don't know the answer.[/INST] </s> 
                [INST] Question: {question} 
                Context: {context} 
                Answer: [/INST]
                """
    )

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory="../indexing/chroma_langchain_db",  # Where to save data locally, remove if not neccesary
            )

    # -----------------------------------------------------------------------------------
    # Ensemble retriever with BM25 and vector search
    # -----------------------------------------------------------------------------------

    # Vanilla similarity search retriever
    retriever_similarity_search = vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": 3,
                    "score_threshold": 0.4,
                })

    # BM25 retriever
    all_texts= audio_database.get_all_transcribed_text_for_team_and_topic(selected_team[0], selected_topic[0])
    all_texts_as_list = [text[0] for text in all_texts]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    # create documents


    all_documents = [Document(page_content=doc) for doc in all_texts_as_list]
    chunks = text_splitter.split_documents(all_documents)
    retriever_BM25 = BM25Retriever.from_documents(chunks, search_kwargs={"k": 4})

    # Ensemble retriever with 40% BM25 and 60% similarity search
    ensemble_retriever = EnsembleRetriever(retrievers=[retriever_BM25, retriever_similarity_search],
                                           weights=[0.4, 0.6])
    chain = ({"context": ensemble_retriever , "question": RunnablePassthrough()}
                          | prompt
                          | model
                          | StrOutputParser())

    result = chain.invoke(question)

    st.write(result)

