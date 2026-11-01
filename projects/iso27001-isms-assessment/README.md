# ISO/IEC 27001:2022 ISMS Assessment & Gap Analysis

**Team project, SMT Group training program**

A simulated advisory engagement assessing **XYZ Technologies**, a fictional payment-services company running Microsoft 365 and Azure with a hybrid workforce and PCI-DSS obligations, against **ISO/IEC 27001:2022**. We drafted the ISMS scope, built a risk register, ran a gap analysis across eight assessment domains, and wrote a prioritised 12-month remediation roadmap.

## Approach

1. **Context & scope:** stakeholder interviews (CISO, IT, SOC, HR, DevOps, Procurement) and a Clause 4.3 scope statement with in-scope systems and exclusions.
2. **Evidence review:** documentation review plus technical evidence (identity, vulnerability, configuration).
3. **Risk assessment:** qualitative 3×3 Impact × Likelihood matrix → Critical / High / Medium / Low, with treatment options (Mitigate / Transfer / Avoid / Accept), owners and deadlines.
4. **Gap analysis:** current state vs. ISO 27001 clauses and Annex A controls, NIST CSF and PCI-DSS.
5. **Roadmap:** phased plan to ISMS maturity and certification readiness.

## Key findings

| Finding | Status |
|---|---|
| ISMS scope document | ❌ Not defined |
| Security policies | ⚠️ Outdated (3+ years) |
| Risk management framework | ❌ Not documented |
| MFA on privileged accounts | ❌ Disabled for **22** accounts |
| Global administrators | ⚠️ **5** users |
| Inactive accounts | ❌ **14** still enabled |
| Critical vulnerabilities | ❌ **17** unpatched for 90+ days |
| Payment portal | ❌ Legacy TLS 1.0; outdated public-facing Apache |
| Incident response plan | ⚠️ Exists but never tested |
| Vendor risk management | ❌ No formal process |
| Privileged access | ❌ Shared admin accounts in use |

## Risk register (excerpt)

| Ref | Risk | Impact | Likelihood | Severity |
|---|---|---|---|---|
| RR-001 | MFA disabled on 22 privileged accounts | Critical | High | 🔴 Critical |
| RR-002 | 14 inactive accounts still enabled | High | High | 🔴 Critical |
| RR-004 | 17 critical vulnerabilities unpatched 90+ days | Critical | High | 🔴 Critical |
| RR-005 | Legacy TLS 1.0 on payment portal (PCI-DSS) | Critical | High | 🔴 Critical |
| RR-006 | Outdated Apache on public-facing server | Critical | High | 🔴 Critical |
| RR-003 | 5 users with Global Admin | High | Medium | 🟠 High |
| RR-009 | Developers pushing directly to production | High | Medium | 🟠 High |
| RR-011 | Shared admin accounts | High | Medium | 🟠 High |
| RR-013 | IR plan never tested | High | High | 🟠 High |
| RR-015 | No security steering committee | Medium | Medium | 🟡 Medium |

16 risks were registered in total.

## Remediation roadmap

| Phase | Timeline | Key actions |
|---|---|---|
| **1. Immediate response** | Weeks 1–4 | Enforce MFA on all privileged accounts, disable stale accounts, emergency patching (Critical SLA ≤ 7 days), disable TLS 1.0/1.1 |
| **2. Foundation building** | Months 1–3 | Approve ISMS scope, adopt an ISO 27005 risk methodology, refresh policies, steering committee, PAM, CI/CD change gates, vendor risk programme, IR tabletop exercise |
| **3. ISMS maturity** | Months 3–12 | Quarterly access reviews, security awareness and phishing simulations, tested backups (RTO/RPO), asset inventory (Annex A.5.9), internal audit → ISO 27001 certification |

## Deliverables

- [`reports/Remediation_Roadmap.pdf`](reports/Remediation_Roadmap.pdf): prioritised recommendations by domain, with remediation steps
- [`reports/Findings_to_Domains_Mapping.pdf`](reports/Findings_to_Domains_Mapping.pdf): findings mapped to the eight assessment domains

**Frameworks:** ISO/IEC 27001:2022 · ISO 27005 · NIST CSF · NIST SP 800-53 · PCI-DSS v4.0

*XYZ Technologies is a fictional organisation created for the training exercise.*
