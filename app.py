import streamlit as st
from PIL import Image
import pytesseract
import requests
import json

# Hàm TTS
def text_to_speech(text):
    # Gửi yêu cầu tới Edge TTS API
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

# Giao diện người dùng Streamlit
st.title("OCR và Text-to-Speech")

# Tải lên hình ảnh
uploaded_file = st.file_uploader("Tải lên hình ảnh", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Hiển thị hình ảnh
    image = Image.open(uploaded_file)
    st.image(image, caption='Hình ảnh đã tải lên', use_column_width=True)

    # Thực hiện OCR
    extracted_text = pytesseract.image_to_string(image)
    st.write("Văn bản được trích xuất từ hình ảnh:")
    st.write(extracted_text)

    # TTS
    if st.button("Phát âm thanh"):
        audio_content = text_to_speech(extracted_text)
        if audio_content:
            # Lưu tệp âm thanh và phát
            with open("output.mp3", "wb") as f:
                f.write(audio_content)
            st.audio("output.mp3", format='audio/mp3')
