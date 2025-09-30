from typing import List, Dict
from .decomposer import Decomposer
from .motif_encoder import MotifEncoder

# Correct Codon Python interop imports: explicitly import Pillow submodules
try:
    from python import PIL.Image as Image
    from python import PIL.ImageDraw as ImageDraw
    from python import PIL.ImageFont as ImageFont
except Exception as e:
    Image = None; ImageDraw = None; ImageFont = None

def _assign_colors(symbols: List[str]):
    palette = [
        (31,119,180),(255,127,14),(44,160,44),(214,39,40),
        (148,103,189),(140,86,75),(227,119,194),(127,127,127),
        (188,189,34),(23,190,207)
    ]
    mapping = {}
    idx = 0
    for s in symbols:
        if s == '-':
            mapping[s] = (255,255,255)
        else:
            mapping[s] = palette[idx % len(palette)]
            idx += 1
    return mapping

def generate_plots(tr_id: str, sample_ids: List[str], aligned_sequences: List[str], symbol_map: Dict[str,str]):
    if Image is None or ImageDraw is None or ImageFont is None:
        raise ImportError("Pillow not available to Codon. Ensure CODON_PYTHON and PYTHONPATH are set and Pillow is installed.")
    if not aligned_sequences:
        return
    rows = len(aligned_sequences)
    cols = len(aligned_sequences[0])
    cell = 20

    used_symbols = sorted({ch for seq in aligned_sequences for ch in seq})
    sym_to_color = _assign_colors(used_symbols)

    # composition image
    img_w, img_h = cols*cell, rows*cell
    comp = Image.new('RGB', (img_w, img_h), color=(255,255,255))
    d = ImageDraw.Draw(comp)
    for r, seq in enumerate(aligned_sequences):
        for c, ch in enumerate(seq):
            x0, y0 = c*cell, r*cell
            x1, y1 = x0+cell, y0+cell
            d.rectangle([x0,y0,x1,y1], fill=sym_to_color.get(ch,(0,0,0)), outline=(0,0,0))
    comp.save(f"{tr_id}_trplot.png")

    # legend
    motifs = sorted(symbol_map.keys())
    lh = 20
    lw = 480
    lh_total = max(1, len(motifs))*lh
    leg = Image.new('RGB', (lw, lh_total), color=(255,255,255))
    dl = ImageDraw.Draw(leg)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    for i, motif in enumerate(motifs):
        sym = symbol_map[motif]
        color = sym_to_color.get(sym, (0,0,0))
        y = i*lh
        dl.rectangle([5,y+5,15,y+15], fill=color, outline=(0,0,0))
        dl.text((22,y+3), f"{motif}  ({sym})", fill=(0,0,0), font=font)
    leg.save(f"{tr_id}_color_map.png")

class TandemRepeatVizWorker:
    def __init__(self):
        self.decomposer = Decomposer()
        self.encoder = MotifEncoder()

    def generate_trplot(self, tr_id: str, sample_ids: List[str], tr_sequences: List[str], motifs: List[str]):
        decomposed = [self.decomposer.decompose(seq, motifs) for seq in tr_sequences]
        encoded, symbol_map = self.encoder.encode(decomposed, motif_map_file=f"{tr_id}_motif_map.txt")
        aligned: List[str] = []
        if encoded:
            max_len = max(len(s) for s in encoded)
            for s in encoded:
                if len(s) < max_len:
                    s = s + ('-' * (max_len - len(s)))
                aligned.append(s)
        with open(f"{tr_id}_aligned.txt", 'w') as f:
            for sid, seq in zip(sample_ids, aligned):
                f.write(f">{sid}\n{seq}\n")
        generate_plots(tr_id, sample_ids, aligned, symbol_map)
