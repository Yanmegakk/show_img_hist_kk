import streamlit as st
import torch
from PIL import Image, ImageEnhance, ImageOps
from torchvision.transforms import functional as F
from PIL import Image
import numpy as np

# Load the RealESRGAN model
model_path = 'realesrgan-x4minus.pth'  # Replace with your actual path
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_path, map_location=device)["model"].to(device).eval()

# Function to enhance image using RealESRGAN
def enhance_with_realesrgan(image, scale=4):
    with torch.no_grad():
        lr_img = F.to_tensor(image).unsqueeze(0).to(device)
        sr_img = model(lr_img).squeeze(0)
        sr_img = F.to_pil_image(sr_img.cpu())
    return sr_img

# Function to apply contrast adjustment
def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# Function to apply color inversion
def invert_colors(image):
    return Image.fromarray(np.array(image)[:, :, ::-1])

def main():
    st.set_page_config(page_title="画像処理アプリ", page_icon="📷", layout="wide")
    st.title("画像処理アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.subheader("元の画像")
        st.image(image, caption="元の画像", use_column_width=True)

        operation = st.selectbox("処理を選択してください", ["高画質化", "コントラスト調整", "色反転化"])
        
        if operation == "高画質化":
            enhanced_image = enhance_with_realesrgan(image)
        elif operation == "コントラスト調整":
            contrast_factor = st.slider("コントラスト調整", 0.1, 3.0, 1.0, 0.1)
            enhanced_image = adjust_contrast(image, contrast_factor)
        else:
            enhanced_image = invert_colors(image)

        st.subheader("処理後の画像")
        st.image(enhanced_image, caption="処理後の画像", use_column_width=True)

        st.subheader("比較")
        col1, col2 = st.beta_columns(2)
        col1.image(image, caption="元の画像", use_column_width=True)
        col2.image(enhanced_image, caption="処理後の画像", use_column_width=True)

if __name__ == "__main__":
    main()
