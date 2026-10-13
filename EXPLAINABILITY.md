# Explainability

## Inputs
The agent accepts heritage asset records with supplied condition, significance, exposure, and urgency scores, optional weights, and documentation or consultation metadata.

## Decision
It validates score ranges, normalizes non-negative weights, calculates a weighted priority indicator, and highlights records with high urgency or missing documentation.

## Limits
It does not authenticate objects, independently determine significance, establish title or ownership, verify site facts, or prescribe conservation treatment. Results depend on supplied records and assessor judgments.

## Tool: validate-heritage-records

### Inputs and Data Sources
A list of user-supplied heritage asset records.

### Decision and Reasoning
Checks unique IDs, required numeric scores, score ranges, and optional metadata types.

### Outputs and Evidence
Returns validation errors, warnings, and valid asset IDs.

### Limits and Constraints
It cannot confirm authenticity, provenance, ownership, or the accuracy of condition observations.

### Failure Handling
Invalid records are reported and excluded from scoring.

### Human Review
Confirm records with authorized custodians, conservators, and relevant community representatives.

## Tool: assess-preservation-priorities

### Inputs and Data Sources
Validated records and optional user-supplied weights.

### Decision and Reasoning
Computes a weighted average of the four explicitly supplied 0–100 indicators and flags high urgency.

### Outputs and Evidence
Returns scores, component values, weights, and priority labels.

### Limits and Constraints
A score is not an independent cultural-value assessment or treatment recommendation.

### Failure Handling
Invalid weights or records return structured errors.

### Human Review
Review priorities with qualified conservators and relevant communities, accounting for local context and protocols.

## Tool: build-preservation-plan

### Inputs and Data Sources
Heritage asset records and optional weights.

### Decision and Reasoning
Combines validation, priority scores, missing-evidence flags, and non-invasive next steps.

### Outputs and Evidence
Produces a JSON-compatible planning report with limitations and review actions.

### Limits and Constraints
It does not prescribe physical intervention, certify legal compliance, or decide access to culturally sensitive information.

### Failure Handling
Missing information remains explicit rather than silently filled.

### Human Review
Obtain required permissions, consultation, and qualified conservation review before implementing any action.
