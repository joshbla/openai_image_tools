from PIL import Image, ImageDraw

img = Image.new('RGBA', (1024, 1024), color=(0, 0, 0, 255))
draw = ImageDraw.Draw(img)
draw.rectangle([1, 1, 1022, 1022], fill=(255, 255, 255, 0))
img.save('templateborder.png')