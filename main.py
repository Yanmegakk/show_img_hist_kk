import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import matplotlib.pyplot as plt

# 高画質化
def enhance_image(image, scale_factor=2):
    width, height = image.size
    new_width = width * scale_factor
    new_height = height * scale_factor
    return image.resize((new_width, new_height), Image.LANCZOS)

# コントラスト調整
def adjust_contrast(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# 色反転化
def invert_colors(image):
    return ImageOps.invert(image)

def create_tone_curve(points):
    x = np.arange(256)
    curve = np.interp(x, *zip(*sorted(points.items())))
    return curve.astype(int)

def plot_tone_curve(curve_points):
    r_curve, g_curve, b_curve = curve_points
    x = np.arange(256)
    plt.figure(figsize=(6, 4))
    plt.plot(x, r_curve, 'r', label='R')
    plt.plot(x, g_curve, 'g', label='G')
    plt.plot(x, b_curve, 'b', label='B')
    plt.title('トーンカーブ')
    plt.xlabel('入力')
    plt.ylabel('出力')
    plt.legend()
    return plt

def main():
    st.set_page_config(page_title="画像処理アプリ", page_icon="🎨")

    st.title("画像処理アプリ")

    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.subheader("元の画像")
        st.image(uploaded_image, caption="元の画像", use_column_width=True)

        image = Image.open(uploaded_image)

        st.sidebar.header("画像処理オプション")
        options = {
            "高画質化": enhance_image,
            "コントラスト調整": adjust_contrast,
            "色反転化": invert_colors,
            "トーンカーブ": create_tone_curve,
        }
        selected_option = st.sidebar.selectbox("処理を選択してください", list(options.keys()))

        if selected_option == "トーンカーブ":
            st.sidebar.subheader("トーンカーブ設定")
            r_curve = st.sidebar.slider("Rトーンカーブ", 0, 255, (0, 255))
            g_curve = st.sidebar.slider("Gトーンカーブ", 0, 255, (0, 255))
            b_curve = st.sidebar.slider("Bトーンカーブ", 0, 255, (0, 255))
            curve_points = {
                "r": create_tone_curve({"r": r_curve}),
                "g": create_tone_curve({"g": g_curve}),
                "b": create_tone_curve({"b": b_curve})
            }
            processed_image = options[selected_option](image, curve_points)
            
            st.subheader("トーンカーブの状態")
            st.pyplot(plot_tone_curve([curve_points["r"], curve_points["g"], curve_points["b"]]))
        else:
            processed_image = options[selected_option](image)

        st.subheader("処理後の画像")
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="変更前", use_column_width=True)
        with col2:
            st.image(processed_image, caption="変更後", use_column_width=True)

if __name__ == "__main__":
    main()



