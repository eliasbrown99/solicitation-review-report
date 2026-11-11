"""Build the chart from aggregate data and diagrams from reviewed source behavior."""
import json
from pathlib import Path
from html import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
data = json.loads((ROOT / 'analysis/derived/saved-output-audit.json').read_text())
paper, ink, brass, line = '#f7f2e8', '#302923', '#78572f', '#dcd2c3'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'text.color': ink, 'axes.labelcolor': ink, 'xtick.color': ink, 'ytick.color': ink, 'svg.fonttype':'path'})
for label, size in [('wide',(8.5,3.5)),('mobile',(4.4,4.1))]:
    fig, ax = plt.subplots(figsize=size, facecolor=paper)
    ax.set_facecolor(paper)
    counts = data['top_level_bullets']
    cats = [f'{n} bullets' for n in counts]
    values = list(counts.values())
    bars = ax.barh(cats, values, color=brass, height=.56)
    ax.invert_yaxis()
    for bar,v in zip(bars,values): ax.text(v+.7,bar.get_y()+bar.get_height()/2,str(v),va='center',fontweight='bold')
    ax.set_xlim(0,45)
    ax.set_xticks([0,10,20,30,40])
    ax.set_xlabel('Number of saved section summaries',labelpad=12)
    ax.xaxis.grid(True,color=line,linewidth=.7)
    ax.set_axisbelow(True)
    ax.tick_params(length=0,pad=8)
    for s in ax.spines.values(): s.set_visible(False)
    fig.tight_layout(pad=1.2)
    fig.savefig(OUT/f'bullet-counts-{label}.svg',facecolor=paper)
    plt.close(fig)

def svg_start(w,h,title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{brass}"/></marker></defs><rect width="100%" height="100%" fill="{paper}"/><g font-family="Arial, sans-serif" fill="{ink}">']

def box(parts,x,y,w,h,title,lines):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#eee5d8" stroke="{line}"/>')
    parts.append(f'<text x="{x+18}" y="{y+29}" font-size="18" font-weight="bold">{escape(title)}</text>')
    for i,t in enumerate(lines): parts.append(f'<text x="{x+18}" y="{y+55+i*23}" font-size="15">{escape(t)}</text>')

def arrow(parts,x1,y1,x2,y2):
    parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{brass}" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')

steps=[('01  Upload & parse',['PDF or Word → Markdown','LlamaParse extracts text and headings']),('02  Build sections',['Check heading numbering with an LLM','Flatten retained headings into sections']),('03  Select relevant material',['Heading + first 1,000 characters','Excluded sections stop here']),('04  Summarize & condense',['2,000-character chunks; 100 overlap','Prompt requests ≤5 bullets per section']),('05  Save & review',['JSON text in SQLite → React interface','Search, reopen, or delete saved results'])]
# A vertical connected flow keeps stage labels legible at phone width.
parts=svg_start(430,755,'From solicitation to saved digest','Read top to bottom. An uploaded file is parsed, divided into sections, filtered for relevance, summarized, and stored for human review. Excluded sections do not reach the summary.')
for i,(title,lines) in enumerate(steps):
    y=12+i*148
    box(parts,10,y,410,111,title,lines)
    if i<4: arrow(parts,215,y+111,215,y+140)
parts.append('</g></svg>')
(OUT/'workflow.svg').write_text(''.join(parts))

parts=svg_start(430,580,'One saved row contains a list of sections','The summaries table has id, filename, upload_time, and summary. The summary field is JSON text holding a list of heading and summary objects, not a separate relational section table.')
box(parts,10,12,410,190,'SQLite: summaries table',['id — primary key','filename — uploaded name','upload_time — saved timestamp','summary — JSON serialized as TEXT'])
arrow(parts,215,202,215,252)
box(parts,10,268,410,127,'Inside the summary field',['A list of section objects','Each has: heading + summary','One document row → many sections'])
arrow(parts,215,395,215,445)
box(parts,10,461,410,105,'Displayed in the interface',['Heading followed by summary bullets','No page-level source citations stored'])
parts.append('</g></svg>')
(OUT/'storage.svg').write_text(''.join(parts))
print('Built two chart variants and two source-based diagrams.')
