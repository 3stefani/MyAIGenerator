import requests
import streamlit as st

api_key = '' # Add API KEY generated on OpenAI

def openai_request(prompt):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers=headers,
        json={
            'prompt': prompt,
            'model': 'dall-e-3',
            'size': '1024x1024',  
            'n': 1
        }
    )
    if response.status_code != 200:
        raise Exception(response.json())
    else:
        image_url = response.json()['data'][0]['url']

    return image_url

def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Page settings
st.set_page_config(page_title="AI Image Generator", page_icon="", layout="centered")

# Creation App Streamlit
st.image("images/full.jpg", use_column_width=True)
st.title("AI Image Generator")

# Adding a sidebar
description = st.text_area("Prompt")

# Añadir un botón
if st.button("Generate Image"):
    with st.spinner("Generating your image..."):
        try:
            url = openai_request(description)
            filename = "AI_images/image_generator.png"
            download_image(url, filename)
            st.image(filename, use_column_width=True)
            with open(filename, "rb") as f:
                image_data = f.read()
            st.download_button(label="Download Image", data=image_data, file_name="image_generated.jpg")
        except Exception as e:
            st.error(f"Error generating image: {e}")