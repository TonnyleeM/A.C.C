import textrazor
import json

# Your TextRazor API key
textrazor.api_key = "f6fa48ff4de6013859382ef3269f6bbe3901cd38832ea620f2295fbe"

# Load data from JSON files
def load_data(file_paths):
    combined_data = {}
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            combined_data.update(data)
    return combined_data

# Summarize text using the TextRazor API
def summarize_text(text):
    client = textrazor.TextRazor(extractors=["topics"])
    response = client.analyze(text)

    # Create a short paragraph summary
    summary = " ".join([topic.id for topic in response.topics()])
    return summary if summary else "No summary available."

# Main function to summarize data for specified countries
def summarize_countries(input_files, output_file):
    data = load_data(input_files)
    summaries = {}

    for country, text in data.items():
        summary = summarize_text(text)
        summaries[country] = summary
        print(f"Summary for {country}: {summary}")

    # Save summaries to a new JSON file
    with open(output_file, 'w') as json_file:
        json.dump(summaries, json_file, indent=4)

    print(f"Summaries saved to {output_file}")

# Specify the input and output JSON files
input_files = ['african_summaries.json', 'african_culture_summaries.json']
output_file = 'summarized_countries.json'

# Run the summarization
summarize_countries(input_files, output_file)