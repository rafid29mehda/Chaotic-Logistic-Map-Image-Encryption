### Chaotic Logistic Map Image Encryption and Decryption

The project implements a chaotic logistic map-based encryption and decryption system for images. The system encrypts an image by applying XOR-based pixel manipulation combined with pixel shuffling, all driven by a chaotic sequence generated from the logistic map. The encryption ensures high security and obscures the original image, while the decryption process reliably restores the original image when provided with the correct key.

---

### **Features**
1. **Chaotic Logistic Map-Based Encryption**:
   - Utilizes a logistic map to generate a chaotic sequence, which serves as the encryption key.
   - Employs XOR operations and pixel shuffling for enhanced obfuscation.

2. **Multi-Layer Encryption**:
   - Two layers of XOR-based encryption:
     - The first layer uses the logistic map sequence.
     - The second layer applies another logistic map sequence on shuffled pixels.

3. **Pixel Shuffling**:
   - Shuffles pixel positions using a deterministic random sequence derived from the encryption key, disrupting spatial correlations.

4. **Decryption**:
   - Reverses the encryption process by applying inverse operations (unshuffling and reversing XOR).

5. **Streamlit Web Application**:
   - A user-friendly interface for uploading images, encrypting them, and decrypting the encrypted images.
   - Displays progress bars during processing for better user experience.
   - Allows users to download the encrypted image.

---

### **How It Works**
#### **Encryption Process**
1. **Input**: A user uploads an image and provides an encryption key (seed value between 0 and 1).
2. **First XOR Operation**:
   - A chaotic sequence is generated using the logistic map and XORed with the flattened image.
3. **Pixel Shuffling**:
   - Pixels are shuffled based on a deterministic random sequence derived from the encryption key.
4. **Second XOR Operation**:
   - A second chaotic sequence is applied using XOR to further obscure the image.
5. **Output**: The encrypted image is displayed and made available for download.

#### **Decryption Process**
1. **Input**: The encrypted image, original image dimensions, and the same key used during encryption.
2. **Reverse Second XOR Operation**:
   - The second chaotic sequence is generated and XORed with the encrypted image.
3. **Unshuffle Pixels**:
   - Pixels are restored to their original positions using the inverse of the deterministic shuffling sequence.
4. **Reverse First XOR Operation**:
   - The first chaotic sequence is used to decrypt the image, restoring the original.
5. **Output**: The decrypted image is displayed.

---

### **How to Use**
1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Upload an image using the file uploader.
3. Select an encryption key (seed) using slider.
4. Click **Encrypt Image** to encrypt the uploaded image.
5. Download the encrypted image using the provided download button.
6. Click **Decrypt Image** to reverse the encryption and view the original image.
