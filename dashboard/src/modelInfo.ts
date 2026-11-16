// Single source of truth for the "Model results" page.
// Numbers come from the held-out test set. Update this file after every retrain.
export const MODEL_INFO = {
  algorithm: "XGBoost (gradient-boosted decision trees) with calibrated probabilities",
  featureCount: 40,
  testCarts: 630_303,
  baseRate: 72.61, // percent of test carts that were abandoned
  metrics: { accuracy: 74.43, precision: 75.69, recall: 95.42, f1: 84.42, rocAuc: 70.85, prAuc: 86.11 },
  // Scores of a model that simply says "abandoned" for every cart
  baseline: { accuracy: 72.61, precision: 72.61, f1: 84.13, rocAuc: 50, prAuc: 72.61 },
  // ROC-AUC on each data split
  fit: { train: 72.81, validation: 70.93, test: 70.85 },
  bands: [
    { key: "High", label: "High risk", carts: 170_457, abandoned: 88.6 },
    { key: "Medium", label: "Medium risk", carts: 214_808, abandoned: 77.1 },
    { key: "Low", label: "Lower risk", carts: 245_038, abandoned: 57.5 },
  ],
};