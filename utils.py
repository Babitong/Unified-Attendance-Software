import qrcode
import os
from PIL import Image
from qrcode.constants import ERROR_CORRECT_L
import qrcode.constants
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from io import BytesIO
import base64

# Function to generate a general QR code
def generate_general_qr():
    # The URL the QR should link to
    scan_url ="http://127.0.0.1:8000/check-in/"  # Use your localhost URL for testing
    folder = "media/qrcodes"  # Folder to store the image
    os.makedirs(folder, exist_ok=True)

    # Create a QR code instance


    img = qrcode.make(scan_url)
    file_path = os.path.join(folder, "general_qrcode.png")
    img.save(file_path)  # type: ignore
    
    print("✅ QR saved!")

    
generate_general_qr()

def generate_attendance_chart(data):
    users = [item['user'] for item in data]
    counts = [item['count'] for item in data]

    fig, ax = plt.subplots(figsize=(6, 4))
    # Create a color map

    colormap = cm.get_cmap('tab20', len(users))
    colors = [colormap(i) for i in range(len(users))]

    ax.bar(users, counts, color=colors ,width=0.5) 
    ax.set_title("Attendance by User")
    ax.set_xlabel("USERS" , fontsize=16)
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.xticks(rotation=44, fontsize=8)

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    chart_base64 = base64.b64encode(image_png).decode('utf-8')
    return chart_base64
