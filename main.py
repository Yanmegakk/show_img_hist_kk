import streamlit as st
from PIL import Image, ImageEnhance, ImageOps

def enhance_image(image, option, parameter=1.0):
    if option == "高画質化":
        return image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    elif option == "コントラスト調整":
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(parameter)
    elif option == "色反転化":
        return ImageOps.invert(image)

def main():
    st.title("画像処理アプリ")
    st.write("アップロードされた画像に対して、処理を選択してください。")

    uploaded_image = st.file_uploader("画像を選択してください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.subheader("アップロードされた画像")
        st.image(image, caption="アップロードされた画像", use_column_width=True)

        option = st.selectbox("処理を選択してください", ["選択してください", "高画質化", "コントラスト調整", "色反転化"])

        if option != "選択してください":
            if option == "コントラスト調整":
                contrast_level = st.slider("コントラストの強度", 0.0, 2.0, 1.0, 0.1)
                processed_image = enhance_image(image, option, contrast_level)
            else:
                processed_image = enhance_image(image, option)

            st.subheader("処理後の画像")
            st.image(processed_image, caption="処理後の画像", use_column_width=True)

if __name__ == "__main__":
    main()

