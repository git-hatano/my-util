"""
実行方法
streamlit run image_viewer.py

クリップボードへのコピーはローカル実行の時しかできない仕様です
"""

import streamlit as st
import os
import cv2
import pyperclip
import tempfile
import pandas as pd

def display_images(image_paths, confs=None):
    if not image_paths:
        st.warning("No images found.")
        return

    cols = st.columns(5)  # 5列で画像を表示
    col_index = 0

    for idx, (image_path, conf) in enumerate(zip(image_paths, confs if confs else [None]*len(image_paths))):
        with cols[col_index]:
            try:
                img = cv2.imread(image_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    caption = f"{os.path.basename(image_path)}"
                    if conf is not None:
                        caption += f" | conf: {conf:.2f}"
                    st.image(img, caption=caption, use_column_width=True)
                    if st.button("Copy path", key=f'copy-{idx}'):
                        pyperclip.copy(image_path)
                        st.success(f"Copied to clipboard: {image_path}")
                col_index = (col_index + 1) % 5
            except Exception as e:
                st.error(f"Failed to load or display {image_path}: {e}")

def load_and_display_images(df, sort_order):
    df = df.sort_values('conf', ascending=(sort_order == "Ascending"))
    display_images(df['image_path'].tolist(), df['conf'].tolist())

def main():
    st.set_page_config(layout="wide")
    st.title('Image Viewer')

    method = st.radio("Choose your input method:", ("Upload Files", "Enter Folder Path", "Upload CSV"))
    image_paths = []

    if method == "Upload Files":
        uploaded_files = st.file_uploader("Choose images to upload", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', '.webp'])
        if uploaded_files:
            try:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(tmpdirname, uploaded_file.name)
                        with open(file_path, 'wb') as f:
                            f.write(uploaded_file.read())
                        image_paths.append(file_path)
                    display_images(image_paths)
            except Exception as e:
                st.error(f"An error occurred while processing uploaded files: {e}")
    
    elif method == "Enter Folder Path":
        folder_path = st.text_input("Enter the folder path:")
        if folder_path:
            try:
                image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
                display_images(image_paths)
            except Exception as e:
                st.error(f"An error occurred while processing the folder: {e}")
    
    elif method == "Upload CSV":
        csv_file = st.file_uploader("Upload a CSV file", type=['csv'])
        if csv_file:
            try:
                df = pd.read_csv(csv_file)
                if 'image_path' in df.columns and 'conf' in df.columns:
                    df['exists'] = df['image_path'].apply(lambda x: os.path.exists(x))
                    df = df[df['exists']]
                    if df.empty:
                        st.warning("No valid image paths found.")
                    else:
                        sort_order = st.radio("Sort order:", ("Ascending", "Descending"))
                        load_and_display_images(df, sort_order)
                else:
                    st.error("CSV must contain 'image_path' and 'conf' columns.")
            except Exception as e:
                st.error(f"An error occurred while processing the CSV file: {e}")

if __name__ == "__main__":
    main()
