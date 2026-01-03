from PIL import Image
import os

IN_DIR = 'screenshots'

files = [f for f in os.listdir(IN_DIR) if f.startswith('real_') and f.lower().endswith('.png')]
print(f'Found {len(files)} files to optimize')

for fname in files:
    path = os.path.join(IN_DIR, fname)
    img = Image.open(path)
    # Resize if wider than 1200 px
    max_width = 1200
    if img.width > max_width:
        new_h = int(max_width * img.height / img.width)
        img = img.resize((max_width, new_h), Image.LANCZOS)
        print(f'Resized {fname} to {img.size}')
    # Convert to palette-based (quantize) to reduce size while keeping quality
    quantized = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    out_path = os.path.join(IN_DIR, fname.replace('.png', '.opt.png'))
    quantized.save(out_path, optimize=True)
    orig_size = os.path.getsize(path)
    new_size = os.path.getsize(out_path)
    print(f'Optimized {fname}: {orig_size/1024:.1f}KB -> {new_size/1024:.1f}KB')

print('Optimization complete. Optimized files have suffix .opt.png')