import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import cv2

# 高画質化
def enhance_image(image):
    return image.resize((image.width * 2, image.height * 2), Image.LANCZOS)

# コントラスト調整
def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# 色反転化
def invert_colors(image):
    return ImageOps.invert(image)

# HSVパラメータの調節
def adjust_hsv(image, h_factor, s_factor, v_factor):
    hsv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
    hsv_image[:, :, 0] = np.clip(hsv_image[:, :, 0] * h_factor, 0, 255)
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * s_factor, 0, 255)
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * v_factor, 0, 255)
    return Image.fromarray(cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB))

def main():
    st.set_page_config(page_title="画像処理アプリVer.kk", page_icon="🖼️")
    st.title("画像処理アプリVer.kk")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)

        st.sidebar.header("エフェクト選択")
        effect = st.sidebar.radio("エフェクトを選んでください", ("高画質化", "コントラスト調整", "色反転化", "HSVパラメータ調整"))

        st.subheader("元画像")
        st.image(image, caption="元画像", use_column_width=True)

        st.subheader("変更後の画像")
        if effect == "高画質化":
            new_image = enhance_image(image)
        elif effect == "コントラスト調整":
            contrast_factor = st.sidebar.slider("コントラスト調整", 0.5, 2.0, 1.0)
            new_image = adjust_contrast(image, contrast_factor)
        elif effect == "色反転化":
            new_image = invert_colors(image)
        else:
            h_factor = st.sidebar.slider("Hue", 0.0, 2.0, 1.0)
            s_factor = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
            v_factor = st.sidebar.slider("Value", 0.0, 2.0, 1.0)
            new_image = adjust_hsv(image, h_factor, s_factor, v_factor)

        st.image([image, new_image], caption=["元画像", "変更後の画像"], use_column_width=True)

if __name__ == "__main__":
    main()
