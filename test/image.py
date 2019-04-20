from PIL import Image

pngFile=Image.open('F:\\ml\\js_racing\\screens_set1\\0.png')

print(pngFile.size)

rgb_image=pngFile.convert('RGB')

r,g,b = rgb_image.getpixel((50,50))

print(r,g,b)