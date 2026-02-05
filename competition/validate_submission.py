import pandas as pd
import sys

def main(pred_path, test_nodes_path):
    preds = pd.read_csv(pred_path)
    test_nodes = pd.read_csv(test_nodes_path)

    if "id" not in preds.columns or "y_pred" not in preds.columns:
        raise ValueError("predictions.csv must contain id and y_pred")

    if preds["id"].duplicated().any():
        raise ValueError("Duplicate IDs found")

    if preds["y_pred"].isna().any():
        raise ValueError("NaN predictions found")

    # --- UPDATED SECTION ---
    # Define your valid labels (e.g., 0, 1, 2, 3, 4, 5, 6)
    valid_labels = set(range(7)) 
    
    # Check if all predictions are within the set of valid integer labels
    if not set(preds["y_pred"]).issubset(valid_labels):
        invalid_vals = set(preds["y_pred"]) - valid_labels
        raise ValueError(f"Invalid predictions found: {invalid_vals}. Must be integers between 0 and 6.")
    # ------------------------

    if set(preds["id"]) != set(test_nodes["id"]):
        raise ValueError("Prediction IDs do not match test nodes")

    print("VALID SUBMISSION")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])