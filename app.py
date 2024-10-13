import streamlit as st
from PIL import Image
import pytesseract
import requests
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

# Tạo một lớp để xử lý video
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.image = None

    def transform(self, frame):
        img = frame.to_image()
        self.image = img
        return av.VideoFrame.from_image(img)

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

# Tạo một đối tượng video từ webcam
ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
transformer = ctx.video_transformer

# Thực hiện OCR khi nhấn nút
if transformer and st.button("Chụp và xử lý ảnh"):
    if transformer.image is not None:
        # Hiển thị ảnh chụp
        st.image(transformer.image, caption='Ảnh chụp từ webcam', use_column_width=True)

        # Lưu ảnh tạm thời để xử lý OCR
        transformer.image.save("temp_image.png")

        # Thực hiện OCR
        extracted_text = pytesseract.image_to_string(transformer.image)
        st.write("Văn bản được trích xuất từ ảnh:")
        st.write(extracted_text)

        # TTS - Phát văn bản trích xuất
        if st.button("Phát âm thanh"):
            audio_content = text_to_speech(extracted_text)
            if audio_content:
                # Lưu và phát tệp âm thanh
                with open("output.mp3", "wb") as f:
                    f.write(audio_content)
                st.audio("output.mp3", format='audio/mp3')
    else:
        st.warning("Không có hình ảnh nào được chụp.")

