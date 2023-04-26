import os
import re
import time
import tempfile
from typing import Tuple

import openai
import streamlit as st
from pytube import YouTube

# Set your OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']


def download_youtube_video(url: str) -> str:
    """
    Download a YouTube video in MP4 format.

    :param url: The YouTube video URL.
    :return: The local file path of the downloaded video.
    """
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').get_lowest_resolution()
    
    # Sanitize the video title by replacing non-alphanumeric characters, spaces, or hyphens with underscores
    sanitized_title = re.sub(r"[^\w\-]", "_", yt.title)
    # Limit the sanitized title length to avoid issues with long file names and lowercase
    sanitized_title = sanitized_title[:25].lower()
    
    # Download the video
    output_path = stream.download(output_path=tempfile.gettempdir())
    
    return output_path


def transcribe_video(video_path: str) -> str:
    """
    Transcribe a video using OpenAI's whisper-1 model.

    :param video_path: The local file path of the video.
    :return: The transcription text.
    """
    # Transcribe the video using the whisper-1 model
    with open(video_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    return transcript.text


def summarize_text(text: str, length: int = 100) -> str:
    """
    Summarize a given text using OpenAI's text-davinci-003 model.

    :param text: The input text to be summarized.
    :param length: The desired length of the summary in words (default is 100).
    :return: The summary text.
    """
    prompt = f"Please summarize the following text in about {length} words: {text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=length,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()

    return summary


def main():
    st.title("YouTube Video Transcription and Summarization")

    youtube_url = st.text_input("Enter the YouTube video URL:")

    if youtube_url:
        video_path = download_youtube_video(youtube_url)

        st.write("Transcribing the video...")
        transcription = transcribe_video(video_path)

        st.write("Transcription:")
        # Used code blocks to avoid unexpected markdown interactions
        st.code(transcription)

        summarize = st.checkbox("Do you want to summarize the transcription?")

        if summarize:
            summary_length = st.slider("Enter the desired summary length (in words):", 10, 500, 100)

            st.write("Summarizing the transcription...")
            summary = summarize_text(transcription, length=summary_length * 4)

            st.write("Summary:")
            st.write(summary)

def main_cli():
    """
    The main function for the command-line interface (CLI) version of the application.
    """
    youtube_url = input("Enter the YouTube video URL: ")
    video_path = download_youtube_video(youtube_url)
    transcription = transcribe_video(video_path)

    summarize = input("Do you want to summarize the transcription? (yes/no): ").lower()

    if summarize == 'yes':
        summary_length = int(input("Enter the desired summary length (in words): "))
        summary = summarize_text(transcription, length=summary_length)
        print("\nSummary:\n", summary)
    else:
        print("\nTranscription:\n", transcription)


if __name__ == "__main__":
    try:
        import streamlit
        main()
    except ImportError:
        main_cli()