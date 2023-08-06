import streamlit as st
from PIL import Image, ImageEnhance, ImageOps

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

def main():
    st.set_page_config(page_title="画像処理アプリ", page_icon="🎨")

    st.title("画像処理アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.subheader("変更前")

        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="変更前", use_column_width=True)

        st.sidebar.title("オプション")
        operation = st.sidebar.selectbox("処理を選択", ["高画質化", "コントラスト調整", "色反転化"])

        if operation == "高画質化":
            enhanced_image = enhance_image(original_image)
        elif operation == "コントラスト調整":
            contrast_factor = st.sidebar.slider("コントラスト調整", 0.5, 2.0, 1.0, 0.1)
            enhanced_image = adjust_contrast(original_image, contrast_factor)
        else:
            enhanced_image = invert_colors(original_image)

        st.subheader("変更後")

        st.image(enhanced_image, caption="変更後", use_column_width=True)

if __name__ == "__main__":
    main()
