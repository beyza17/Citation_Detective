# Citation Detective - Node Classification

## 🎯 Challenge Overview
Investigating the Cora Network: Can you solve the mystery of the missing paper subjects?
Your score is determined by the **minimum per-class F1 score** - your worst-performing class defines your final rank!

![Cora Dataset](image.png)
## 📊 Dataset Information
The dataset was processed using the `Planetoid` library with the following graph properties:

* **Undirected:** True
* **Self-loops:** False
* **Isolated Nodes:** False
* **Total Training Nodes:** 640 
* **Training Label Rate:** 0.236
* **Total Testing Nodes:** 1,000
* **Total Node Features:** 1,433
* **Testing Label Rate:** 0.369

## 🏷️ Category Mapping
The dataset classifies papers into 7 distinct scientific fields:

| Index | Category Name       |
| :--- | :---               |
| 0    | Theory             |
| 1    | Reinforcement Learning |
| 2    | Genetic Algorithms |
| 3    | Neural Networks    |
| 4    | Probabilistic Methods |
| 5    | Case Based         |
| 6    | Rule Learning      |

----

## Class Distribution 
![alt text](image-1.png)
![alt text](image-2.png)

## Dataset Distribution

| Index | Category Name       | Training Set |            | Testing Set |            |
| :--- | :---               | :---: | :---: | :---: | :---: |
|       |                    | **Count** | **%** | **Count** | **%** |
| 0    | Theory             | 81    | 12.66% | 130   | 13.0% |
| 1    | Reinforcement Learning | 56  | 8.75%  | 91    | 9.1%  |
| 2    | Genetic Algorithms | 98    | 15.31% | 144   | 14.4% |
| 3    | Neural Networks    | 178   | 27.81% | 319   | 31.9% |
| 4    | Probabilistic Methods | 101 | 15.78% | 149   | 14.9% |
| 5    | Case Based         | 77    | 12.03% | 103   | 10.3% |
| 6    | Rule Learning      | 49    | 7.66%  | 64    | 6.4%  |
| **Total** | | **640** | **100%** | **1000** | **100%** |


---

## 1. Task Overview

**Task:** Node classification on a graph  
**Input:** Public graph structure and node features  
**Output:** Predictions for unseen test nodes  
**Metric:** f1 score (multi classification)

Participants train any GNN or non-GNN model *offline* and submit predictions
for the test nodes.

---

## 2. Repository Structure

```
.
├── data/
│   ├── public/
│   │   ├── train.csv # has labels in the last column
│   │   ├── test.csv
│   │   ├── test_nodes.csv
│   │   └── sample_submission.csv
│   └── private/
│       └── test_labels.csv   # never committed (used only in CI)
├── competition/
│   ├── config.yaml
│   ├── validate_submission.py
│   ├── evaluate.py
│   └── metrics.py
├── submissions/
│   ├── README.md
│   └── inbox/<team>/<run_id>/predictions.csv
├── leaderboard/
│   ├── leaderboard.csv
│   └── leaderboard.md
└── .github/workflows/
    ├── score_submission.yml
    └── publish_leaderboard.yml

```
## 3. Submission Format

Participants submit a **single CSV file**:

**predictions.csv**
```
id,y_pred
n0001,3
n0002,2
...
```

Rules:
- `id` must match exactly the IDs in `test_nodes.csv`
- One row per test node
- `y_pred` must be a float in [0,1]
- No missing or duplicate IDs

A sample is provided in:
```
data/public/sample_submission.csv
```

---

## 4. How to Submit

1. Fork this repository
2. Create a new folder:
```
submissions/inbox/<team_name>/<run_id>/
```
3. Add:
   - `predictions.csv`
   - `metadata.json`

Example `metadata.json`:
```json
{
  "team": "example_team",
  "model": "llm-only",
  "llm_name": "gpt-x",
  "notes": "Temporal GNN with class weighting"
}
```

4. Open a Pull Request to `main`

The PR will be **automatically scored** and the result posted as a comment.

---

## 5. 📊Leaderboard
View the interactive leaderboard here: [Leaderboard](https://beyza17.github.io/Citation_Detective/leaderboard.html)

After a PR is merged, the submission is added to:
- `leaderboard/leaderboard.csv`
- `leaderboard/leaderboard.md`

Rankings are sorted by **descending score**.




---

## 6. Rules

- No external or private data
- No manual labeling of test data
- No modification of evaluation scripts
- Unlimited offline training is allowed
- Only predictions are submitted

Violations may result in disqualification.

---

## 7. Human vs LLM Studies

To use this competition for research:
- Fix a time budget (e.g., 2 hours)
- Fix a submission budget (e.g., 5 runs)
- Record metadata fields (`model`, `llm_name`)
- Compare:
  - validity rate
  - best score within K submissions
  - score vs submission index

---



## 8. Baseline Performance (validation set)


- Min per-class F1: ~0.6

Your goal: Beat the baseline! 🎯


## 9. References
- Data: [Planetoid-Cora](https://pytorch-geometric.readthedocs.io/en/2.5.0/generated/torch_geometric.datasets.Planetoid.html)

😈Your worst class performance defines your score.

## 🤓 Have a nice work!
---

## 10. License

MIT License.


