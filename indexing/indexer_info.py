import chromadb

# more info: https://cookbook.chromadb.dev/core/collections
client = chromadb.PersistentClient(path="./chroma_langchain_db")
collections = client.list_collections()

print(collections)

# Iterate over collection
collection = client.get_or_create_collection(collections[0].name)
existing_count = collection.count()
batch_size = 10
for i in range(0, existing_count, batch_size):
    batch = collection.get(
        include=["metadatas", "documents", "embeddings"],
        limit=batch_size,
        offset=i)
    print(batch)  # do something with the batch
