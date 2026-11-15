"""img2img: eigene Zeichnung (Pose, Form, Farben) -> sd-turbo verfeinert Details -> zurück zu Pixel-Art."""
import sys, json, time, torch
from PIL import Image, ImageFilter
from diffusers import AutoPipelineForImage2Image
torch.set_num_threads(2)
pipe = AutoPipelineForImage2Image.from_pretrained('/home/claude/models/sd-turbo', dtype=torch.bfloat16, variant='fp16')
pipe.vae.enable_tiling(); pipe.enable_attention_slicing()
def prep(src):
    im = Image.open(src).convert('RGBA')
    s = 512 / max(im.size) * 0.86
    im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST)
    bg = Image.new('RGB', (512, 512), (255, 255, 255))
    bg.paste(im, ((512 - im.width) // 2, 512 - im.height - 24), im)
    return bg.filter(ImageFilter.GaussianBlur(2))
for j in json.load(open(sys.argv[1])):
    t = time.time()
    init = prep(j['src'])
    steps = j.get('steps', 4); st = j.get('strength', 0.5)
    out = pipe(prompt=j['prompt'], image=init, num_inference_steps=steps, strength=st, guidance_scale=0.0,
               generator=torch.Generator().manual_seed(j.get('seed', 1))).images[0]
    out.save(j['out']); print('ok', j['out'], round(time.time() - t, 1), flush=True)
