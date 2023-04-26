import os
import time
import tempfile
from typing import Tuple

import openai
import streamlit as st
from pytube import YouTube

# Set your OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']


def download_youtube_video(url: str, resolution: str = 'lowest') -> str:
    """
    Download a YouTube video in MP4 format.

    :param url: The YouTube video URL.
    :param resolution: The desired video resolution (default is 'lowest').
    :return: The local file path of the downloaded video.
    """
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4', res=resolution).first()
    output_path = os.path.join(tempfile.gettempdir(), f"{yt.title}.mp4")
    stream.download(output_path=output_path)
    return output_path


def transcribe_video(video_path: str) -> str:
    """
    Transcribe a video using OpenAI's Whisper ASR model.

    :param video_path: The local file path of the video.
    :return: The transcription text.
    """
    # Upload the video file to OpenAI's servers
    with open(video_path, "rb") as f:
        file = openai.File.create(file=f.read(), purpose="transcription")

    # Start a transcription job using the Whisper ASR model
    job = openai.Job.create(file_id=file.id, model="whisper-v1", priority="high")

    # Poll the job status until it's complete
    while True:
        job = openai.Job.get(job.id)
        if job.status == "succeeded":
            break
        elif job.status == "failed":
            raise Exception("Transcription job failed")
        time.sleep(1)

    # Fetch the transcription results
    transcript = job.get_results()

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
        st.write(transcription)

        summarize = st.checkbox("Do you want to summarize the transcription?")

        if summarize:
            summary_length = st.slider("Enter the desired summary length (in words):", 10, 500, 100)

            st.write("Summarizing the transcription...")
            summary = summarize_text(transcription, length=summary_length * 4)

            st.write("Summary:")
            st.write(summary)


if __name__ == "__main__":
    main()
