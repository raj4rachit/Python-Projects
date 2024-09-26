from rembg import remove
from PIL import Image

input_path='3.png'
output_path='4.png'

input=Image.open(input_path)
output=remove(input)
output.save(output_path)

print('done')