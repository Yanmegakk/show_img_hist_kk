import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import matplotlib.pyplot as plt

def enhance_image(image, scale_factor=2):
    width, height = image.size
    new_width = width * scale_factor
    new_height = height * scale_factor
    return image.resize((new_width, new_height), Image.LANCZOS)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def invert_colors(image):
    return ImageOps.invert(image)

def adjust_tone_curve(image, curve):
    img_array = np.array(image)
    for channel in range(3):
        img_array[:, :, channel] = np.interp(img_array[:, :, channel], np.arange(256), curve[channel])
    return Image.fromarray(img_array)

def plot_tone_curve(curve):
    x = np.arange(256)
    plt.figure(figsize=(6, 4))
    plt.plot(x, curve[0], 'r', label='R')
    plt.plot(x, curve[1], 'g', label='G')
    plt.plot(x, curve[2], 'b', label='B')
    plt.title('トーンカーブ')
    plt.xlabel('入力')
    plt.ylabel('出力')
    plt.legend()
    st.pyplot()

def main():
    st.set_page_config(page_title="画像処理アプリ", page_icon="🎨")

    st.title("画像処理アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.sidebar.title("オプション")
        operation = st.sidebar.selectbox("処理を選択", ["高画質化", "コントラスト調整", "色反転化", "トーンカーブ調整"])

        original_image = Image.open(uploaded_image)
        st.subheader("変更前")
        st.image(original_image, caption="変更前", use_column_width=True)

        if operation == "高画質化":
            enhanced_image = enhance_image(original_image)
        elif operation == "コントラスト調整":
            contrast_factor = st.sidebar.slider("コントラスト調整", 0.5, 2.0, 1.0, 0.1)
            enhanced_image = adjust_contrast(original_image, contrast_factor)
        elif operation == "色反転化":
            enhanced_image = invert_colors(original_image)
        else:
            st.sidebar.subheader("トーンカーブ調整")
            r_curve = st.sidebar.slider("R チャンネル", 0.0, 2.0, 1.0, 0.1)
            g_curve = st.sidebar.slider("G チャンネル", 0.0, 2.0, 1.0, 0.1)
            b_curve = st.sidebar.slider("B チャンネル", 0.0, 2.0, 1.0, 0.1)
            curve = [r_curve, g_curve, b_curve]
            enhanced_image = adjust_tone_curve(original_image, curve)
            plot_tone_curve(curve)

        st.subheader("変更後")
        st.image(enhanced_image, caption="変更後", use_column_width=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        ax1.imshow(original_image)
        ax1.set_title("変更前")
        ax1.axis("off")
        ax2.imshow(enhanced_image)
        ax2.set_title("変更後")
        ax2.axis("off")

        st.subheader("変更前後比較")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
