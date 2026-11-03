#!/usr/bin/env python3
"""Patch SubProcesses/cuts.f of an MG5 v3.6.3 process dir (usage: patch_cuts_vbs.py <proc_dir>/SubProcesses/cuts.f).
Replaces the stock WBF cut (acts on the two HARDEST jets, useless for boosted-H topologies where the hardest jets are the Higgs-jets)
by an ANY-PAIR VBS filter: event passes iff there EXISTS a pair of final-state jets/b (is_a_j or is_a_b) with
   y1*y2 < 0, |y1-y2| > DELTAETA (run_card), m_jj > XETAMIN (run_card, REPURPOSED as an m_jj threshold in GeV).
Events with < 2 jets bypass (as stock).  Rationale: patches/003.  Idempotent; aborts if the stock block is not found exactly once."""
import sys, re
f = sys.argv[1]; s = open(f).read()
if "VBSANYPAIR" in s: print("already patched"); sys.exit(0)
a = s.index("C-- FIND THE HARDEST JETS"); b = s.index("c Begin photon isolation")
assert s.count("C-- FIND THE HARDEST JETS") == 1 and a < b
new = """C-- VBSANYPAIR (hh patch 003): exist jet pair with y1*y2<0, |dy|>DELTAETA, mjj>XETAMIN(GeV)
            ptmax1=0d0
            ptmax2=0d0
            hardj2=0
            do i=nincoming+1,nexternal
               if(is_a_j(i).or.is_a_b(i)) hardj2=hardj2+1
            enddo
            if (hardj2.lt.2) goto 21 ! bypass: not enough jets
            do hardj1=nincoming+1,nexternal-1
               if(.not.(is_a_j(hardj1).or.is_a_b(hardj1))) cycle
               do i=hardj1+1,nexternal
                  if(.not.(is_a_j(i).or.is_a_b(i))) cycle
                  if (rap(p(0,hardj1))*rap(p(0,i)) .ge. 0d0) cycle
                  if (abs(rap(p(0,hardj1))-rap(p(0,i))) .le. deltaeta) cycle
                  ptmax2=(p(0,hardj1)+p(0,i))**2-(p(1,hardj1)+p(1,i))**2
     &                  -(p(2,hardj1)+p(2,i))**2-(p(3,hardj1)+p(3,i))**2
                  if (ptmax2 .lt. xetamin**2) cycle
                  ptmax1=1d0
               enddo
            enddo
            if (ptmax1.lt.0.5d0) then
               passcuts=.false.
               return
            endif
         ENDIF

"""
s = s[:a] + new + s[b:]; open(f, "w").write(s); print("patched", f)
