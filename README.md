# YouTube Transcript Summarizer

This application allows users to summarize YouTube video transcripts. Users can provide a YouTube URL or a search query, and the application will fetch the transcript, summarize it using the Gemini API, and display the summary.

## Features

*   Summarize YouTube video transcripts.
*   Search for YouTube videos by query.
*   Direct URL input for summarization.
*   Feedback mechanism for summaries.
*   Modern and clean user interface.

## Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SuccessSoham/YouTube-video-transcript
    cd YouTube-video-transcript
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv env
    ```

3.  **Activate the virtual environment:**

    *   **Windows:**
        ```bash
        .\env\Scripts\activate
        ```

    *   **macOS/Linux:**
        ```bash
        source env/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Get a Gemini API Key:**
    *   Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to obtain your API key.

2.  **Create a `.env` file:**
    *   In the root directory of the project, create a file named `.env`.
    *   Add your Gemini API key to this file:
        ```
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
        Replace `"YOUR_GEMINI_API_KEY"` with your actual API key.

## Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

2.  **Open in browser:**
    *   The application will open in your web browser (usually at `http://localhost:8501`).

3.  **Enter YouTube URL or Search Query:**
    *   In the input field, paste a YouTube video URL or type a search query (e.g., "AI 2027").

4.  **Click "Summarize":**
    *   The application will fetch the transcript, summarize it, and display the summary.

## Troubleshooting

*   **`type object 'YouTubeTranscriptApi' has no attribute 'get_transcript'` or `'FetchedTranscriptSnippet' object is not subscriptable'`:** These errors usually indicate an issue with the `youtube-transcript-api` library. Ensure you have the correct version installed and that your Python environment is refreshed. If the issue persists, try reinstalling the library:
    ```bash
    pip uninstall youtube-transcript-api
    pip install youtube-transcript-api
    ```
    Also, ensure your `agent.py` file matches the latest changes (refer to the repository for the most up-to-date code).
