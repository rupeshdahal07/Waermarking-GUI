import os
from tkinter import Tk, Label, Button, filedialog, Entry, Canvas, PhotoImage
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")
        self.root.geometry("600x600")

        # Initialize variables
        self.image_path = None
        self.watermark_text = ""
        self.watermarked_image = None

        # UI Components
        Label(root, text="Watermark Text:").pack(pady=10)
        self.watermark_entry = Entry(root, width=40)
        self.watermark_entry.pack(pady=10)

        Button(root, text="Upload Image", command=self.upload_image).pack(pady=10)
        Button(root, text="Add Watermark", command=self.add_watermark).pack(pady=10)
        Button(root, text="Save Image", command=self.save_image).pack(pady=10)

        self.canvas = Canvas(root, width=500, height=400, bg="gray")
        self.canvas.pack(pady=20)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if self.image_path:
            self.display_image(self.image_path)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((500, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(250, 200, image=self.tk_image)

    def add_watermark(self):
        if not self.image_path:
            print("Please upload an image first.")
            return

        self.watermark_text = self.watermark_entry.get()
        if not self.watermark_text:
            print("Please enter a watermark text.")
            return

        # Load the image
        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Set font size relative to the image
        font_size = int(height / 20)
        font = ImageFont.truetype("arial.ttf", font_size)

        # Add watermark text
        text_bbox = font.getbbox(self.watermark_text)  # Updated method
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        position = (width - text_width - 10, height - text_height - 10)  # Bottom-right corner
        draw.text(position, self.watermark_text, fill=(255, 255, 255), font=font)

        # Save watermarked image for preview
        self.watermarked_image = image
        preview_path = "watermarked_preview.jpg"
        image.save(preview_path)
        self.display_image(preview_path)



    def save_image(self):
        if not self.watermarked_image:
            print("No watermarked image to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG Files", "*.jpg"), ("PNG Files", "*.png")],
        )
        if save_path:
            self.watermarked_image.save(save_path)
            print(f"Image saved to {save_path}")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = WatermarkApp(root)
    root.mainloop()
