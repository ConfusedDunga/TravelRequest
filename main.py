import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from base64 import b64encode

def resize_and_crop(image, target_width, target_height):
    """
    Resize and crop the image to cover the specified area while maintaining the aspect ratio.
    """
    width, height = image.size
    aspect_ratio = width / height

    target_ratio = target_width / target_height

    if aspect_ratio > target_ratio:
        # Resize based on width
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        # Resize based on height
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    # Resize the image with LANCZOS filter for antialiasing
    resized_img = image.resize((new_width, new_height), Image.LANCZOS)

    # Crop the center of the resized image to cover the specified area
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    cropped_img = resized_img.crop((left, top, right, bottom))

    return cropped_img

def add_data_to_image(template_path, user_data, uber_screenshot=None):
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Set custom font size
    font_size = 46
    font_path = "arial.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    # Example: Adding user data to specific locations
    draw.text((310, 1280), f"{user_data['Date']}", fill="black", font=font, antialias=True)
    draw.text((670, 600), f"{user_data['Name']}", fill="black", font=font, antialias=True)
    draw.text((600, 1280), f"{user_data['From']}", fill="black", font=font, antialias=True)
    draw.text((990, 1280), f"{user_data['To']}", fill="black", font=font, antialias=True)
    draw.text((1500, 1280), f"{user_data['Travelling Mode']}", fill="black", font=font, antialias=True)

    # Paste Uber screenshot if provided
    if uber_screenshot is not None:
        uber_img = Image.open(uber_screenshot)

        # Calculate scaling factors for width and height
        target_width_mm = 48
        target_height_mm = 108
        target_width_pixels = int((target_width_mm / 25.4) * 300)  # Assuming 300 DPI
        target_height_pixels = int((target_height_mm / 25.4) * 300)

        # Resize and crop the Uber screenshot to specific dimensions
        uber_img = resize_and_crop(uber_img, target_width=target_width_pixels, target_height=target_height_pixels)
        img.paste(uber_img, (960, 1700))  # Adjust the coordinates as needed

    # You can add more data based on your template
    img = img.convert("RGB")
    return img


def main():
    st.title("Nepal Bankers' Association")
    st.subheader("Staff Travel Form")

    # Input fields
    date = st.date_input("Date")
    name = st.text_input("Name")
    travel_from = st.text_input("From")
    travel_to = st.text_input("To")
    travel_mode = st.text_input("Travelling Mode")

    # Upload Uber screenshot
    uber_screenshot = st.file_uploader("Upload Uber Screenshot", type=["png", "jpg", "jpeg"])

    if st.button("Generate and Download Image"):
        # Prepare user data
        user_data = {
            "Date": date,
            "Name": name,
            "From": travel_from,
            "To": travel_to,
            "Travelling Mode": travel_mode,
        }

        # Process Uber screenshot if provided
        if uber_screenshot is not None:
            # Do something with the Uber screenshot, you can save it or process it as needed
            pass

        # Add data to the image
        template_path = "form.png"  # Replace with the path to your high-resolution template image
        result_img = add_data_to_image(template_path, user_data, uber_screenshot)

        # Convert image to bytes
        img_bytes = BytesIO()
        result_img.save(img_bytes, format="PNG", quality=95)  # Adjust quality as needed

        # Display the result image
        st.image(result_img, caption="Generated Image", use_column_width=True)

        # Provide a download button for the user
        st.markdown(get_image_download_button(img_bytes), unsafe_allow_html=True)

def get_image_download_button(img_bytes):
    download_button_str = f'<a href="data:application/octet-stream;base64,{b64encode(img_bytes.getvalue()).decode()}" download="output_image.png"><button>Download Image</button></a>'
    return download_button_str

if __name__ == "__main__":
    main()
