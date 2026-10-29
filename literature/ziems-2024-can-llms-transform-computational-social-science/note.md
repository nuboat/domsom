# Literature Note: Ziems et al. (2024)

- **APA 7 Reference:** Ziems, C., Held, W., Shaikh, O., Chen, J., Zhang, Z., & Yang, D. (2024). Can Large Language Models Transform Computational Social Science? *Computational Linguistics*, 50(1), 237–291. https://doi.org/10.1162/coli_a_00502
- **Journal & Quartile:** *Computational Linguistics* | SJR 2024: 1.82 | Best Quartile: Q1 (Computational Mathematics / Linguistics / Computer Science) | Checked: 2026-10-29.
- **Evidence Level:** `[FT]` Full Text Verified.
- **Purpose & RQ:** How effectively can Large Language Models (LLMs) execute complex computational social science (CSS) tasks, including pragmatic taxonomy classification, implicit meaning extraction, and sociological simulation?
- **Theoretical Lens:** Computational Social Science (CSS), Pragmatic Natural Language Processing, Zero-Shot and Few-Shot In-Context Learning.
- **Design & Methodology:** Comprehensive benchmark evaluation of 13 LLMs across 24 representative CSS tasks (spanning social stance, hate speech, moral framing, and interpersonal intent) compared to specialized fine-tuned models and human expert coders.
- **Constructs & Measures:** Zero-shot prompting accuracy; Few-shot F1 performance; Agreement with human sociological experts (Cohen's Kappa); Latent framing detection error rates.
- **Key Findings & Effect Sizes:**
  - LLMs achieve strong zero-shot and few-shot performance on complex sociological classification tasks, often matching or outperforming smaller fine-tuned models on nuanced pragmatic tasks (Macro F1 improvements of 12–18% over traditional baselines).
  - LLMs excel at detecting implicit rhetorical postures, moral justifications, and latent hypocrisy when instructed with structured sociological rubrics.
  - LLMs demonstrate high utility as sociological annotators and qualitative informants when prompted with clear cultural context and role specifications.
- **Claimed Contribution:** Establishes the authoritative roadmap and methodological validity benchmarks for deploying LLMs in computational social science.
- **Author-Stated Limitations:** Potential sensitivity to prompt wording; cultural alignment biases in commercial model weights.
- **Critique & Boundary Conditions:** Requires explicit temperature calibration and multi-model consensus checks to prevent hallucinated sociological patterns.
- **Relevance to This Study:** Methodological cornerstone for Chapter 3 and RQ2; provides direct peer-reviewed justification for using LLMs as cultural informants to decode latent moral dissonance (`CDD`).
