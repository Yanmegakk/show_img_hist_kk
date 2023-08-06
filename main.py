import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import numpy as np

# 画像を高画質化
def enhance_image(image, scale_factor=2):
    width, height = image.size
    new_width = width * scale_factor
    new_height = height * scale_factor
    return image.resize((new_width, new_height), Image.LANCZOS)

# コントラストを調整
def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# 色反転
def invert_colors(image):
    return ImageOps.invert(image)

# トーンカーブの調整
def adjust_tone_curve(image, control_points):
    curve = ImageEnhance.Color(image).enhance(0).point(control_points)
    return Image.blend(image, curve, alpha=0.5)

def main():
    st.set_page_config(page_title="画像処理アプリVer.kk", page_icon="🎨", layout="wide")
    st.markdown(
        """
        <style>
        .css-1aumxhk {
            background-color: #006400 !important;
        }
        .css-1aumxhk:hover {
            background-color: #004c00 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("画像処理アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.sidebar.title("オプション")
        operation = st.sidebar.selectbox("処理を選択", ["高画質化", "コントラスト調整", "色反転化", "トーンカーブ調整"])

        st.sidebar.markdown(
            """
            <style>
            .css-1p7hx3i {
                background-color: #006400 !important;
            }
            .css-1p7hx3i:hover {
                background-color: #004c00 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        control_points = {
            0: 0,
            128: 128,
            255: 255,
        }

        if operation == "高画質化":
            enhanced_image = enhance_image(Image.open(uploaded_image))
        elif operation == "コントラスト調整":
            contrast_factor = st.sidebar.slider("コントラスト調整", 0.5, 2.0, 1.0, 0.1)
            enhanced_image = adjust_contrast(Image.open(uploaded_image), contrast_factor)
        elif operation == "色反転化":
            enhanced_image = invert_colors(Image.open(uploaded_image))
        else:
            control_points[128] = st.sidebar.slider("中間トーン (128)", 0, 255, 128)
            enhanced_image = adjust_tone_curve(Image.open(uploaded_image), control_points)

        col1, col2 = st.beta_columns(2)
        col1.subheader("変更前")
        col1.image(Image.open(uploaded_image), caption="変更前", use_column_width=True)

        col2.subheader("変更後")
        col2.image(enhanced_image, caption="変更後", use_column_width=True)

if __name__ == "__main__":
    main()
