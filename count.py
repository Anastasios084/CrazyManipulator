import json
from collections import Counter


def count_field_in_json(obj, field):
    """Recursively count how many times `field` appears in the JSON object."""
    count = 0
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == field:
                count += 1
            count += count_field_in_json(value, field)
    elif isinstance(obj, list):
        for item in obj:
            count += count_field_in_json(item, field)
    return count

def collect_ids(obj, field):
    """Recursively collect all values for `field` in the JSON object."""
    ids = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == field:
                ids.append(value)
            ids.extend(collect_ids(value, field))
    elif isinstance(obj, list):
        for item in obj:
            ids.extend(collect_ids(item, field))
    return ids
# # Define the path to your text file
# file_path = 'crazytime3.json'  # Make sure this is the correct path
# new_file_path = "crazy3UTF8.json"

# # Read the original file in binary mode, then decode
# with open(file_path, 'rb') as original_file:
#     byte_content = original_file.read()  # Read the file as bytes
#     # Decode using 'utf-8' and replace errors to ensure valid JSON structure
#     content = byte_content.decode('utf-8', 'replace')

# # Write the content back to a new file in UTF-8 encoding
# with open(new_file_path, 'w', encoding='utf-8') as new_file:
#     new_file.write(content)

# print(f'File has been converted and saved as {new_file_path}')

file_path = "combined_data.json"
# Now, try to load the JSON from the new file
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)  # This should now work without errors

# print(json.dumps(json_data, indent=4))
count = count_field_in_json(json_data, "startedAt")
print(f'The field "{"startedAt"}" appears {count} times in the JSON file.')


# Use the function to collect all IDs from your JSON data
all_ids = collect_ids(json_data, "startedAt")

# Count how many times each ID appears
id_counts = Counter(all_ids)

# Now you can print out how many unique IDs there are and how many are duplicates
unique_ids = len(id_counts)
duplicates = sum(count > 1 for count in id_counts.values())

print(f'There are {unique_ids} unique IDs.')
print(f'There are {duplicates} IDs that appear more than once.')

# If you want to see the specific IDs that have duplicates and their counts
for id, count in id_counts.items():
    if count > 1:
        print(f'The ID "{id}" appears {count} times.')


