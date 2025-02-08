import pytrec_eval

# change these values accordingly
test_file = "scifact/qrels/test.tsv"
results_file = "results_title_and_text.txt"

def calculate_map():
  # Load qrels truth
  qrels = {}
  with open(test_file, "r") as f:
    next(f)  # Skip header if present
    for line in f:
      qid, docid, rel = line.strip().split()
      if qid not in qrels:
        qrels[qid] = {}
      qrels[qid][docid] = int(rel)

  # Load results 
  run = {}
  with open(results_file, "r") as f:
    next(f)  # Skip header
    for line in f:
      qid, _, docid, _, score, _ = line.strip().split()
      if qid not in run:
        run[qid] = {}
      run[qid][docid] = float(score)

  # Create evaluator
  evaluator = pytrec_eval.RelevanceEvaluator(qrels, {'map'})

  # Calculate scores
  results = evaluator.evaluate(run)

  # Calculate mean scores across all queries
  mean_scores = {}
  for metric in ['map']:
    mean_scores[metric] = sum(query_scores[metric] 
      for query_scores in results.values()) / len(results)

  print(f"Mean Average Precision (MAP): {mean_scores['map']:.4f}")

if __name__ == "__main__":
  calculate_map()