import streamlit as st
import pytesseract
from PIL import Image
import requests
import base64
from io import BytesIO

# JavaScript to access webcam and capture image
webcam_js = """
    <script>
    function captureImage() {
        const video = document.querySelector('video');
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const image_data_url = canvas.toDataURL('image/jpeg');
        document.getElementById('image_data').value = image_data_url;
        document.forms[0].submit();
    }
    </script>
    <style>
    video { width: 100%; height: auto; }
    </style>
    <video autoplay></video>
    <button onClick="captureImage()">Capture</button>
    <form>
        <input type="hidden" id="image_data" name="image_data">
    </form>
"""

# Display the webcam JavaScript in Streamlit
st.write(webcam_js, unsafe_allow_html=True)

# Nhận dữ liệu ảnh sau khi chụp
image_data_url = st.experimental_get_query_params().get('image_data')

if image_data_url:
    # Decode base64 image
    image_data = image_data_url[0].split(",")[1]
    image_bytes = base64.b64decode(image_data)
    img = Image.open(BytesIO(image_bytes))

    # Hiển thị ảnh
    st.image(img, caption="Ảnh chụp từ webcam", use_column_width=True)

    # OCR: Trích xuất văn bản từ ảnh
    extracted_text = pytesseract.image_to_string(img)
    st.write("Văn bản được trích xuất từ ảnh:")
    st.write(extracted_text)

    # TTS - Phát văn bản trích xuất
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
            st.error("Lỗi TTS API: " + response.text)
            return None

    if st.button("Phát âm thanh"):
        audio_content = text_to_speech(extracted_text)
        if audio_content:
            st.audio(audio_content, format="audio/mp3")
