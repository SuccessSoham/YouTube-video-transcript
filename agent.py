import os
import time
from pytube import YouTube
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable

load_dotenv()

def run_agent(query):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY is not set. Please create a .env file and add your API key.", []
    genai.configure(api_key=api_key)

    reasoning = []

    # Step 1: Search for the video if a query is provided
    reasoning.append("Step 1: Search for the video")
    if "youtube.com" in query:
        video_url = query
        reasoning.append(f"Tool Call: Using direct URL: {video_url}")
    else:
        reasoning.append(f"Tool Call: Searching for '{query}' on DuckDuckGo")
        with DDGS() as ddgs:
            results = list(ddgs.videos(query, max_results=1))
            if not results:
                return "Sorry, I couldn't find any relevant videos.", reasoning
            video_url = results[0]['content']
            reasoning.append(f"Tool Call Result: Found video: {video_url}")

    # Step 2: Get the transcript
    reasoning.append("Step 2: Get the transcript")
    reasoning.append(f"Tool Call: Using pytube and youtube_transcript_api for transcript from {video_url}")
    try:
        # Extract video ID from URL
        video_id = YouTube(video_url).video_id
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        
        # Format transcript into a single string
        transcript_text = " ".join([t.text for t in transcript_list])
        
        # Create a Document object (similar to what YoutubeLoader would return)
        result = [Document(page_content=transcript_text, metadata={"source": video_url})]

    except NoTranscriptFound:
        return "Error: No transcript found for this video.", reasoning
    except VideoUnavailable:
        return "Error: Video is unavailable or private.", reasoning
    except Exception as e:
        return f"An unexpected error occurred during transcript loading: {e}", reasoning
    reasoning.append("Tool Call Result: Transcript loaded")

    # Step 3: Split the transcript into chunks
    reasoning.append("Step 3: Split the transcript into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
    texts = text_splitter.split_documents(result)
    reasoning.append(f"Tool Call Result: Transcript split into {len(texts)} chunks")

    # Step 4: Summarize the transcript using Gemini API
    reasoning.append("Step 4: Summarize the transcript using Gemini API")
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Map step
    reasoning.append("Map Step: Summarizing each chunk")
    summaries = []
    for i, text in enumerate(texts):
        reasoning.append(f"Tool Call: Gemini API to summarize chunk {i+1}/{len(texts)}")
        try:
            response = model.generate_content(f"Summarize this text: {text.page_content}")
            summaries.append(response.text)
        except Exception as e:
            return f"An error occurred during Gemini API call in the map step: {e}", reasoning
        time.sleep(1) # To avoid hitting the rate limit

    # Reduce step
    reasoning.append("Reduce Step: Combining summaries")
    combined_summary = " ".join(summaries)
    reasoning.append("Tool Call: Gemini API to create a final summary")
    try:
        final_summary = model.generate_content(f"Create a cohesive summary from the following summaries: {combined_summary}")
    except Exception as e:
        return f"An error occurred during Gemini API call in the reduce step: {e}", reasoning

    return final_summary.text, reasoning