import sys
from collections import Counter
from PIL import Image
sys.path.insert(0,'/home/claude/fable_art')
import px
im=Image.open(sys.argv[1]).convert('RGBA')
o=px.orphans(im)
inv={v[:3]:k for k,v in ((n,px.PAL[i]) for n,i in px.IDX.items())}
import k2
inv={k2.px.PAL[i][:3]:n for n,i in k2.px.IDX.items()}
print(len(o), Counter(inv.get(im.getpixel(p)[:3],'?') for p in o).most_common(12))
