import pandas as pd
import os

def save_summary_to_excel(game_title, positive_review, negative_review, recommended, not_recommended):
    """Save game summary to an Excel file, appending if the file already exists."""
    # Create a dictionary with the new data
    new_data = {
        'Game Title': [game_title],
        'Positive Review': [positive_review],
        'Negative Review': [negative_review],
        'Recommended': [recommended],
        'Not Recommended': [not_recommended]
    }

    new_df = pd.DataFrame(new_data)
    
    # Specify the file path
    output_file_path = r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Evaluation\game_summary_output.xlsx'
    
    if os.path.exists(output_file_path):
        # If the file exists, read the existing data
        existing_df = pd.read_excel(output_file_path)
        
        # Append the new data to the existing DataFrame
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        # If the file does not exist, use the new DataFrame as is
        updated_df = new_df

    # Save the updated DataFrame to the Excel file
    updated_df.to_excel(output_file_path, index=False)  # Save as Excel
    print(f"Summary saved to {output_file_path}")

# Example usage
# save_summary_to_excel("Example Game", "Great gameplay!", "Could be better.", 90, 10)
