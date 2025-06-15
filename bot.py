# from langchain.text_splitter import RecursiveCharacterTextSplitter # text split
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI # vectores,llm call
# from langchain_community.vectorstores import FAISS # vector store
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv # api key call 
# from prompts import prompt 
# from yt_transcript import get_transcript

# from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
# from langchain_core.output_parsers import StrOutputParser
# parser = StrOutputParser()

# #step 1: 
# #Step 1a - Indexing (Document Ingestion)
# # is in  -->  yt_transcript.py
# video_id = "Gfr50f6ZBvo"
# transcript = get_transcript(video_id)

# if not transcript.strip():
#     raise ValueError("Transcript is empty. Cannot proceed with vector generation.")


# #Step 1b - Indexing (Text Splitting):

# splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
# chunks = splitter.create_documents([transcript])

# #Step 1c & 1d - Indexing (Embedding Generation and Storing in Vector Store):

# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# vector_store = FAISS.from_documents(chunks, embeddings)

# #Step 2 - Retrieval:

# retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# #retriever.invoke('What is deepmind')

# #Step 3 - Augmentation
# # is in ---> prompts.py

# # question          = "is the topic of nuclear fusion discussed in this video? if yes then what was discussed"
# #retrieved_docs    = retriever.invoke(question)

# #context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
# #context_text

# # final_prompt = prompt.invoke({"context": context_text, "question": question})

# #Step 4 - Generation

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

# # answer = llm.invoke(final_prompt)
# # print(answer.content)


# #Building a Chain:

# def format_docs(retrieved_docs):
#   context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
#   return context_text

# #chain:
# parallel_chain = RunnableParallel({
#     'context': retriever | RunnableLambda(format_docs),
#     'question': RunnablePassthrough()
# })


# #parallel_chain.invoke('who is Demis')

# #parser:


# # LCXL main_chain 
# main_chain = parallel_chain | prompt | llm | parser

# final_output = main_chain.invoke('What is deepmind')

# print(final_output)


# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.vectorstores import FAISS
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
# from dotenv import load_dotenv
# from langchain_core.output_parsers import StrOutputParser
# from prompts import prompt
# from yt_transcript import get_transcript
# import os

# # Load environment variables (OpenAI API key)
# load_dotenv()

# # Step 1: Get Transcript
# video_id = "dQw4w9WgXcQ"  # Rick Astley's "Never Gonna Give You Up"

# transcript = get_transcript(video_id)

# # Check if transcript is empty
# if not transcript.strip():
#     print(f"Error: Transcript for video ID {video_id} is empty or unavailable.")
#     print("Please try a different video ID or check if transcripts are enabled for this video.")
#     exit(1)  # Exit gracefully instead of raising an error

# # Step 1b: Text Splitting
# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# chunks = splitter.create_documents([transcript])
# print(f"[Created {len(chunks)} document chunks]")

# # Step 1c & 1d: Embedding Generation and Storing in Vector Store
# try:
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#     vector_store = FAISS.from_documents(chunks, embeddings)
#     print("[Vector store created successfully]")
# except Exception as e:
#     print(f"[Error creating vector store: {e}]")
#     exit(1)

# # Step 2: Retrieval
# retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# # Step 3: Augmentation (Defined in prompts.py)

# # Step 4: Generation
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
# parser = StrOutputParser()

# # Define format_docs function
# def format_docs(retrieved_docs):
#     context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
#     return context_text

# # Build the chain
# parallel_chain = RunnableParallel({
#     'context': retriever | RunnableLambda(format_docs),
#     'question': RunnablePassthrough()
# })

# # Main chain
# main_chain = parallel_chain | prompt | llm | parser

# # Test the chain
# try:
#     question = "What is the main theme or message of the song in the video?"
#     final_output = main_chain.invoke(question)
#     print("\n[Final Output]:")
#     print(final_output)
# except Exception as e:
#     print(f"[Error running the chain: {e}]")


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from prompts import prompt
from yt_transcript import get_transcript
import os

# Load environment variables (OpenAI API key)
load_dotenv()

# Step 1: Get Transcript
video_id = "dQw4w9WgXcQ"  # Primary video ID
fallback_video_id = "L_jWHffIx5E"  # Fallback: TED Talk with likely transcripts

transcript = get_transcript(video_id)
if not transcript.strip():
    print(f"[Warning: Transcript for video ID {video_id} is empty. Trying fallback video ID {fallback_video_id}]")
    transcript = get_transcript(fallback_video_id)
    if not transcript.strip():
        print(f"[Error: Transcript for fallback video ID {fallback_video_id} is also empty or unavailable.]")
        print("Please check if transcripts are enabled or try a different video ID.")
        exit(1)
    else:
        active_video_id = fallback_video_id
else:
    active_video_id = video_id

print(f"[Using transcript from video ID: {active_video_id}]")

# Step 1b: Text Splitting
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript])
print(f"[Created {len(chunks)} document chunks]")

# Step 1c & 1d: Embedding Generation and Storing in Vector Store
try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("[Vector store created successfully]")
except Exception as e:
    print(f"[Error creating vector store: {e}]")
    exit(1)

# Step 2: Retrieval
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Step 3: Augmentation (Defined in prompts.py)

# Step 4: Generation
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
parser = StrOutputParser()

# Define format_docs function
def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

# Build the chain
parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

# Main chain
main_chain = parallel_chain | prompt | llm | parser

# Test multiple relevant questions
questions = [
    "What is the main theme or message of the song in the video?",
    "Does the transcript include the phrase 'Never gonna give you up'? If so, how many times is it mentioned?",
    "What specific lyrics mention promises or commitments made in the song?",
    "Are there any references to love or relationships in the song's lyrics?",
    "What is the tone of the lyrics?"
]

for question in questions:
    try:
        final_output = main_chain.invoke(question)
        print("\n[Question]:", question)
        print("[Final Output]:", final_output)
    except Exception as e:
        print(f"[Error processing question '{question}': {e}]")