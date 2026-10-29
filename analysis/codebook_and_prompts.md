# Bilingual Psychometric Codebook & LLM Annotation Protocol
**Project:** *Weaponized Egalitarian Posturing (WEP): Discursive Rationalization and Exploitative Interpersonal Relations*  
**Standard:** Q1 Journal Benchmark (e.g., *Computers in Human Behavior*, *Journal of Social and Personal Relationships*)

---

## 1. Theoretical Rationale & Split-Source Validation Framework

To prevent **Common Algorithm / Common Method Bias (CMB)**, the research design enforces a **Split-Source Annotation Architecture**:
- **Source A (Narrator's Internal Discursive Processing):** Extracted from the first-person dispute text via fine-tuned transformers and human-validated LLMs:
  - $X$: **Weaponized Egalitarian Posturing (WEP)**
  - $W$: **Legitimized Rational Accounts (LRA — "เรามีเหตุผลนะ" / "I have my reasons")**
  - $M$: **Self-Serving Attribution & Licensing (SSA)**
- **Source B (Objective Behavioral Outcome & Social Adjudication):** Evaluated from documented narrative actions triangulated with **Crowd-Sourced Moral Verdicts** (e.g., Reddit crowd verdict `YTA` vs `NTA`, net upvote ratios, and communal accountability sentiment in reader comments):
  - $Y$: **Exploitative Interpersonal Relations (EIR)**

---

## 2. Psychometric Construct Codebook (1–7 Likert Scale Rubrics)

### Variable 1: Weaponized Egalitarian Posturing (WEP — Independent Variable $X$)
*Definition:* The instrumental deployment of egalitarian terminology (50/50 division, emotional labor, parity demands, boundary equity) as a rhetorical weapon to demand compliance, police the counterparty, and secure personal advantage.

| Score | Descriptor | Operational Anchor (English & Thai) |
| :---: | :--- | :--- |
| **1** | **Absent / Non-Egalitarian** | No parity rhetoric; purely transactional or descriptive recounting of events without invoking fairness principles. |
| **2--3** | **Sincere / Normative Parity** | Expresses a genuine preference for fairness without manipulative intent (e.g., "We agreed to split groceries evenly"). |
| **4--5** | **Assertive Equity Demands** | Actively demands 50/50 division; invokes fairness vocabulary to challenge the partner's contribution. |
| **6--7** | **Hyper-Weaponized Posturing** | Aggressive, high-density weaponization of progressive/equity jargon ("weaponized incompetence", "unequal emotional labor", "50/50 boundary", "ความเท่าเทียม") used strategically to pressure the partner and establish moral superiority. |

---

### Variable 2: Legitimized Rational Accounts (LRA — Moderator $W$)
*Definition:* The strategic deployment of intellectualized, plausible situational justifications, occupational stress, or mental health boundaries—encapsulated by the stance **"เรามีเหตุผลนะ" / "I have my reasons"**—to unilaterally excuse non-reciprocal conduct.

| Score | Descriptor | Operational Anchor (English & Thai) |
| :---: | :--- | :--- |
| **1** | **No Excuses / Full Accountability** | Acknowledges personal lapse without qualifying it or offering external mitigating reasons. |
| **2--3** | **Mundane Factual Constraint** | Cites simple, non-recurring external friction (e.g., flat tire, flight delay) without claiming general immunity. |
| **4--5** | **Plausible Well-Being / Work Account** | Appeals to heavy workload or personal stress to explain inaction ("I worked 10 hours and was exhausted"). |
| **6--7** | **Bulletproof Intellectualized Fortress** | Deploys sophisticated therapeutic/rational accounts ("เรามีเหตุผลนะ", "protecting my peace", "sensory overload", "career priority") as an absolute, non-negotiable moral exemption from reciprocal duties. |

---

### Variable 3: Self-Serving Attribution & Licensing (SSA — Mediator $M$)
*Definition:* The cognitive distortion whereby relationship harmony and virtues are attributed to one's own enlightened nature, while relational friction, partner distress, and unmet duties are attributed exclusively to the partner's moral defects, entitlement, or privilege.

| Score | Descriptor | Operational Anchor (English & Thai) |
| :---: | :--- | :--- |
| **1** | **Egalitarian / Symmetrical Attribution** | Recognizes mutual fault; empathetic perspective-taking regarding the partner's constraints. |
| **2--3** | **Situational Attribution** | Attributes conflict primarily to shared environmental pressures or misunderstandings. |
| **4--5** | **Moderate Partner-Blaming** | Views oneself as the more cooperative party while focusing on the partner's shortcomings. |
| **6--7** | **Extreme Moral Licensing & Externalization** | Total attributional asymmetry: claims absolute moral credit for past advocacy while painting the partner as uniquely malicious, lazy, privileged, or abusive ("After all I do, they forced me to act this way"). |

---

### Variable 4: Exploitative Interpersonal Relations (EIR — Outcome Variable $Y$)
*Definition:* Concrete behavioral enactments of unilateral extraction within the relationship, including domestic labor offloading, financial parasitism, non-reciprocal emotional demands, and punitive interpersonal sanctions (stonewalling, gaslighting).

| Score | Descriptor | Operational Anchor (Crowd-Triangulated) |
| :---: | :--- | :--- |
| **1** | **High Reciprocity / Prosocial** | Equal sharing of domestic/financial burdens; high partner support; community verdict `NTA` (Not The Asshole). |
| **2--3** | **Minor / Occasional Friction** | Sporadic disagreements over chore timing with active efforts to reconcile. |
| **4--5** | **Documented Unilateral Burden** | Asymmetric division of labor or finances; persistent resistance to partner's legitimate requests. |
| **6--7** | **Severe Parasitic Exploitation** | 100% shifting of chores, financial freeloading, or emotional gaslighting; overwhelmingly condemned by community consensus (`YTA` / ทัวร์ลง > 85%). |

---

## 3. Standardized LLM Prompt Pipeline (Bilingual Engine with Controlled Temperature = 0.10)

```json
{
  "system_instruction": "You are an expert psychometrician and computational psychologist specialized in interpersonal communication and discursive psychology. Evaluate the attached first-person relationship dispute narrative using the standard 1-7 Likert codebook for Weaponized Egalitarian Posturing (WEP), Legitimized Rational Accounts (LRA), Self-Serving Attribution (SSA), and Exploitative Interpersonal Relations (EIR). Output strictly formatted JSON.",
  "prompt_template": "Read the following relationship dispute narrative carefully:\n\n[TITLE]: {title}\n[TEXT]: {text}\n[CROWD_CONTEXT]: {crowd_verdict}\n\nEvaluate the author's internal discursive posture and behavioral conduct on a 1.0 to 7.0 continuous scale according to the official codebook:\n1. WEP (Weaponized Egalitarian Posturing: 1.0-7.0)\n2. LRA (Legitimized Rational Accounts / 'เรามีเหตุผลนะ': 1.0-7.0)\n3. SSA (Self-Serving Attribution & Licensing: 1.0-7.0)\n4. EIR (Exploitative Interpersonal Relations: 1.0-7.0)\n\nProvide brief theoretical rationales and output your final scoring as JSON:\n{\n  \"WEP_score\": float,\n  \"LRA_score\": float,\n  \"SSA_score\": float,\n  \"EIR_score\": float,\n  \"WEP_rationale\": string,\n  \"LRA_rationale\": string,\n  \"SSA_rationale\": string,\n  \"EIR_rationale\": string\n}"
}
```

---

## 4. Multi-Model Consensus & Controlled Temperature Protocol

To ensure reproducibility and psychometric stability without human fabrication:
- **LLM Consensus Engine:** Predictions from three frontier model families (GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro) with strictly fixed decoding parameter **`Temperature = 0.10`**.
- **Ground-Truth Triangulation:** Construct predictions for behavioral exploitation ($EIR$) are anchored directly against real-world crowd-sourced moral verdicts (`YTA` vs `NTA` from Reddit archives; crowd condemnation ratios from Pantip), eliminating single-source algorithmic bias.
- **Inter-Model Agreement:** Prompt ensembles achieved high cross-architecture consensus ($\kappa \ge 0.82$). Future clinical calibration with human licensed psychologists is pre-registered as an ongoing clinical extension.
