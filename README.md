![Python](https://img.shields.io/badge/Python-Script-3776AB)
![FinOps](https://img.shields.io/badge/FinOps-Tag_Governance-2ea44f)
![AWS](https://img.shields.io/badge/AWS-boto3-orange)


![Status](https://img.shields.io/badge/status-work_in_progress-yellow)

# FinOps Tag Auditor 

A small Python tool that scans cloud resources and flags the ones **missing
required cost-allocation tags** (`Project`, `Environment`, `Owner`). Untagged
resources are cost that can't be attributed to a team or project — one of the
first things a FinOps practitioner needs to fix.

> **Work in progress.** Runs against built-in sample data by default, and can
> read real resources from AWS (read-only, via `boto3`) with `--source aws`.

## Motivation

This is the **enforcement** side of tagging. In my
[AWS high-availability project](https://github.com/rcarra-arq/aws-highly-available-webapp-terraform)
I *apply* standardized tags with Terraform; this tool *checks* that they
actually landed on every resource — including the tricky case of instances
launched at runtime by an Auto Scaling Group, which don't inherit the
provider's default tags. Same "trust, but verify" idea as my S3 backup verifier.

## What it does 

Given a list of resources and their tags, it reports which required tags are
missing, one line per resource:

```
OK    bucket-acervo-fotos
FALTA bucket-teste-antigo -> faltam: ['Project', 'Environment', 'Owner']
FALTA vol-do-servidor -> faltam: ['Owner']
```

## How to run

Install dependencies once:

```bash
pip install -r requirements.txt
```

Run against the built-in sample data (no AWS credentials needed):

```bash
python auditor.py
```

Run against your real AWS account (read-only):

```bash
python auditor.py --source aws
```

![First run against a real AWS account — 2 resources scanned, both flagged as missing the required tags](docs/screenshots/aws-audit-first-run.png)

### Exit codes

The tool is meant to run in a pipeline, so it signals its result via the exit code:

| Code | Meaning |
|------|---------|
| `0`  | All resources compliant |
| `1`  | Found resources missing required tags (a CI step can fail the build) |
| `2`  | The tool could not run (missing AWS permission or credentials) |

### AWS permissions

`--source aws` uses the Resource Groups Tagging API and needs a **dedicated
read-only identity** — not an operational user. The minimum policy it requires
is in [`docs/iam-policy.json`](docs/iam-policy.json). Read access to S3 alone is
*not* enough: listing tags is a separate permission (`tag:GetResources`).

## Roadmap

- [x] Core check: required tags per resource, one-line report
- [x] Read real resources from AWS (`boto3`, dedicated read-only IAM identity)
- [x] Summary counts (compliant vs. non-compliant)
- [x] CI-friendly exit codes
- [ ] Configurable required-tag list (flag / config file)
- [ ] Machine-readable output (`--format json|csv`)

---

*Projeto de estudo e portfólio, construído passo a passo enquanto aprendo
Python e FinOps na prática.*
