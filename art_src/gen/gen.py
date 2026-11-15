import sys, time, torch
from diffusers import AutoPipelineForText2Image
torch.set_num_threads(2)
pipe = AutoPipelineForText2Image.from_pretrained('/home/claude/models/sd-turbo', dtype=torch.bfloat16, variant='fp16')
pipe.vae.enable_tiling(); pipe.enable_attention_slicing()
prompt = sys.argv[1]; out = sys.argv[2]; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
t = time.time()
img = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0, width=512, height=512,
           generator=torch.Generator().manual_seed(seed)).images[0]
img.save(out); print('ok', time.time() - t)
