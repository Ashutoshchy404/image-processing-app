import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def apply_sharpening(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def apply_smoothing(image):
    return cv2.GaussianBlur(image, (15, 15), 0)

def apply_contrast(image, factor):
    pil_image = Image.fromarray(image)
    enhancer = ImageEnhance.Contrast(pil_image)
    return np.array(enhancer.enhance(factor))

def apply_black_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def main():
    st.title("Image Processing App")
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)
        
        st.image(image, caption="Original Image", use_column_width=True)
        
        apply_sharp = st.checkbox("Apply Sharpening")
        apply_smooth = st.checkbox("Apply Smoothing")
        apply_contrast_adj = st.checkbox("Apply Contrast")
        apply_bw = st.checkbox("Convert to Black & White")
        
        processed_image = image.copy()
        
        if apply_sharp:
            processed_image = apply_sharpening(processed_image)
        if apply_smooth:
            processed_image = apply_smoothing(processed_image)
        if apply_contrast_adj:
            contrast_factor = st.slider("Select Contrast Level", 0.5, 3.0, 1.5)
            processed_image = apply_contrast(processed_image, contrast_factor)
        if apply_bw:
            processed_image = apply_black_white(processed_image)
            
        if apply_sharp or apply_smooth or apply_contrast_adj or apply_bw:
            st.image(processed_image, caption="Processed Image", use_column_width=True)

if __name__ == "__main__":
    main()
