#!/usr/bin/env python3
"""LHE-level I/S for the EW x QCD interference (G2 item 8): sigma_I (signed, gridpack) x fraction of parton-level VBS events (m_jj>500, |dy_jj|>2.5, signed weights, bootstrap error) divided by the same for the EW signal (undecayed W+H, W- smoke LHE). VALIDATION number, not a yield."""
import gzip,math,glob,numpy as np,json
def load(f):
    W=[];P=[];ev=None
    for l in gzip.open(f,"rt"):
        if l.startswith("<event>"): ev=[];first=True;continue
        if l.startswith("</event>"):
            W.append(w0);P.append([e for e in ev if e[5]==1 and (abs(e[4])<=5 or e[4]==21)][:2]);ev=None;continue
        if ev is None: continue
        if first: w0=float(l.split()[2]);first=False;continue
        x=l.split()
        if len(x)>=13: ev.append((float(x[6]),float(x[7]),float(x[8]),float(x[9]),int(x[0]),int(x[1])))
    return np.array(W),P
def vbs(p):
    if len(p)<2: return False
    s=[p[0][i]+p[1][i] for i in range(4)]; m=math.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2,0))
    y=lambda q:0.5*math.log((q[3]+q[2])/(q[3]-q[2]))
    return m>500 and abs(y(p[0])-y(p[1]))>2.5
WH="/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; rs={}
for tag,fs in (("I",glob.glob(f"{WH}/work/test/I_WHjj/*[0-9].lhe.gz")),("S",glob.glob(f"{WH}/work/smoke/w[pm]_light_nodec/*.lhe.gz"))):
    W=[];P=[]
    for f in fs: w,p=load(f);W+=list(w);P+=p
    W=np.array(W);m=np.array([vbs(p) for p in P]);f=(W*m).sum()/W.sum();rng=np.random.default_rng(1);bs=[]
    for _ in range(500):
        i=rng.integers(0,len(W),len(W));bs.append((W[i]*m[i]).sum()/W[i].sum())
    rs[tag]=(f,float(np.std(bs)),len(W),float((W>0).mean()))
sI=-0.2503; sS=38.4+23.66; fI,eI,nI,pI=rs["I"];fS,eS,nS,pS=rs["S"]
r_vbs=sI*fI/(sS*fS); err=abs(r_vbs)*math.sqrt((eI/fI)**2+(eS/fS)**2+(0.0042/0.2503)**2) if fI else None
out=dict(sigma_I_fb=sI,sigma_S_undecayed_fb=sS,I_over_S_inclusive=sI/sS,I_over_S_parton_VBS=r_vbs,err=err,frac_VBS_I=rs["I"],frac_VBS_S=rs["S"],note="LHE-level validation numbers (parton m_jj>500,|dy|>2.5; W,H undecayed); not a yield")
json.dump(out,open(f"{WH}/work/I_over_S.json","w"),indent=1);print(out)
