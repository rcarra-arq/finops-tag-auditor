![Python](https://img.shields.io/badge/Python-Script-3776AB)
![FinOps](https://img.shields.io/badge/FinOps-Tag_Governance-2ea44f)
![AWS](https://img.shields.io/badge/AWS-boto3-orange)


![Status](https://img.shields.io/badge/status-work_in_progress-yellow)

# FinOps Tag Auditor 

A small Python tool that scans cloud resources and flags the ones **missing
required cost-allocation tags** (`Project`, `Environment`, `Owner`). Untagged
resources are cost that can't be attributed to a team or project — one of the
first things a FinOps practitioner needs to fix.

> **Work in progress.** The tag-checking logic works against sample data.
> Reading real resources from AWS (read-only, via `boto3`) is the next step.

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

```bash
python auditor.py
```

## Roadmap

- [x] Core check: required tags per resource, one-line report
- [ ] Read real resources from AWS (`boto3`, dedicated read-only IAM identity)
- [ ] Summary counts (compliant vs. non-compliant)
- [ ] Configurable required-tag list

---

*Projeto de estudo e portfólio, construído passo a passo enquanto aprendo
Python e FinOps na prática.*
