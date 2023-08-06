import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def enhance_image(image, scale_factor):
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return image.resize((new_width, new_height), Image.LANCZOS)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def invert_colors(image):
    return ImageOps.invert(image)

def adjust_hsv(image, hue, saturation, value):
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()
    h = h.point(lambda p: p + hue)
    s = s.point(lambda p: p * saturation)
    v = v.point(lambda p: p * value)
    return Image.merge("HSV", (h, s, v)).convert("RGB")

def main():
    st.set_page_config(page_title="画像処理アプリVer.kk", page_icon="🖼️")
    st.title("画像処理アプリVer.kk")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.subheader("元の画像")
        st.image(uploaded_image, caption="元の画像", use_column_width=True)

        image = Image.open(uploaded_image)

        # 高画質化
        enhance_factor = st.slider("高画質化", 1.0, 4.0, 2.0, 0.1)
        enhanced_image = enhance_image(image, enhance_factor)

        # コントラスト調整
        contrast_factor = st.slider("コントラスト調整", 0.5, 2.0, 1.0, 0.1)
        contrast_adjusted = adjust_contrast(image, contrast_factor)

        # 色反転化
        inverted_image = invert_colors(image)

        # HSVパラメータ調節
        hue = st.slider("色相調整", -255, 255, 0, 1)
        saturation = st.slider("彩度調整", 0.0, 2.0, 1.0, 0.1)
        value = st.slider("明度調整", 0.0, 2.0, 1.0, 0.1)
        hsv_adjusted = adjust_hsv(image, hue, saturation, value)

        st.subheader("変換後の画像")
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(enhanced_image, caption="高画質化", use_column_width=True)
            st.image(contrast_adjusted, caption="コントラスト調整", use_column_width=True)
        
        with col2:
            st.image(inverted_image, caption="色反転化", use_column_width=True)
            st.image(hsv_adjusted, caption="HSVパラメータ調節", use_column_width=True)

if __name__ == "__main__":
    main()
