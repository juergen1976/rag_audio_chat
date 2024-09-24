import chromadb
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import SentenceTransformerEmbeddings
from transformers.models.cvt.convert_cvt_original_pytorch_checkpoint_to_pytorch import embeddings

from AB_AudioChat.database import AudioChatDatabase


# 1. Read the teams and topics from the postgres database
audio_database = AudioChatDatabase()
teams = audio_database.get_teams()
print(teams)

# get all collections
client = chromadb.PersistentClient(path="../indexing/chroma_langchain_db")
collections = client.list_collections()
print(collections)

model = ChatOllama(model="llama3")

prompt = PromptTemplate.from_template(
            """
            <s> [INST]Beantworte die Frage im Kontext. Wenn der Kontext die snicht enthält sage du hast keine Informationen dazu.[/INST] </s> 
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

# # test search in vector store
# # more info: https://python.langchain.com/docs/integrations/vectorstores/chroma/
# results = vector_store.similarity_search_with_score(
#     "Ist die Installation sehr einfach zu machen ?", k=3,
# )
# for res, score in results:
#     print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")

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

result = chain.invoke("Kann man die Installation einfach machen ?")
print(result)
