import json
import csv
import sys
import re
import os

# Paths relative to the script location (dataset/generate_dataset.py)
SKILLS_INDEX_PATH = "../skills_index.json"
CATALOG_PATH = "../CATALOG.md"
OUTPUT_CSV_PATH = "skills.csv"

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {path}: {e}", file=sys.stderr)
        sys.exit(1)

def parse_catalog(path):
    print(f"Parsing catalog from {path}...")
    triggers_map = {}
    tags_map = {}
    
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
            
        # Regex for catalog table rows
        # | Skill | Description | Tags | Triggers |
        # Example: | `angular` | Modern Angular... | angular | angular, v20... |
        row_regex = re.compile(r'\|\s*`([^`]+)`\s*\|\s*[^|]+\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|')

        for line in lines:
            match = row_regex.search(line)
            if match:
                skill_id = match.group(1).strip()
                # Split by comma and strip whitespace
                tags = [t.strip() for t in match.group(2).split(',') if t.strip()]
                triggers = [t.strip() for t in match.group(3).split(',') if t.strip()]
                
                tags_map[skill_id] = tags
                triggers_map[skill_id] = triggers
                
        return tags_map, triggers_map
        
    except FileNotFoundError:
        print(f"Error: File not found at {path}", file=sys.stderr)
        # return empty maps if catalog is missing, but warn
        return {}, {}

def main():
    print("Loading data...")
    skills_index = load_json(SKILLS_INDEX_PATH)
    catalog_tags, catalog_triggers = parse_catalog(CATALOG_PATH)
    
    rows = []
    
    print(f"Processing {len(skills_index)} skills...")
    for skill in skills_index:
        skill_id = skill.get('id', '')
        
        tags = catalog_tags.get(skill_id, [])
        triggers = catalog_triggers.get(skill_id, [])
        
        row = {
            'id': skill_id,
            'name': skill.get('name', ''),
            'description': skill.get('description', ''),
            'category': skill.get('category', 'uncategorized'),
            'risk': skill.get('risk', 'unknown'),
            'source': skill.get('source', 'unknown'),
            'path': skill.get('path', ''),
            'tags': ','.join(tags), 
            'triggers': ','.join(triggers)
        }
        rows.append(row)
        
    # Write CSV
    print(f"Writing {len(rows)} rows to {OUTPUT_CSV_PATH}...")
    headers = ['id', 'name', 'description', 'category', 'risk', 'source', 'path', 'tags', 'triggers']
    
    with open(OUTPUT_CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
        
    print("Done.")

if __name__ == "__main__":
    main()
