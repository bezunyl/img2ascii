from PIL import Image, ImageDraw, ImageFont
import math
import sys
import getopt

FILE = "rufus"

# DEFINITIONS
class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def relative_luminance(r, g, b):
    return round(((0.2126*r + 0.7152*g + 0.0722*b) / 255), 1)

CHARS = {
    0.0: "$",
    0.1: "@",
    0.2: "%",
    0.3: "#",
    0.4: "*",
    0.5: "+",
    0.6: "=",
    0.7: "-",
    0.8: ":",
    0.9: ".",
    1.0: " "
}
"""
argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "f:")

except:
    print("No file given. Use -f to specify an image.")

for opt, arg in opts:
    if opt in ["-f"]:
        FILE = arg
"""
img = Image.open("./assets/%s.jpg"%(FILE))

cluster_size = 2
cluster_w = cluster_size
cluster_h = cluster_size

cols = img.size[0] // cluster_w
rows = img.size[1] // cluster_h

img_pix = img.load()

map_hori = []

for i in range(cols):
    pix_hori = []
    for j in range(i * cluster_w, i * cluster_w + cluster_w):
        pix_hori.append(j)
    map_hori.append(pix_hori)

map_vert = []

for i in range(rows):
    pix_vert = []
    for j in range(i * cluster_h, i * cluster_h + cluster_h):
        pix_vert.append(j)
    map_vert.append(pix_vert)

clusters = []

for i in range(rows):
    for j in range(cols):
        cluster = []
        for k in range(cluster_size):
            for l in range(cluster_size):
                cluster.append(Pixel(map_hori[j][k], map_vert[i][l]))
        clusters.append(cluster)

luma = []

for cluster in clusters:
    sum = 0
    for pix in cluster:
        color = img_pix[pix.x, pix.y]
        sum += relative_luminance(color[0], color[1], color[2])
    luma.append(round(sum / len(cluster), 1))


result = []

for i in range(rows):
    result_col = ""
    for j in range(cols):
        result_col += CHARS[luma[i * cols + j]]
    result.append(result_col)

result_text = "\n".join(result)

with open("./results/%s.txt"%(FILE), "w") as F:
    F.write(result_text)
    F.close()

result_img = Image.new("RGB", (int(round(img.size[0] * (6/cluster_size), 0)), int(round(img.size[1] * (6/cluster_size), 0))), color = (255, 255, 255))
result_draw = ImageDraw.Draw(result_img)
#result_font = ImageFont.truetype("./assets/fonts/consola", 12)
result_draw.text((0, 0), result_text, fill = (0, 0, 0), spacing = -5, stroke_width = 30)

result_img.show()
result_img.save("./results/%s.jpg"%(FILE))

