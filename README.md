# YouDigest
*YouTube Transcription and Summarization*

This repository contains a Python script and Streamlit web app that allows users to download YouTube videos, transcribe their audio using OpenAI's Whisper ASR model, and optionally summarize the transcription using the text-davinci-003 model.

## Requirements

- Python 3.6 or later
- OpenAI API Key

## Installation

1. Clone this repository:

```bash
git clone https://github.com/JordieB/youtube-transcription.git
cd youtube-transcription
```

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your_openai_api_key"
```

## Usage

### As a Streamlit web app

```bash
streamlit run app.py
```
1. Open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501).
2. Enter a YouTube video URL, and the app will display the transcription and provide an option to summarize it.

### As a standalone Python script
1. Edit the app.py file and only allow `main_cli()` run in the final lines.
2. Run the script
```bash
python app.py
```
Follow the prompts in the terminal to enter a YouTube video URL and optionally summarize the transcription.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
