
import pandas as pd
import sys
from metrics import binary_auc
from sklearn.metrics import f1_score

def main(pred_path, label_path):
    preds = pd.read_csv(pred_path).sort_values("id")
    labels = pd.read_csv(label_path).sort_values("id")

    merged = labels.merge(preds, on="id", how="inner")
    if len(merged) != len(labels):
        raise ValueError("ID mismatch between predictions and labels")

    # score = binary_auc(merged["y_true"], merged["y_pred"])
    score = f1_score(merged["y_true"], merged["y_pred"], average='macro')
    print(f"SCORE={score:.8f}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
