import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops
import colorsys

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

def create_color_palette(image):
    colors = []
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            hsv = colorsys.rgb_to_hsv(pixel_color[0] / 255, pixel_color[1] / 255, pixel_color[2] / 255)
            colors.append(hsv)
    return colors

def main():
    st.title("画像編集アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.sidebar.title("編集オプション")
        enhance = st.sidebar.checkbox("高画質化")
        contrast = st.sidebar.slider("コントラスト調整", 0.5, 2.0, 1.0, step=0.1)
        invert = st.sidebar.checkbox("色反転化")
        hue = st.sidebar.slider("Hue", 0.0, 2.0, 1.0, step=0.01)
        saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0, step=0.01)
        value = st.sidebar.slider("Value", 0.0, 2.0, 1.0, step=0.01)
        reset = st.sidebar.button("リセット")

        original_image = Image.open(uploaded_image)

        st.image(original_image, caption="元画像", use_column_width=True)

        edited_image = original_image.copy()

        if enhance:
            edited_image = enhance_image(edited_image)

        if contrast != 1.0:
            edited_image = adjust_contrast(edited_image, contrast)

        if invert:
            edited_image = invert_colors(edited_image)

        if hue != 1.0 or saturation != 1.0 or value != 1.0:
            edited_image = adjust_hsv(edited_image, hue, saturation, value)

        st.image(edited_image, caption="編集後の画像", use_column_width=True)

        if reset:
            edited_image = original_image.copy()

        st.sidebar.subheader("カラーパレット")
        colors = create_color_palette(edited_image)
        palette_img = Image.new("RGB", (len(colors), 50))
        for i, hsv in enumerate(colors):
            rgb_color = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
            palette_img.putpixel((i, 25), tuple(int(c * 255) for c in rgb_color))
        st.sidebar.image(palette_img, caption="Color Palette", use_column_width=True)

if __name__ == "__main__":
    main()
