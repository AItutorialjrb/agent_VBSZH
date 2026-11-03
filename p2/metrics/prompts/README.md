# Human prompts log
One CSV per run: `prompts/<run_id>.csv`, columns `utc,run_id,phase,class[task|decision|corrective-intervention|continue],assisted,verbatim_or_ref,note`.
Classes per handoff §2.3. Free-form prompts that are not the §7 standard prompt (+ decision answers) are `corrective-intervention` with a reason.
