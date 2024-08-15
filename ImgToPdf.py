import os
from tkinter import Tk, Button, Label, filedialog, Listbox, MULTIPLE, END
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def image_to_pdf(image_path, output_pdf_path):
    img = Image.open(image_path)

    img_width, img_height = img.size

    pdf_width, pdf_height = letter

    scale = min(pdf_width / img_width, pdf_height / img_height)
    scaled_width = img_width * scale
    scaled_height = img_height * scale

    x_pos = (pdf_width - scaled_width) / 2
    y_pos = (pdf_height - scaled_height) / 2

    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.drawImage(image_path, x_pos, y_pos, width=scaled_width, height=scaled_height)

    c.showPage()
    c.save()

def convert_images_to_pdfs(image_paths, output_folder):
    total_images = len(image_paths)
    for index, image_path in enumerate(image_paths):
        filename = os.path.basename(image_path)
        output_pdf_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.pdf')

        image_to_pdf(image_path, output_pdf_path)
        print(f"Converted {index + 1}/{total_images}: {filename} to {output_pdf_path}")

def browse_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_paths:
        image_listbox.delete(0, END)
        for file_path in file_paths:
            image_listbox.insert(END, file_path)

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_label.config(text=folder_selected)

def generate_pdfs():
    selected_images = image_listbox.get(0, END)
    output_folder = output_folder_label.cget("text")

    if selected_images and output_folder:
        convert_images_to_pdfs(selected_images, output_folder)
root = Tk()
root.title("Image to PDF Converter")

image_listbox = Listbox(root, selectmode=MULTIPLE, width=50, height=15)
image_listbox.pack(pady=10)
browse_images_button = Button(root, text="Browse Images", command=browse_images)
browse_images_button.pack(pady=5)

output_folder_label = Label(root, text="No folder selected")
output_folder_label.pack(pady=10)
browse_output_button = Button(root, text="Browse Output Folder", command=browse_output_folder)
browse_output_button.pack(pady=5)

generate_button = Button(root, text="Generate PDFs", command=generate_pdfs)
generate_button.pack(pady=20)

root.mainloop()
