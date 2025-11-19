import streamlit as st
from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo
import io

st.set_page_config(page_title="Image Border Tool", layout="wide")

st.title("📸 Image Border Tool")
st.markdown("Add white borders to your images with custom sizing")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
    help="Upload an image from your iPhone, iPad, or computer"
)

if uploaded_file is not None:
    # Load the image
    original_image = Image.open(uploaded_file)
    
    # Display original dimensions
    width, height = original_image.size
    st.info(f"Original image size: {width} × {height} pixels")
    
    # Border size slider (percentage of longest dimension)
    border_percentage = st.slider(
        "Border size (% of longest dimension)",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        help="Default is 5% matching your script"
    )
    
    # Calculate border size in pixels
    max_dimension = max(width, height)
    border_size = int(max_dimension * (border_percentage / 100))
    
    st.caption(f"Border width: {border_size} pixels")
    
    # Create bordered image
    bordered_image = ImageOps.expand(
        original_image,
        border=border_size,
        fill='white'
    )
    
    # Preview section
    st.subheader("Preview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original**")
        st.image(original_image, use_container_width=True)
    
    with col2:
        st.markdown("**With Border**")
        st.image(bordered_image, use_container_width=True)
    
    # Download section
    st.subheader("Download")
    
    # Determine output format
    output_format = original_image.format if original_image.format else "PNG"
    file_extension = output_format.lower()
    
    # Convert image to bytes
    buf = io.BytesIO()
    
    # Preserve EXIF data
    exif_data = original_image.info.get('exif')
    
    # Preserve quality for JPEGs
    if output_format in ["JPEG", "JPG"]:
        if exif_data:
            bordered_image.save(buf, format="JPEG", quality=95, optimize=True, exif=exif_data)
        else:
            bordered_image.save(buf, format="JPEG", quality=95, optimize=True)
        mime_type = "image/jpeg"
    else:
        # For PNG, preserve metadata differently
        metadata = PngInfo()
        for key, value in original_image.info.items():
            if isinstance(value, (str, bytes)):
                metadata.add_text(str(key), str(value))
        bordered_image.save(buf, format="PNG", optimize=True, pnginfo=metadata)
        mime_type = "image/png"
        file_extension = "png"
    
    buf.seek(0)
    
    # Generate output filename
    original_name = uploaded_file.name.rsplit('.', 1)[0]
    output_filename = f"{original_name}_bordered.{file_extension}"
    
    # Download button
    st.download_button(
        label="⬇️ Download Bordered Image",
        data=buf,
        file_name=output_filename,
        mime=mime_type,
        help="Download full quality image with border",
        use_container_width=True
    )
    
    new_width, new_height = bordered_image.size
    st.success(f"New image size: {new_width} × {new_height} pixels")

else:
    st.info("👆 Upload an image to get started")
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload** your image using the file uploader above
        2. **Adjust** the border size with the slider
        3. **Preview** the original and bordered versions side by side
        4. **Download** your bordered image at full quality
        
        **Tips:**
        - Default border is 5% (same as your script)
        - Works with JPG and PNG files
        - Preserves image quality and EXIF data (including creation date)
        - Border size scales with image dimensions
        """)
