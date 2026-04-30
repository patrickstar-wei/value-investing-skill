# /source-check

Audit all numerical data sources used in the current investment analysis.

Output:

- Source Annotation Table
- Model Input Source Table (audit / appendix only)
- Derived Metric Table (audit / appendix only)
- Unverified / Assumption Table
- Conflicting source list
- Whether valuation can proceed

Example:

```text
/source-check TSLA
/source-check GOOGL --model reverse-dcf
```
