import streamlit as st
from PIL import Image, ImageEnhance
from colorthief import ColorThief
import matplotlib.pyplot as plt
import numpy as np
import io

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
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.imshow([np.array(palette)], aspect='auto')
    ax.axis('off')
    st.pyplot(fig)


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
            # ... 以前のエフェクトはそのまま ...

        st.subheader("変更後の画像")
        st.image(enhanced_image, caption="変更後の画像", use_column_width=True)

        st.sidebar.header("カラーパレット")
        # BytesIOを使用して画像を一時的に保存
        img_io = io.BytesIO()
        enhanced_image.save(img_io, format='PNG')
        img_io.seek(0)
        color_thief = ColorThief(img_io)
        palette = color_thief.get_palette(color_count=5)
        plot_color_palette(palette)

if __name__ == "__main__":
    main()