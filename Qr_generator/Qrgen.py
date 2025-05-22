from tkinter import *
import qrcode
import os
from PIL import Image as PilImage, ImageTk, ImageSequence

root = Tk()
root.title("QR Code Generator")
root.geometry("800x600")
root.config(bg="#F2EFE5")
root.resizable(False, False)

gif_path = r"C:\Users\Dharmin vadher\Desktop\PyScripts\Qr_generator\QRcodescan.gif"

#
def animate_gif(label, gif_path, cycles):
    gif_image = PilImage.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]
    frame_count = len(frames)

    def play_gif(count):
        frame = frames[count % frame_count]
        label.config(image=frame)
        root.update_idletasks()
        if count < frame_count * cycles:
            label.after(gif_image.info['duration'], play_gif, count + 1)
        else:
            label.place_forget()
            display_qr_code()

    label.place(x=400, y=150)
    play_gif(0)

def display_qr_code():
    qr_text = entry_text.get()
    qr = qrcode.make(qr_text)

    try:
        global qr_image
        qr_image = ImageTk.PhotoImage(qr)
        image_view.config(image=qr_image)
        image_view.place(x=400, y=150)
    except Exception as e:
        print(f"Error displaying QR code: {e}")

def generate():
    qr_text = entry_text.get().strip()
    if not qr_text:
        warning_label = Label(root, text="⚠ Please enter some text!", fg="red", bg="#F2EFE5", font=("Arial", 12))
        warning_label.place(x=50, y=280)
        root.after(2000, warning_label.destroy)  # auto hide after 2 seconds
        return

    loading_label = Label(root, text="", fg="white", bg="#2B2B2B")
    loading_label.place(x=400, y=150)
    animate_gif(loading_label, gif_path, cycles=1)


Label(root, text="Enter text or URL:", fg="#BF9264", bg="#F2EFE5", font=30).place(x=50, y=215)

image_view = Label(root, bg="#2B2B2B")
# image_view.place(x=400, y=150)

entry_text = Entry(root, width=28, font="arial 15")

entry_text.place(x=50, y=250)

button = Button(root, text="Generate", width=20, height=2, bg="#D4C9BE", fg="white", command=generate)
button.place(x=50, y=300)

root.mainloop()