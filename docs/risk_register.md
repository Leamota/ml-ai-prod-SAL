 # Risk Register

| ID | Risk Description                               | Likelihood (Low/Med/High) | Impact (Low/Med/High) | Mitigation Strategy                          |
|----|-----------------------------------------------|---------------------------|------------------------|----------------------------------------------|
| R1 | Kafka cluster misconfiguration                | Medium                    | High                   | Use predefined configs and automated tests    |
| R2 | Model training takes longer than expected     | High                      | Medium                 | Optimize data pipeline; use smaller subsets   |
| R3 | Cloud Run deployment fails                    | Medium                    | High                   | Keep rollback versions; test infra locally    |
| R4 | GitHub Actions CI/CD pipeline breaks          | Low                       | High                   | Add pipeline tests; document workflows        |
| R5 | Team communication delays                     | Medium                    | Medium                 | Weekly standups; Teams chat SLAs              |

