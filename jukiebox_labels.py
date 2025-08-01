# Jukiebox, copyright 2025
# Julie C. Mitchell, julie.mitchell@gmail.com
# All rights reserved. May be freely used and
# modified individually by any user.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
import sys

# Read data
data = pd.read_csv(sys.argv[1])

# Set up page layout
paper_width_inch = 8.5
paper_height_inch = 11

cell_width_inch = 3
cell_height_inch = 1

# Uncomment this if the two columns are separated
#space_between_columns_inch = 0.833333
#top_margin_inch = 0.5
#left_margin_inch = 0.833333

# Uncomment this if the two columns are adjacent
space_between_columns_inch = 0
top_margin_inch = 0.5
left_margin_inch = 1.25

n_rows = 10
n_cols = 2
labels_per_page = n_rows * n_cols

# Set figure size to standard letter paper
fig_width = paper_width_inch
fig_height = paper_height_inch

# Load background image
bg_image = mpimg.imread('jukiebox_image.png')

# Function to adjust font size to fit text inside cell
def get_fontsize(text, max_width, ax, base_size):
    t = ax.text(0, 0, text, fontsize=base_size, family='Courier New')
    renderer = plt.gcf().canvas.get_renderer()
    bbox = t.get_window_extent(renderer=renderer)
    text_width = bbox.width / plt.gcf().dpi  # inches
    t.remove()
    if text_width <= max_width:
        return base_size
    else:
        return max(int(base_size * max_width / text_width), 6)  # Minimum size 6

# Draw one page of labels
def draw_page(entries, pdf):

    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_axes([0, 0, 1, 1])  # Fill the entire page
    ax.set_xlim(0, fig_width)
    ax.set_ylim(0, fig_height)
    ax.axis('off')

    def draw_label(x, y, text_a, artist, text_b):
    
        # Background image
        ax.imshow(bg_image, extent=(x, x+cell_width_inch, y, y+cell_height_inch), aspect='auto')
        
        # Border (change edgecolor to match your label)
        rect = Rectangle((x, y), cell_width_inch, cell_height_inch, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)

        # Text with Courier font and dynamic size
        center_x = x + cell_width_inch / 2
        center_y = y + cell_height_inch / 2

        max_artist_width = cell_width_inch * 0.73  # leave a little padding
        max_title_width = cell_width_inch * 0.9  # leave a little padding

        fontsize_a = get_fontsize(text_a, max_title_width, ax, 12)
        fontsize_artist = get_fontsize(artist, max_artist_width, ax, 14)
        fontsize_b = get_fontsize(text_b, max_title_width, ax, 12)

    # Uncomment below to make song titles the same size
      #  if fontsize_a > fontsize_b:
      #      fontsize_a = fontsize_b
      #  else:
      #      fontsize_b = fontsize_a

        ax.text(center_x, center_y + 0.3333, text_a, ha='center', va='center', fontsize=fontsize_a, family='Courier New')
        ax.text(center_x, center_y, artist, ha='center', va='center', fontsize=fontsize_artist, weight='bold', family='Courier New')
        ax.text(center_x, center_y - 0.3333, text_b, ha='center', va='center', fontsize=fontsize_b, family='Courier New')

    for idx, entry in enumerate(entries):
        row = idx % n_rows
        col = idx // n_rows

        x = left_margin_inch + col * (cell_width_inch + space_between_columns_inch)
        y = fig_height - top_margin_inch - (row + 1) * cell_height_inch

        draw_label(x, y, entry[2], entry[1], entry[3])

    pdf.savefig(fig)
    plt.close(fig)

# Create PDF
pdf = matplotlib.backends.backend_pdf.PdfPages(sys.argv[1]+".pdf")

for start_idx in range(0, len(data), labels_per_page):
    page_entries = data.iloc[start_idx:start_idx+labels_per_page]
    draw_page(page_entries.itertuples(index=False), pdf)

pdf.close()
print("PDF with labels saved as "+sys.argv[1]+".pdf")
