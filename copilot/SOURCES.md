# Knowledge-base manifest

`type` = how the co-pilot should consume it.
**download** = pull a clean copy into `knowledge/` (stable, version-independent).
**fetch-live** = read on demand via web fetch (changes per version / frequently updated).

| Category | Source | URL | type | Notes / licence |
|---|---|---|---|---|
| 00 method-selection | Borshchev & Filippov — Reasons, Techniques, Tools | https://www.anylogic.com/resources/articles/from-system-dynamics-and-discrete-event-to-practical-agent-based-modeling-reasons-techniques-tools/ | download | Free, AnyLogic-hosted. The approach-choice paper. |
| 01 anylogic-core | AnyLogic Help (block reference, RL, Alpyne) | https://anylogic.help/ | fetch-live | Version-specific; do not freeze. |
| 01 anylogic-core | AnyLogic in 3 Days (free PDF) | https://www.anylogic.com/resources/books/free-simulation-book-and-modeling-tutorials/ | download | Free. |
| 01 anylogic-core | Big Book of Simulation Modeling (Borshchev) | https://www.anylogic.com/resources/books/ | download | Free chapters. Covers DES+ABM+SD. |
| 01 anylogic-core | Cloud model library (examples by industry) | https://cloud.anylogic.com/models | fetch-live | Dissect example models. |
| 02 statistics | NIST/SEMATECH e-Handbook of Statistical Methods | https://www.itl.nist.gov/div898/handbook/ | download | Free. Distributions + goodness-of-fit. |
| 02 statistics | fitdistrplus (R) | https://cran.r-project.org/package=fitdistrplus | fetch-live | MLE/MME + KS/AD/CvM fits. |
| 02 statistics | scipy.stats (Python) | https://docs.scipy.org/doc/scipy/reference/stats.html | fetch-live | Fitting in Python. |
| 03 supply-chain | Ivanov — Operations & Supply Chain Sim w/ AnyLogic (free) | https://www.anylogic.com/upload/pdf/Ivanov_AL_book_2017.pdf | download | Free, official. |
| 03 supply-chain | anyLogistix supply-chain guide (free) | https://www.anylogistix.com/resources/books/alx-textbook/ | download | Free PLE guide. |
| 04 manufacturing | AnyLogic job-shop tutorial | https://anylogic.help/tutorials/job-shop/ | fetch-live | Manufacturing DES. |
| 05 healthcare | DES in the ED — systematic review (open access) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5406177/ | download | Free. ED modeling framework. |
| 05 healthcare | DES in Healthcare — comprehensive review (IJERPH/MDPI) | search title (MDPI, open access) | download | Free. Efficiency-metric focus. |
| 06 ai-ml | AnyLogic AI / RL / Alpyne | https://www.anylogic.com/features/artificial-intelligence/ | fetch-live | RL experiment + Alpyne + Azure ML. |
| 06 ai-ml | FlexSim Reinforcement Learning docs | https://docs.flexsim.com/ (Reinforcement Learning) | fetch-live | Alternative tool; Gym + SB3. |
| 07 optimization | AnyLogic Optimization experiment / OptQuest | https://anylogic.help/ (Optimization) | fetch-live | Parameter optimisation. |
| 07 optimization | Winter Simulation Conference proceedings | https://informs-sim.org/ | fetch-live | Free tutorials: DES, ABM, sim-opt, input modeling. |
