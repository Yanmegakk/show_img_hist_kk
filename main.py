import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import torchvision.transforms as transforms
import torch
import requests

# ページのタイトルやアイコンを設定
st.set_page_config(page_title="Cool Image Editor", page_icon=":art:", layout="wide")

# ESRGANのモデルをダウンロード
model_url = "https://github.com/xinntao/ESRGAN/releases/download/v0.4.1/ESRGAN_x4.pth"
model_path = "ESRGAN_x4.pth"
if not st.session_state.model_downloaded:
    st.session_state.model_downloaded = True
    response = requests.get(model_url)
    with open(model_path, "wb") as f:
        f.write(response.content)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_path, map_location=device).to(device)
model.eval()

def enhance_image_esrgan(image, scale_factor=4):
    transform = transforms.Compose([
        transforms.Resize((image.size[1] * scale_factor, image.size[0] * scale_factor)),
        transforms.ToTensor()
    ])
    image_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        enhanced_tensor = model(image_tensor).clamp(0.0, 1.0)
    enhanced_image = transforms.ToPILImage()(enhanced_tensor.cpu().squeeze())
    return enhanced_image

def adjust_contrast(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def invert_colors(image):
    return ImageOps.invert(image)

def main():
    st.title("Cool Image Editor")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)

        st.subheader("変換前と変換後")

        col1, col2 = st.beta_columns(2)

        with col1:
            st.image(image, caption="変換前", use_column_width=True)

        with col2:
            st.sidebar.subheader("エフェクトを選択")
            selected_effects = st.sidebar.multiselect("エフェクトを選んでください", ["高画質化", "コントラスト調整", "色反転"])

            if "高画質化" in selected_effects:
                enhanced_image = enhance_image_esrgan(image)
                st.image(enhanced_image, caption="高画質化", use_column_width=True)

            if "コントラスト調整" in selected_effects:
                contrast_factor = st.sidebar.slider("コントラストの強度を調整", 0.5, 5.0, 1.5)
                contrast_adjusted_image = adjust_contrast(image, contrast_factor)
                st.image(contrast_adjusted_image, caption="コントラスト調整", use_column_width=True)

            if "色反転" in selected_effects:
                inverted_image = invert_colors(image)
                st.image(inverted_image, caption="色反転", use_column_width=True)

if __name__ == "__main__":
    main()