import whisper
import os
import re
import json

# Function to format transcription text by placing each sentence on a new line
def format_transcription(text):
    sentences = re.split(r'([.!?])\s*', text)  # Splitting at ., !, ?
    formatted_text = ""
    for i in range(0, len(sentences) - 1, 2):
        formatted_text += sentences[i] + sentences[i + 1] + "\n"
    return formatted_text.strip()

# Function to transcribe all audio/video files in a folder recursively
def transcribe_folder(input_folder, output_folder):
    # Load the Whisper model
    model = whisper.load_model("tiny")  # Using the smallest available model

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List of supported audio and video formats
    supported_formats = (".mp3", ".wav", ".mp4", ".m4a", ".ogg", ".flac")

    # Recursively scan the folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                print(f"Transcribing: {file_path}")

                # Transcribe the audio/video file
                result = model.transcribe(file_path)
                formatted_text = format_transcription(result["text"])

                # Create a structured output file name
                file_name = os.path.splitext(file)[0]  # Remove extension
                txt_output_path = os.path.join(output_folder, f"{file_name}.txt")
                json_output_path = os.path.join(output_folder, f"{file_name}.json")

                # Save transcription as a TXT file
                with open(txt_output_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(formatted_text)

                # Save transcription as a JSON file
                with open(json_output_path, "w", encoding="utf-8") as json_file:
                    json.dump({"file": file, "transcription": formatted_text}, json_file, indent=4)

                print(f"Saved transcription to:\n  {txt_output_path}\n  {json_output_path}")

# Define input folder (where media files are located) and output folder (where transcriptions will be saved)
input_folder = r"C:\Users\PRACHI\audio to speech"
output_folder = r"C:\Users\PRACHI\audio to speech\Transcriptions"

# Run the transcription process
transcribe_folder(input_folder, output_folder)

print("✅ Transcription completed for all media files!")
