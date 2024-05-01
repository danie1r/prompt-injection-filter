import json
from langkit import injections, extract

def examine():
    schema = injections.init()
    results = []
    with open('contains_results.json', 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            # Check if the target_field exists in the JSON data
            for elem in data['results']:
                result = extract({"prompt":elem['sentence']},schema=schema)
                if result['prompt.injection'] >= 0.5:
                    results.append({'score': result['prompt.injection'], 'sentence': elem['sentence'], 'domain': elem['domain']})
                    print(elem['sentence'])
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file")
    return results
result = examine()
data = {'results' : result}
with open('classify_results.json', 'w') as file:
    json.dump(data, file, indent=4)