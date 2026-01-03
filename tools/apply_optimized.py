import os

IN_DIR = 'screenshots'

for f in os.listdir(IN_DIR):
    if f.endswith('.opt.png'):
        orig = f.replace('.opt.png', '.png')
        src = os.path.join(IN_DIR, f)
        dst = os.path.join(IN_DIR, orig)
        # Backup original
        bak = dst + '.bak'
        if os.path.exists(dst):
            os.replace(dst, bak)
        os.replace(src, dst)
        print(f'Applied optimized image: {dst} (backup at {bak} if existed)')

print('Apply complete')