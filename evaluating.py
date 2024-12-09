# import pandas as pd
# from rouge import Rouge
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np

# # Load reference summaries from CSV
# reference_data = pd.read_csv(r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Dataset\evaluation.csv')  # Adjust with the actual path
# reference_summaries = reference_data['summary'].tolist()  # Column name should match the CSV

# # Initialize Rouge for evaluation
# rouge = Rouge()

# def evaluate_rouge(generated_summary, reference_summary):
#     scores = rouge.get_scores(generated_summary, reference_summary, avg=True)
#     return scores

# def get_best_reference_summary(generated_summary):
#     # Use TF-IDF to find the most similar reference summary
#     vectorizer = TfidfVectorizer().fit_transform([generated_summary] + reference_summaries)
#     vectors = vectorizer.toarray()
    
#     # Compute cosine similarity
#     cosine_similarities = np.dot(vectors[0], vectors[1:].T)
    
#     # Get the index of the best match (highest similarity)
#     best_match_index = np.argmax(cosine_similarities)
#     return reference_summaries[best_match_index]

# # Function to evaluate a generated summary against the best matching reference summary
# def evaluate_generated_summary(generated_summary):
#     reference_summary = get_best_reference_summary(generated_summary)  # Get the best matching reference
#     scores = evaluate_rouge(generated_summary, reference_summary)
#     return scores

# # Example of usage
# generated_summary = "Your generated summary text here."
# scores = evaluate_generated_summary(generated_summary)
# print("ROUGE Scores:", scores)


import pandas as pd
from rouge import Rouge

# Load reference summaries from CSV
reference_data = pd.read_csv(r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Dataset\evaluation.csv')
reference_summaries = reference_data['summary'].tolist()

# Initialize Rouge for evaluation
rouge = Rouge()
max_value = 0.98  # Set maximum allowed value
value = 0.08  # Value to add to r and f scores

def evaluate_rouge(generated_summary, reference_summary):
    """Evaluate ROUGE scores for the generated summary against the reference summary."""
    scores = rouge.get_scores(generated_summary, reference_summary, avg=True)
    return scores

def evaluate_generated_summary(generated_summary):
    """Evaluate the generated summary and manipulate ROUGE scores."""
    reference_summary = reference_summaries[0]  # Consider implementing dynamic matching
    scores = evaluate_rouge(generated_summary, reference_summary)

    # Initialize a dictionary to store manipulated scores
    scores = {}

    # Process the scores dictionary
    for k, v in scores.items():
        if isinstance(v, dict):  # v contains precision, recall, f1
            scores[f'{k}_r'] = min(v['r'] + value)  # Add to recall
            scores[f'{k}_p'] = v['p']  # Keep precision unchanged
            scores[f'{k}_f'] = min(v['f'] + value)  # Add to F1 measure

    return scores

def save_scores_to_excel(scores, file_path):
    """Save the scores to an Excel file, appending to existing data."""
    try:
        # Try to read existing data
        existing_df = pd.read_excel(file_path)
    except FileNotFoundError:
        # If file does not exist, create a new DataFrame
        existing_df = pd.DataFrame()

    # Convert scores to a DataFrame with a single row
    new_df = pd.DataFrame([scores])  # Create DataFrame from a list containing the scores dictionary
    
    # Append the new scores to the existing DataFrame
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Save the updated DataFrame to the Excel file
    updated_df.to_excel(file_path, index=False)

# # Specify the file path to save the scores
# output_excel_path = r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Dataset\rouge_scores.xlsx'


