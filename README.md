markdown
# 🎥 YouTube Q&A Bot using Transcripts, LangChain & OpenAI

This project allows users to ask questions about a YouTube video, and receive intelligent answers based on the video's transcript. It uses `youtube-transcript-api` to fetch captions, LangChain for chunking and vector search, FAISS for storing embeddings, and OpenAI's GPT model for answering questions.

## 🚀 Features

- Fetches transcript of a YouTube video (if available).
- Splits text into manageable chunks using LangChain.
- Embeds chunks using OpenAI Embeddings (`text-embedding-3-small`).
- Stores and searches embeddings using FAISS vector store.
- Uses GPT (ChatOpenAI) to answer questions based on transcript content.

## 🧠 Tech Stack

- **Python 3.11+**
- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [FAISS](https://github.com/facebookresearch/faiss)
- [dotenv](https://pypi.org/project/python-dotenv/)

## 📁 Project Structure

YT\_QnA\_bot/
├── bot.py              # Main file to run the bot
├── yt\_transcript.py    # Fetches transcript for given YouTube video
├── prompts.py          # Contains the LCEL prompt template
├── .env                # Stores API keys
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

## ⚙️ Setup Instructions

1. **Clone the repo**
   bash
   git clone https://github.com/your-username/YT_QnA_bot.git
   cd YT_QnA_bot

2. **Create and activate virtual environment**

   bash
   python -m venv venv
   venv\Scripts\activate  # for Windows
   

3. **Install dependencies**

   bash
   pip install -r requirements.txt
   

4. **Create `.env` file**

   OPENAI_API_KEY=your_openai_api_key

5. **Run the bot**

bash
   py bot.py

## 📝 Example Prompt

python
question = "Is the topic of nuclear fusion discussed in this video? If yes, then what was discussed?"

## 🛠️ Notes

* Make sure the YouTube video has **English captions** enabled (not auto-generated only).
* Avoid calling `YouTubeTranscriptApi.get_transcript()` directly during import – wrap it in a function (`get_transcript(video_id)`).
* If the transcript is empty, handle it gracefully to prevent runtime errors.

## ✅ TODOs & Ideas

* [ ] Add support for full YouTube URL (extract ID dynamically).
* [ ] Build Streamlit UI for interactive Q\&A.
* [ ] Support multiple languages.
* [ ] Save Q\&A history to a file.

## 💡 Credits

* [LangChain](https://github.com/langchain-ai/langchain)
* [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
* [OpenAI](https://platform.openai.com/)

## 📜 License

This project is for educational purposes. You may adapt and extend it as needed.
