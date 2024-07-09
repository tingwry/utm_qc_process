from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import Image

def save_dataframe_as_image(dataframe):
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the size as needed
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center')

    # Save the plot as an image file
    image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if image_path:
        plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        # Open the saved image to confirm it was saved correctly
        Image.open(image_path).show()


