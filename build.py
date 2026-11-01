"""Builds the TechVestVentures Ukraine Russia Casualty Graphs site from focus/ukraine-casualties/ charts and records.json.
Modeled on jobs-site/build.py. Numbers come only from the linked sources."""
import os,sys,shutil,json,glob
sys.path.insert(0,'/workspace/risk-watcher/graphs-site');sys.path.insert(0,'/workspace/risk-watcher');os.chdir(os.path.dirname(os.path.abspath(__file__)))
from common import *
T="TechVestVentures Ukraine Russia Casualty Graphs";J="/workspace/risk-watcher/focus/ukraine-casualties/"
R={g["file"]:g for g in json.load(open(J+"work/records.json"))}
F=lambda n:[f for f in R if f.startswith(f"UKR RUS Casualties {n:02d} ")][0]
TABS=[("exchanges","Body Exchanges","The one bilateral number both governments publish: bodies handed back in each swap since November 2024, cumulative totals, yearly returns to Ukraine, and the per-swap ratio. A swap counts bodies each side holds, not the deaths each side suffered.",[F(i) for i in (1,2,3,4)]),
 ("claims","Claims by Side","Who says what: Kyiv's, Moscow's, Western and independent (named-dead) figures for each side's losses, labelled by claimant.",[F(i) for i in (5,6,7)]),
 ("divergence","Divergence and Civilians","The swap ratio against the Western-implied killed ratio, and UN-verified civilian casualties.",[F(i) for i in (8,9)])]
shutil.rmtree("issues",ignore_errors=True);os.makedirs("issues/img");os.makedirs("assets",exist_ok=True)
assert sorted(f for _,_,_,fs in TABS for f in fs)==sorted(os.path.basename(p) for p in glob.glob(J+"UKR RUS Casualties 0*.png")),"chart set changed"
tabs=[];src={};n=0
def w(k,lab,body): open(f"issues/{k}.html","w").write(page(T,k,body));tabs.append((k,lab))
for k,lab,note,fs in TABS:
    b=f'<h2 class="desk">{E(lab)}</h2><p>{E(note)}</p>'
    for f in fs:
        g=R[f];n+=1;out=f"img/{k}-{n:02d}.webp";save_img(J+f,"issues/"+out)
        urls=list(dict.fromkeys([g["source"]]+list(g.get("extra_sources") or [])))
        for u in urls: src.setdefault(u,g["title"])
        b+=figure(out,g["title"],f'{g["caption"]} [{g.get("label","Data")}. Data: {g["data_date"]}]',urls)
    w(k,lab,b)
w("sources","Sources",f'<h2 class="desk">Sources ({len(src)} links)</h2><p>All charts were drawn by TechVestVentures from the data linked below. Every figure is labelled by who claims it.</p><ul class="src">'+"".join(f'<li>{E(l)}: <a href="{E(u)}">{E(u)}</a></li>' for u,l in src.items())+"</ul>")
index(T,tabs,"Sections",cur="ukrcas");print(n,"charts",len(src),"sources",[t[0] for t in tabs])
