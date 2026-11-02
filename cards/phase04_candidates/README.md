# Phase 04 candidates — UNVALIDATED
`delphes_card_CMS_vbszh_v0.tcl`: stock LCG_110 CMS card + electron-before-photon overlap priority + slimmed TreeWriter
(see reports/03_generation_validation.md §4, decision D11). Must be validated (electron/photon efficiencies vs stock,
e->gamma rate, file size) before production. The Particle branch is kept here; the planned in-job skim
(reports/04_production_plan.md) computes generator overlap flags and drops it for most jobs.
