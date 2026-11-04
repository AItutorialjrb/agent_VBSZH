# PROTOTYPE (G2-FIX option 2): parton-level (post-shower) fat-jet veto via a python UserHooks + SlowJet; measured 18 % pass, 0.0087 s/event on Q_4j LHE; cannot feed Delphes with stock tools (see reports/04 17.1). Edit LHEF path before use.
import pythia8, time, sys
class H(pythia8.UserHooks):
    def __init__(s):
        super().__init__(); s.sj=pythia8.SlowJet(-1,0.8,250.,2.4,2,2,None,False); s.n=0; s.acc=0
    def canVetoPartonLevel(s): return True
    def doVetoPartonLevel(s, ev):
        s.n+=1
        s.sj.analyze(ev)
        ok = s.sj.sizeJet()>=2
        if ok: s.acc+=1
        return not ok
h=H()
p=pythia8.Pythia("",False)
for l in ["Beams:frameType=4","Beams:LHEF=/tmp/rjiang/q4j.lhe","Random:setSeed=on","Random:seed=7","Next:numberCount=0","HadronLevel:all=on","PartonLevel:MPI=on"]: p.readString(l)
p.setUserHooksPtr(h); p.init()
t=time.time(); n=0
for i in range(1000):
    if not p.next():
        if p.infoPython().atEndOfFile(): break
        continue
    n+=1
print("hook calls",h.n,"accepted at parton level",h.acc,"events returned",n,"time",time.time()-t)
