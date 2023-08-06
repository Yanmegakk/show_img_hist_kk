import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops
from colorthief import ColorThief

# 日本語UI設定
st.set_page_config(page_title="画像編集アプリ", page_icon=":camera:", layout="wide")

def enhance_image(image, scale_factor=2):
    width, height = image.size
    new_width = width * scale_factor
    new_height = height * scale_factor
    return image.resize((new_width, new_height), Image.LANCZOS)

def adjust_contrast(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def invert_colors(image):
    return ImageChops.invert(image)

def adjust_hsv(image, hue_factor=1.0, saturation_factor=1.0, value_factor=1.0):
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()
    h = np.array(h)
    s = np.array(s)
    v = np.array(v)
    h = (h * hue_factor) % 256
    s = np.clip(s * saturation_factor, 0, 255)
    v = np.clip(v * value_factor, 0, 255)
    h = Image.fromarray(h.astype("uint8"), "L")
    s = Image.fromarray(s.astype("uint8"), "L")
    v = Image.fromarray(v.astype("uint8"), "L")
    return Image.merge("HSV", (h, s, v)).convert("RGB")

def main():
    st.title("画像編集アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.sidebar.title("編集オプション")
        # ... 他の編集オプション ...

        original_image = Image.open(uploaded_image)

        # 元画像と変更後の画像を横並びで表示
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="元画像", use_column_width=True)

        edited_image = original_image.copy()

        # 画像編集処理

        with col2:
            st.image(edited_image, caption="編集後の画像", use_column_width=True)

            # 変更後の画像からカラーパレットを生成
            color_thief = ColorThief(edited_image)
            dominant_color = color_thief.get_color(quality=1)
            palette = color_thief.get_palette(color_count=5)

            # カラーパレットを表示
            st.subheader("カラーパレット")
            palette_html = ""
            for color in palette:
                palette_html += f'<div style="width: 30px; height: 30px; background-color: rgb({color[0]}, {color[1]}, {color[2]})"></div>'
            st.markdown(palette_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

