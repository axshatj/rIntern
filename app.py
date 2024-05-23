import streamlit as st
import os
import base64
import requests
from main import MySearchEngine
from dotenv import load_dotenv

load_dotenv()
openai_key = os.environ.get("OPENAI_API_KEY")
allowed_types = ["jpg", "png", "jpeg"]

def process_images(uploaded_files):
    base64_images = [base64.b64encode(file.read()).decode('utf-8') for file in uploaded_files]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}"
    }
    responses = []
    for base64_image in base64_images:
        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What’s in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        responses.append(response.json())
    return responses

st.title("Multimodal Medical Helper")

uploaded_files = st.file_uploader("Upload images", type=allowed_types, accept_multiple_files=True)
input_box = st.text_input("Your Message:")
send_button = st.button("Send")
output_box = st.empty()

if send_button:
    if uploaded_files and not input_box:  # Only images
        responses = process_images(uploaded_files)
        texts_from_images = [response['choices'][0]['message']['content'] for response in responses]
        combined_text = " ".join(texts_from_images)
        answer = MySearchEngine().search(combined_text)
        output_box.write(answer['response'])

    elif not uploaded_files and input_box:  # Only text
        answer = MySearchEngine().search(input_box)
        output_box.write(answer['response'])

    elif uploaded_files and input_box:  # Both images and text
        responses = process_images(uploaded_files)
        texts_from_images = [response['choices'][0]['message']['content'] for response in responses]
        combined_text = " ".join(texts_from_images) + " " + input_box
        answer = MySearchEngine().search(combined_text)
        output_box.write(answer['response'])
