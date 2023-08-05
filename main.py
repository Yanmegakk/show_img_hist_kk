import streamlit as st
from PIL import Image

def enhance_image(image, scale_factor=2):
    width, height = image.size
    new_width = width * scale_factor
    new_height = height * scale_factor
    return image.resize((new_width, new_height), Image.LANCZOS)

def main():
    st.title("Image Enhancer")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        image = Image.open(uploaded_image)
        enhanced_image = enhance_image(image)

        st.subheader("Enhanced Image")
        st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)

if __name__ == "__main__":
    main()
