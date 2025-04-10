import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import random
from sketch import convert_to_sketch  # Import the sketch function

# ---------- Image Processing Functions ----------
def apply_sharpening(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def apply_smoothing(image):
    return cv2.GaussianBlur(image, (15, 15), 0)

def apply_contrast(image, factor):
    pil_image = Image.fromarray(image)
    enhancer = ImageEnhance.Contrast(pil_image)
    return np.array(enhancer.enhance(factor))

def apply_brightness(image, factor):
    pil_image = Image.fromarray(image)
    enhancer = ImageEnhance.Brightness(pil_image)
    return np.array(enhancer.enhance(factor))

def apply_black_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def random_filter(image):
    filters = [
        apply_sharpening,
        apply_smoothing,
        lambda img: apply_contrast(img, random.uniform(0.5, 2.5)),
        apply_black_white,
        lambda img: apply_brightness(img, random.uniform(0.5, 1.5))
    ]
    return random.choice(filters)(image)

def crop_image(image, x, y, width, height):
    return image[y:y+height, x:x+width]

def rotate_image(image, angle):
    pil_image = Image.fromarray(image)
    return np.array(pil_image.rotate(angle, expand=True))

# ---------- Main App ----------
def main():
    st.set_page_config(page_title="Pixel Perfect Editor", layout="wide")

    st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
            }
        </style>
    """, unsafe_allow_html=True)

    if 'original_image' not in st.session_state:
        st.session_state.original_image = None

    # ---------- Image Editor UI ----------
    with st.sidebar:
        st.title("Controls")
        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

        st.subheader("Basic Adjustments")
        apply_sharp = st.checkbox("Apply Sharpening")
        apply_smooth = st.checkbox("Apply Smoothing")
        apply_contrast_adj = st.checkbox("Apply Contrast")
        apply_bw = st.checkbox("Convert to Black & White")
        apply_brightness_adj = st.checkbox("Adjust Brightness")

        contrast_factor = st.slider("Contrast Level", 0.5, 3.0, 1.5) if apply_contrast_adj else 1.0
        brightness_factor = st.slider("Brightness Level", 0.5, 2.0, 1.0) if apply_brightness_adj else 1.0

        st.subheader("Special Effects")
        col1, col2 = st.columns(2)
        with col1:
            apply_random = st.button("Surprise Me!")
        with col2:
            cancel_changes = st.button("Cancel Changes")

        st.subheader("Crop Image")
        enable_crop = st.checkbox("Enable Crop")
        x = st.slider("X", 0, 100, 0)
        y = st.slider("Y", 0, 100, 0)
        width = st.slider("Width", 0, 100, 100)
        height = st.slider("Height", 0, 100, 100)
        apply_crop = st.button("Apply Crop")

        st.subheader("Rotate Image")
        enable_rotate = st.checkbox("Enable Rotate")
        rotate_angle = st.slider("Rotation Angle", -180, 180, 0)
        apply_rotate = st.button("Apply Rotation")

        st.subheader("Sketch Effect")
        apply_sketch = st.button("Convert to Sketch")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)

        if st.session_state.original_image is None:
            st.session_state.original_image = image.copy()

        if cancel_changes:
            processed_image = st.session_state.original_image.copy()
        else:
            processed_image = image.copy()

            if apply_sharp:
                processed_image = apply_sharpening(processed_image)
            if apply_smooth:
                processed_image = apply_smoothing(processed_image)
            if apply_contrast_adj:
                processed_image = apply_contrast(processed_image, contrast_factor)
            if apply_brightness_adj:
                processed_image = apply_brightness(processed_image, brightness_factor)
            if apply_bw:
                processed_image = apply_black_white(processed_image)
            if apply_random:
                processed_image = random_filter(processed_image)
            if apply_sketch:
                processed_image = convert_to_sketch(processed_image)

            if enable_crop and apply_crop:
                h, w = processed_image.shape[:2]
                x_px = int(x / 100 * w)
                y_px = int(y / 100 * h)
                width_px = int(width / 100 * w)
                height_px = int(height / 100 * h)
                processed_image = crop_image(processed_image, x_px, y_px, width_px, height_px)

            if enable_rotate and apply_rotate and rotate_angle != 0:
                processed_image = rotate_image(processed_image, rotate_angle)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='image-title'>Original Image</div>", unsafe_allow_html=True)
            st.image(image, use_column_width=True)

        with col2:
            st.markdown("<div class='image-title'>Processed Image</div>", unsafe_allow_html=True)
            if len(processed_image.shape) == 2:
                st.image(processed_image, use_column_width=True, channels="L")
            else:
                st.image(processed_image, use_column_width=True)
    else:
        st.markdown("<p style='color: black;'>Upload an image to start processing.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
