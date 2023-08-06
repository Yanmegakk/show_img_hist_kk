import streamlit as st
from PIL import Image, ImageEnhance
from colorthief import ColorThief
import matplotlib.pyplot as plt
import numpy as np

def enhance_image(image, scale_factor=2):
    width, height = image.size
    new_width = width * scale_factor
    new_height = height * scale_factor
    return image.resize((new_width, new_height), Image.LANCZOS)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def invert_colors(image):
    return Image.eval(image, lambda px: 255 - px)

def adjust_hsv(image, h_factor, s_factor, v_factor):
    h, s, v = image.convert("HSV").split()
    h = h.point(lambda p: p * h_factor)
    s = s.point(lambda p: p * s_factor)
    v = v.point(lambda p: p * v_factor)
    return Image.merge("HSV", (h, s, v)).convert("RGB")

def plot_color_palette(palette):
    plt.figure(figsize=(2, 2))
    plt.imshow([np.array(palette)], aspect='auto')
    plt.axis('off')
    st.pyplot()

def main():
    st.title("画像エディタ")

    uploaded_image = st.file_uploader("画像を選択してください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.subheader("元画像")
        st.image(uploaded_image, caption="元画像", use_column_width=True)

        image = Image.open(uploaded_image)

        st.sidebar.header("エフェクトを選択")
        effects = ["高画質化", "コントラスト調整", "色反転化", "HSVパラメータの調節"]
        selected_effects = st.sidebar.multiselect("適用するエフェクトを選択", effects)

        enhanced_image = image.copy()
        for effect in selected_effects:
            if effect == "高画質化":
                enhanced_image = enhance_image(enhanced_image)
            elif effect == "コントラスト調整":
                contrast_factor = st.sidebar.slider("コントラスト調整", 0.1, 3.0, 1.0)
                enhanced_image = adjust_contrast(enhanced_image, contrast_factor)
            elif effect == "色反転化":
                enhanced_image = invert_colors(enhanced_image)
            elif effect == "HSVパラメータの調節":
                h_factor = st.sidebar.slider("Hue", 0.0, 2.0, 1.0)
                s_factor = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
                v_factor = st.sidebar.slider("Value", 0.0, 2.0, 1.0)
                enhanced_image = adjust_hsv(enhanced_image, h_factor, s_factor, v_factor)

        st.subheader("変更後の画像")
        st.image(enhanced_image, caption="変更後の画像", use_column_width=True)

        st.sidebar.header("カラーパレット")
        color_thief = ColorThief(enhanced_image)
        palette = color_thief.get_palette(color_count=5)
        plot_color_palette(palette)

if __name__ == "__main__":
    main()
