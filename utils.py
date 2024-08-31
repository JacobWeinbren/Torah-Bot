def save_image(screenshot, filename="output_image.png"):
    with open(filename, "wb") as f:
        f.write(screenshot)
    print(f"Image generated: {filename}")
    print(f"Image size: {len(screenshot) / 1024:.2f} KB")
