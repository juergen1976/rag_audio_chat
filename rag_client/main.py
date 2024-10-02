import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

from AB_AudioChat.database import AudioChatDatabase

# set page title
st.set_page_config(page_title="AudioGPT Chat", page_icon="🎤", layout="wide")

st.image("./ai_bot.jpg", width=400)

st.sidebar.title("AudioGPT Chat")

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
                collection_name="Da_Jedox",
                embedding_function=embeddings,
                persist_directory="../indexing/chroma_langchain_db",  # Where to save data locally, remove if not neccesary
            )

    retriever = vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": 3,
                    "score_threshold": 0.4,
                })

    chain = ({"context": retriever, "question": RunnablePassthrough()}
                          | prompt
                          | model
                          | StrOutputParser())

    result = chain.invoke(question)

    st.write(result)

