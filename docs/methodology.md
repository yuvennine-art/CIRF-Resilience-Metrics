# Methodology

## Event mapping
CIRF expects canonical events to be present in logs:
- `attack_start`: the moment the hostile action begins
- `compromise`: the first confirmed loss of confidentiality/integrity/availability
- `detection`: first detection event (from IDS/SIEM/etc.)
- `restored`: service restored / recovery achieved

## Metrics
- **MTTC** (time to compromise): compromise − attack_start
- **MTTD** (time to detect): detection − attack_start
- **MTTR** (time to restore): restored − compromise
- **NRI**: area under the normalised service curve (0..1) divided by total duration
- **MLS**: minimum of the normalised service level
- **DR**: disruption ratio = 1 − mean(normalised service)

## Handling censored data
If an event is missing, the corresponding metric is marked as `NR` (not recorded). NRI/MLS/DR are still computed
from the available service curve.

## Aggregation
For repeated runs of the same configuration, CIRF aggregates metrics as mean ± standard deviation. No formal
significance testing is included in this reference implementation.
