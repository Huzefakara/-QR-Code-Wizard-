 # Import necessary modules
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import cv2

# Create a class for the QR code encoder application
class QREncoderApp:
    def __init__(self, parent):
        # Initialize the application with a parent window
        self.parent = parent
        self.parent.title("QR Code Encoder and Decoder")

        # Set up a style for GUI elements
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), foreground='black')

        # Create a frame for the encoder section with a light blue background
        encoder_frame = ttk.Frame(self.parent, style='Encoder.TFrame')
        encoder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create a label for the encoder section
        encoder_label = ttk.Label(encoder_frame, text="QR Encoder", style='Encoder.TLabel')
        encoder_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create a label and an entry field for entering a URL
        url_label = ttk.Label(encoder_frame, text="Enter Website URL:")
        url_label.grid(row=1, column=0, padx=10, pady=10)
        self.url_entry = ttk.Entry(encoder_frame, width=40)
        self.url_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create a label for displaying the generated QR code
        self.qr_code_label = ttk.Label(encoder_frame)
        self.qr_code_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Create a button to generate the QR code
        generate_button = ttk.Button(encoder_frame, text="Generate QR Code", command=self.generate_qr_code)
        generate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Create a button to save the generated QR code
        save_button = ttk.Button(encoder_frame, text="Save QR Code", command=self.save_qr_code)
        save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Initialize a variable to store the QR code image
        self.qr_image = None

    def generate_qr_code(self):
        # Generate a QR code based on the entered URL
        url = self.url_entry.get()
        if url:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Store the generated QR code image
            self.qr_image = qr_image

            # Display the QR code image on the GUI
            qr_photo = ImageTk.PhotoImage(qr_image)
            self.qr_code_label.config(image=qr_photo)
            self.qr_code_label.image = qr_photo
        else:
            self.qr_code_label.config(text="Please enter a valid URL")

    def save_qr_code(self):
        # Save the generated QR code as a PNG file
        if self.qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

            if file_path:
                self.qr_image.save(file_path, "PNG")
        else:
            messagebox.showerror("Error", "No QR code image to save")

# Create a class for the QR code decoder application
class QRDecoderApp:
    def __init__(self, parent):
        self.parent = parent

        # Set up a style for GUI elements
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), foreground='black')

        # Create a frame for the decoder section with a light green background
        decoder_frame = ttk.Frame(self.parent, style='Decoder.TFrame')
        decoder_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Create a label for the decoder section
        decoder_label = ttk.Label(decoder_frame, text="QR Decoder", style='Decoder.TLabel')
        decoder_label.grid(row=0, column=0, padx=10, pady=10)

        # Initialize variables for storing QR code image and decoded link
        self.qr_image = None
        self.decoded_link_text = tk.StringVar()

        # Create an entry field for displaying the decoded link
        decoded_link_entry = ttk.Entry(decoder_frame, textvariable=self.decoded_link_text, width=40)
        decoded_link_entry.grid(row=2, column=0, padx=10, pady=10)

        # Create a button to open the decoded link in a web browser
        open_button = ttk.Button(decoder_frame, text="Open Link", command=self.open_decoded_link)
        open_button.grid(row=3, column=0, padx=10, pady=10)

        # Create a button to decode a QR code from an image
        decode_button = ttk.Button(decoder_frame, text="Decode QR Code", command=self.decode_qr_code)
        decode_button.grid(row=1, column=0, padx=10, pady=10)

    def decode_qr_code(self):
        # Decode a QR code from a selected image file
        img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")])
        if img_path:
            img = cv2.imread(img_path)
            decoded_objects = decode(img)

            if decoded_objects:
                first_object = decoded_objects[0]
                qr_data = first_object.data.decode("utf-8")
                self.decoded_link_text.set(qr_data)
            else:
                messagebox.showerror("Error", "No QR code found in the selected image")
        else:
            messagebox.showerror("Error", "No image selected")

    def open_decoded_link(self):
        # Open the decoded link in a web browser
        decoded_link = self.decoded_link_text.get()
        if decoded_link:
            import webbrowser
            webbrowser.open(decoded_link)

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    root.title("QR Code Encoder and Decoder")

    # Set up styles for different sections of the GUI
    style = ttk.Style()
    style.configure('Encoder.TFrame', background='gold')
    style.configure('Decoder.TFrame', background='blue')
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('Encoder.TLabel', font=('Helvetica', 18, 'bold'))
    style.configure('Decoder.TLabel', font=('Helvetica', 18, 'bold'))

    # Expand the encoder and decoder sections to fill the vertical space
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Create instances of the encoder and decoder applications
    encoder_app = QREncoderApp(root)
    decoder_app = QRDecoderApp(root)

    # Start the main GUI event loop
    root.mainloop()
