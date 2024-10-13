import streamlit as st
from PIL import Image
import pytesseract
import requests
from streamlit_camera_input import camera_input

# Hàm TTS
def text_to_speech(text):
    api_url = "https://api.edge-tts.com/v1/tts"
    payload = {
        "text": text,
        "voice": "en-US-JennyNeural",
        "outputFormat": "audio-16khz-32kbitrate-mono-mp3"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content  # Trả về nội dung âm thanh
    else:
        st.error("Error with TTS API: " + response.text)
        return None

# Giao diện người dùng
st.title("Chụp ảnh từ webcam và OCR")

# Chụp ảnh từ webcam
img_file = camera_input("Chụp ảnh từ webcam")

if img_file:
    # Hiển thị ảnh chụp
    img = Image.open(img_file)
    st.image(img, caption="Ảnh chụp từ webcam", use_column_width=True)

    # Thực hiện OCR
    extracted_text = pytesseract.image_to_string(img)
    st.write("Văn bản được trích xuất từ ảnh:")
    st.write(extracted_text)

    # TTS - Phát văn bản trích xuất
    if st.button("Phát âm thanh"):
        audio_content = text_to_speech(extracted_text)
        if audio_content:
            # Lưu và phát tệp âm thanh
            with open("output.mp3", "wb") as f:
                f.write(audio_content)
            st.audio("output.mp3", format="audio/mp3")
