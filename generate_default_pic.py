from PIL import Image, ImageDraw

def create_default_profile_pic():
    # Create a 200x200 image with a blue background
    size = 200
    img = Image.new('RGB', (size, size), color='#4a90e2')
    draw = ImageDraw.Draw(img)
    
    # Draw a light circle for the avatar
    circle_color = '#ffffff'
    margin = 40
    draw.ellipse([margin, margin, size-margin, size-margin], fill=circle_color)
    
    # Draw a smaller circle for the head
    head_margin = 70
    draw.ellipse([head_margin, head_margin-20, size-head_margin, size-head_margin+20], fill='#4a90e2')
    
    # Draw the body
    body_points = [
        (size//2, size//2+10),  # top
        (size//2+40, size-margin),  # bottom right
        (size//2-40, size-margin),  # bottom left
    ]
    draw.polygon(body_points, fill='#4a90e2')
    
    # Save the image
    img.save('media/profile_pics/default.png')