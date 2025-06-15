import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Define get_transcript function
def get_transcript(video_id, max_retries=3, delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            return transcript, True
        except TranscriptsDisabled:
            st.error(f"Transcripts are disabled for video ID: {video_id}")
            return "", False
        except NoTranscriptFound:
            st.error(f"No English transcript found for video ID: {video_id}")
            return "", False
        except Exception as e:
            st.warning(f"Attempt {attempt}/{max_retries} - Error loading transcript: {e}")
            if attempt == max_retries:
                st.error(f"Failed to load transcript after {max_retries} attempts")
                return "", False
            time.sleep(delay)
    return "", False

# Define prompt
prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables=['context', 'question']
)

# Streamlit app
st.set_page_config(page_title="YouTube Q&A Bot", layout="wide")

# Custom CSS for Tailwind-like styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        font-family: 'Inter', sans-serif;
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .input-box {
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 0.375rem;
        border: 1px solid #d1d5db;
        width: 100%;
    }
    .button {
        background-color: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .button:hover {
        background-color: #2563eb;
    }
    .error {
        color: #dc2626;
        font-size: 0.875rem;
    }
    .success {
        color: #16a34a;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title">YouTube Q&A Bot</h1>', unsafe_allow_html=True)
st.write("Enter a YouTube video ID and ask questions about its transcript.")

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
    st.session_state.vector_store = None
    st.session_state.active_video_id = ""
    st.session_state.chunks_count = 0

# Input for YouTube video ID
video_id = st.text_input("YouTube Video ID", value="dQw4w9WgXcQ", placeholder="e.g., dQw4w9WgXcQ", key="video_id")
fallback_video_id = "L_jWHffIx5E"  # Fallback: TED Talk

# Button to load transcript
if st.button("Load Transcript", key="load_transcript", help="Fetch the video transcript"):
    with st.spinner("Fetching transcript..."):
        # Clear previous state
        st.session_state.transcript = ""
        st.session_state.vector_store = None
        st.session_state.active_video_id = ""
        st.session_state.chunks_count = 0

        # Try primary video ID
        transcript, success = get_transcript(video_id)
        active_video_id = video_id
        

        # Try fallback if primary fails
        if not success:
            st.warning(f"Trying fallback video ID: {fallback_video_id}")
            transcript, success = get_transcript(fallback_video_id)
            active_video_id = fallback_video_id if success else ""

        if success:
            st.session_state.transcript = transcript
            st.session_state.active_video_id = active_video_id
            # Process transcript
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.create_documents([transcript])
            st.session_state.chunks_count = len(chunks)
            st.success(f"Created {st.session_state.chunks_count} document chunks")
            
            # Create vector store
            try:
                embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
                st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)
                st.success("Vector store created successfully")
            except Exception as e:
                st.error(f"Error creating vector store: {e}")
        else:
            st.error("Could not load transcript from primary or fallback video ID.")

# Display transcript status
if st.session_state.transcript:
    st.markdown(f"<p class='success'>Using transcript from video ID: {st.session_state.active_video_id}</p>", unsafe_allow_html=True)
    with st.expander("View Transcript"):
        st.write(st.session_state.transcript)

# Question input and processing
if st.session_state.vector_store:
    question = st.text_input("Ask a question about the video", placeholder="e.g., What is the main theme of the video?", key="question")
    if st.button("Get Answer", key="get_answer", help="Generate answer based on transcript"):
        if not question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    # Set up retriever and chain
                    retriever = st.session_state.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
                    parser = StrOutputParser()

                    def format_docs(retrieved_docs):
                        return "\n\n".join(doc.page_content for doc in retrieved_docs)

                    parallel_chain = RunnableParallel({
                        'context': retriever | RunnableLambda(format_docs),
                        'question': RunnablePassthrough()
                    })

                    main_chain = parallel_chain | prompt | llm | parser

                    # Get answer
                    answer = main_chain.invoke(question)
                    st.markdown("**Question**: " + question)
                    st.markdown("**Answer**: " + answer)
                except Exception as e:
                    st.error(f"Error processing question: {e}")
else:
    st.warning("Please load a valid transcript before asking questions.")