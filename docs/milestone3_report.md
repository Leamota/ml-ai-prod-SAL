# Milestone 3 Report – ML & AI in Production  
**Team SAL (Ayah Jaber, Vincent Bender, Sebastian Rojas, Elizaveta Sorokina, Paul VanMetre)**  
**Project:** Transportation Ride-Sharing and Ride-Planning in Rural Areas  
**Date:** November 2025  

---

## 1️⃣ Offline Evaluation Specification (15 pts)

### Objective  
Evaluate the recommender model using standard offline metrics on a chronological split of user–item interactions.

### Implementation  
File → `recommender/evaluate_offline.py`  
- Split strategy : chronological (70 / 15 / 15 train-val-test).  
- Baseline : popularity-based top-K recommender.  
- Metrics : **HR@10** (hit ratio) and **NDCG@10** (normalized discounted cumulative gain).  
- Output → `results/offline_eval.json`

### Results  
| Metric | Value |
|---------|-------|
| HR@10 | **1.00** |
| NDCG@10 | **0.387** |

The baseline achieves perfect coverage (every test user saw at least one hit) and a moderate ranking quality (NDCG ≈ 0.39).

---

## 2️⃣ Online Evaluation – KPI Proxy (25 pts)

### Objective  
Simulate online user engagement by joining recommendation events with subsequent watch events.

### Implementation  
File → `recommender/evaluate_online.py`  
- Joins simulated `reco_responses` and `watch_events`.  
- Defines a recommendation as successful if the user watched the item **within 10 minutes** of exposure.  
- Outputs → `results/online_eval.json`

### Results  
| KPI | Value |
|-----|-------|
| Online KPI (success rate within 10 min) | **0.667** |

Approximately 67 % of recommended items were consumed promptly, indicating good short-term engagement potential.

---

## 3️⃣ Data Quality & Drift Analysis (20 pts)

### Objective  
Detect feature drift between baseline and current user distributions to ensure model reliability over time.

### Implementation  
File → `recommender/drift.py`  
- Uses **Wasserstein Distance** to measure distribution shifts.  
- Generates synthetic baseline/current data for demonstration.  
- Outputs → `results/drift_report.json`

### Results  
| Feature | Drift (Wasserstein) |
|----------|--------------------|
| age | **2.93** |
| activity_level | **3.15** |

Interpretation: Minor demographic shift (+3 years average age) and moderate behavior drift (activity level ≈ −2 points).

---

## 4️⃣ CI/CD Pipeline & Secrets Management (20 pts)

### Objective  
Implement automated testing, coverage enforcement, linting, container build, and deployment to Google Cloud Run.

### Implementation  
File → `.github/workflows/pipeline.yml`  
- Triggers on `push` and `pull_request` to `main`.  
- Steps → checkout → setup Python → install deps → run pytest + coverage (≥ 70 %) → lint → black → Docker build → push → deploy to Cloud Run.  
- Secrets stored securely in GitHub Actions:  
  - `GCLOUD_SERVICE_KEY` (secret)  
  - `GCLOUD_PROJECT`, `GCLOUD_REGION`, `ARTIFACT_REPO`, `IMAGE_NAME`, `SERVICE_NAME` (variables)  
- Prints deployed service URL after success.

### Outcome  
✅ All CI checks green on GitHub Actions  
✅ Coverage ≥ 70 %  
✅ Automated Cloud Run deployment confirmed  

---

## 5️⃣ Testing & Coverage Summary (10 pts)

- **Pytest Results:** 8 tests passed, 1 warning (safe)  
- **Coverage Threshold:** 70 % enforced via `coverage report --fail-under=70`  
- **Tools:** pytest-cov, flake8, black  

---

## 6️⃣ Lessons Learned & Next Steps (10 pts)

**Key Takeaways**
- Clear CI/CD design enables reproducible experiments and reliable deployments.  
- Offline metrics complement online KPI for a complete performance picture.  
- Drift detection is critical for long-term model stability and responsible AI monitoring.

**Next Steps**
- Integrate real Kafka event streams for live KPI tracking.  
- Extend drift analysis to multivariate features and alerting dashboards.  
- Deploy evaluation and drift modules as scheduled Cloud Run jobs.

---

### References  
- FAU Course Material – ML & AI in Production (2025)  
- Google Cloud Run Docs (2024)  
- Scipy & Pandas Documentation  

---

**Prepared by Ayah Jaber**  
_Milestone 3 Lead – Evaluation & Deployment_

