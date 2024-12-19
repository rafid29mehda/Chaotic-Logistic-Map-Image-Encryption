from PIL import Image
import numpy as np
import streamlit as st
import io
import time
import random

# Resize image to prevent memory issues with large images
def resize_image(img, max_size=(3000, 3000)):
    """
    Resize image to fit within max_size while maintaining aspect ratio.
    """
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img

# Logistic map function
def logistic_map(r, x):
    return r * x * (1 - x)

# Generate chaotic key based on the logistic map
def generate_key(seed, n):
    key = []
    x = seed
    for _ in range(n):
        x = logistic_map(3.9, x)
        key.append(int(x * 255) % 256)  # Map to 0-255
    return np.array(key, dtype=np.uint8)

# Shuffle pixels using a chaotic sequence
def shuffle_pixels(img_array, seed):
    h, w, c = img_array.shape
    num_pixels = h * w
    flattened = img_array.reshape(-1, c)
    indices = np.arange(num_pixels)
    
    random.seed(seed)
    random.shuffle(indices)  # Shuffle indices
    
    shuffled = flattened[indices]
    return shuffled.reshape(h, w, c), indices

# Multi-layer encryption using logistic map and pixel shuffling
def encrypt_image(img_array, seed):
    h, w, c = img_array.shape
    flat_image = img_array.flatten()

    # Generate chaotic key
    chaotic_key = generate_key(seed, len(flat_image))
    
    # XOR-based encryption
    encrypted_flat = [pixel ^ chaotic_key[i] for i, pixel in enumerate(flat_image)]
    encrypted_array = np.array(encrypted_flat, dtype=np.uint8).reshape(h, w, c)

    # Pixel shuffling
    shuffled_array, indices = shuffle_pixels(encrypted_array, seed)

    # Second layer of logistic map encryption
    chaotic_key_2 = generate_key(seed * 1.1, len(flat_image))
    shuffled_flat = shuffled_array.flatten()
    doubly_encrypted_flat = [pixel ^ chaotic_key_2[i] for i, pixel in enumerate(shuffled_flat)]
    doubly_encrypted_array = np.array(doubly_encrypted_flat, dtype=np.uint8).reshape(h, w, c)

    return doubly_encrypted_array

# Decrypt function
def decrypt_image(encrypted_array, seed, original_shape):
    h, w, c = original_shape
    flat_image = encrypted_array.flatten()

    # Generate the second chaotic key
    chaotic_key_2 = generate_key(seed * 1.1, len(flat_image))

    # Reverse the second XOR encryption
    xor_reversed_flat = [pixel ^ chaotic_key_2[i] for i, pixel in enumerate(flat_image)]
    xor_reversed_array = np.array(xor_reversed_flat, dtype=np.uint8).reshape(h, w, c)

    # Reverse pixel shuffling
    shuffled_array = xor_reversed_array
    num_pixels = h * w
    flattened = shuffled_array.reshape(-1, c)
    indices = np.arange(num_pixels)

    random.seed(seed)
    random.shuffle(indices)  # Reuse the same shuffle logic
    unshuffled = np.zeros_like(flattened)
    unshuffled[indices] = flattened
    unshuffled_array = unshuffled.reshape(h, w, c)

    # Generate the first chaotic key
    chaotic_key_1 = generate_key(seed, len(flat_image))

    # Reverse the first XOR encryption
    decrypted_flat = [pixel ^ chaotic_key_1[i] for i, pixel in enumerate(unshuffled_array.flatten())]
    decrypted_array = np.array(decrypted_flat, dtype=np.uint8).reshape(h, w, c)

    return decrypted_array

# Streamlit App
def main():
    st.title("Enhanced Chaotic Logistic Map Image Encryption")
    st.write("Upload an image to encrypt and decrypt using advanced chaotic logistic map methods.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        with st.spinner("Processing upload..."):
            # Simulate a loading delay for upload progress
            progress_bar = st.progress(0)
            for percent_complete in range(0, 101, 20):
                time.sleep(0.1)  # Simulate progress
                progress_bar.progress(percent_complete)

        # Load the uploaded image
        input_image = Image.open(uploaded_file)

        # Resize the image if necessary
        input_image = resize_image(input_image)

        # Display original image
        st.image(input_image, caption="Uploaded Image", use_container_width=True)

        # Convert image to numpy array
        img_array = np.array(input_image)

        # Key input
        key_seed = st.slider("Set the encryption key seed (0 < key < 1)", min_value=0.001, max_value=0.999, step=0.001)

        # Encrypt Image
        if st.button("Encrypt Image"):
            with st.spinner("Encrypting image..."):
                # Simulate a loading delay for encryption progress
                progress_bar = st.progress(0)
                for percent_complete in range(0, 101, 20):
                    time.sleep(0.1)  # Simulate progress
                    progress_bar.progress(percent_complete)

                # Encrypt the image
                encrypted_array = encrypt_image(img_array, key_seed)
                encrypted_image = Image.fromarray(encrypted_array)

                # Store encrypted array in session state
                st.session_state["encrypted_array"] = encrypted_array
                st.session_state["original_shape"] = img_array.shape
                st.session_state["key_seed"] = key_seed

                # Display encrypted image
                st.image(encrypted_image, caption="Encrypted Image", use_container_width=True)

                # Save encrypted image to a buffer
                buffer = io.BytesIO()
                encrypted_image.save(buffer, format="PNG")
                buffer.seek(0)

                # Download button for encrypted image
                st.download_button(
                    label="Download Encrypted Image",
                    data=buffer,
                    file_name="encrypted_image.png",
                    mime="image/png"
                )

        # Decrypt Image
        if st.button("Decrypt Image"):
            if "encrypted_array" in st.session_state:
                with st.spinner("Decrypting image..."):
                    decrypted_array = decrypt_image(
                        st.session_state["encrypted_array"],
                        st.session_state["key_seed"],
                        st.session_state["original_shape"]
                    )
                    decrypted_image = Image.fromarray(decrypted_array)

                    # Display decrypted image
                    st.image(decrypted_image, caption="Decrypted Image", use_container_width=True)
            else:
                st.error("No encrypted image found. Please encrypt an image first.")

if __name__ == "__main__":
    main()
