import pandas as pd

# Define a mapping of keywords to icons and colors - with unique icons for each type
icon_mapping = {
    # Programming Languages
    'Python': {'icon': 'logos:python', 'color': '4B8BBE'},
    'Java': {'icon': 'logos:java', 'color': 'F89820'},
    'JavaScript': {'icon': 'logos:javascript', 'color': 'F7DF1E'},
    'HTML': {'icon': 'logos:html-5', 'color': 'E34F26'},
    'CSS': {'icon': 'logos:css-3', 'color': '1572B6'},
    'SQL': {'icon': 'vscode-icons:file-type-sql', 'color': '00758F'},
    
    # Development concepts
    'Web': {'icon': 'carbon:web-services', 'color': '42A5F5'},
    'API': {'icon': 'carbon:api', 'color': '7E57C2'},
    'Database': {'icon': 'carbon:database', 'color': '26A69A'},
    'Network': {'icon': 'carbon:network', 'color': 'FF7043'},
    'Cloud': {'icon': 'carbon:cloud', 'color': '29B6F6'},
    'Server': {'icon': 'carbon:bare-metal-server', 'color': 'EC407A'},
    
    # Software Engineering
    'Testing': {'icon': 'carbon:test', 'color': '66BB6A'},
    'Debug': {'icon': 'carbon:debug', 'color': 'FFA726'},
    'Code': {'icon': 'carbon:code', 'color': '5C6BC0'},
    'Git': {'icon': 'logos:git', 'color': 'F05032'},
    'Algorithm': {'icon': 'carbon:flow', 'color': '9575CD'},
    'Data Structure': {'icon': 'carbon:data-structured', 'color': '4DB6AC'},
    
    # System & Architecture
    'Operating System': {'icon': 'carbon:terminal', 'color': '78909C'},
    'Architecture': {'icon': 'carbon:infrastructure', 'color': '8D6E63'},
    'System': {'icon': 'carbon:system', 'color': 'BA68C8'},
    'Hardware': {'icon': 'carbon:hardware', 'color': 'F06292'},
    'Software': {'icon': 'carbon:software', 'color': '4FC3F7'},
    'Memory': {'icon': 'carbon:chip', 'color': 'FFB74D'},
    
    # Data Science & Analytics
    'Data': {'icon': 'carbon:data-vis-1', 'color': '4DD0E1'},
    'Analytics': {'icon': 'carbon:chart-line', 'color': 'FF8A65'},
    'Statistics': {'icon': 'carbon:chart-histogram', 'color': '81C784'},
    'Machine Learning': {'icon': 'carbon:machine-learning', 'color': 'AB47BC'},
    'AI': {'icon': 'carbon:ai-status', 'color': '7986CB'},
    'Visualization': {'icon': 'carbon:chart-bubble', 'color': '4DB6AC'},
    
    # IoT & Embedded
    'IoT': {'icon': 'carbon:iot-platform', 'color': 'FF7043'},
    'Embedded': {'icon': 'carbon:chip', 'color': '9575CD'},
    'Sensors': {'icon': 'carbon:sensor', 'color': '4DB6AC'},
    'Microcontroller': {'icon': 'carbon:microservices', 'color': '7E57C2'},
    
    # Research & Innovation
    'Research': {'icon': 'carbon:research', 'color': '00ACC1'},
    'Innovation': {'icon': 'carbon:idea', 'color': '26C6DA'},
    'Study': {'icon': 'carbon:study', 'color': '4DD0E1'},
    'Investigation': {'icon': 'carbon:search', 'color': '80DEEA'},
    'Analysis': {'icon': 'carbon:analytics-reference', 'color': 'B2EBF2'},
    'Experiment': {'icon': 'carbon:chemistry', 'color': '84FFFF'},
    
    # Project & Professional
    'Project': {'icon': 'carbon:task', 'color': 'FFB74D'},
    'Management': {'icon': 'carbon:task-complete', 'color': 'FFA726'},
    'Professional': {'icon': 'carbon:user-profile', 'color': 'FF9800'},
    'Business': {'icon': 'carbon:analytics', 'color': 'FB8C00'},
    'Enterprise': {'icon': 'carbon:enterprise', 'color': 'F57C00'},
    'Industry': {'icon': 'carbon:industry', 'color': 'EF6C00'},
    'Skills': {'icon': 'carbon:skill-level', 'color': 'E65100'},
    
    # Software Engineering specific
    'Programming Fundamentals': {'icon': 'carbon:code', 'color': '9575CD'},
    'Software Engineering': {'icon': 'carbon:application-web', 'color': '7E57C2'},
    'Development Process': {'icon': 'carbon:delivery', 'color': '673AB7'},
    
    # Computing & Desktop alternatives
    'Computing': {'icon': 'carbon:laptop', 'color': '42A5F5'},
    'Computer': {'icon': 'carbon:computer', 'color': '1E88E5'},
    'Desktop': {'icon': 'carbon:screen', 'color': '1976D2'},
    'Workstation': {'icon': 'carbon:development', 'color': '1565C0'},
    'Terminal': {'icon': 'carbon:terminal', 'color': '0D47A1'},
    'Command Line': {'icon': 'carbon:terminal-3270', 'color': '0277BD'},
    'Shell': {'icon': 'carbon:ibm-cloud-shell', 'color': '01579B'},
    
    # Additional Computing concepts with varied icons
    'Computing Systems': {'icon': 'carbon:devices', 'color': '0288D1'},
    'Computer Architecture': {'icon': 'carbon:bare-metal-server', 'color': '039BE5'},
    'Operating System': {'icon': 'carbon:virtual-machine', 'color': '03A9F4'},
    'System Software': {'icon': 'carbon:software-resource', 'color': '29B6F6'},
    'Computer Hardware': {'icon': 'carbon:hardware-security-module', 'color': '4FC3F7'},
    'Computer Network': {'icon': 'carbon:network-4', 'color': '81D4FA'},
    
    # Default (fallback)
    'default': {'icon': 'carbon:education', 'color': '78909C'}
}

# Default education-related icons for variety
education_icons = [
    {'icon': 'carbon:education', 'color': '78909C'},
    {'icon': 'carbon:book', 'color': '607D8B'},
    {'icon': 'carbon:course', 'color': '546E7A'},
    {'icon': 'carbon:study-next', 'color': '455A64'},
    {'icon': 'carbon:learning', 'color': '37474F'},
    {'icon': 'carbon:notebook', 'color': '263238'},
    {'icon': 'carbon:document', 'color': '78909C'},
    {'icon': 'carbon:catalog', 'color': '607D8B'},
    {'icon': 'carbon:workspace', 'color': '546E7A'},
    {'icon': 'carbon:cognitive', 'color': '37474F'},
    {'icon': 'carbon:concept', 'color': '263238'},
    {'icon': 'carbon:skill-level-basic', 'color': '78909C'},
    {'icon': 'carbon:skill-level-intermediate', 'color': '607D8B'},
    {'icon': 'carbon:skill-level-advanced', 'color': '546E7A'},
    {'icon': 'carbon:report', 'color': '455A64'},
    {'icon': 'carbon:data-base', 'color': '37474F'},
    {'icon': 'carbon:assembly-cluster', 'color': '263238'},
    {'icon': 'carbon:assembly', 'color': '78909C'},
    {'icon': 'carbon:template', 'color': '607D8B'},
    {'icon': 'carbon:certificate', 'color': '546E7A'},
    {'icon': 'carbon:portfolio', 'color': '455A64'},
    {'icon': 'carbon:presentation-file', 'color': '37474F'},
    {'icon': 'carbon:lecture', 'color': '263238'},
    {'icon': 'carbon:group-presentation', 'color': '78909C'},
    {'icon': 'carbon:forum', 'color': '607D8B'}
]

def get_icon_and_color(title, aim):
    """Determine the most appropriate icon and color based on module title and aim."""
    title_words = set(title.lower().split())
    aim_words = set(aim.lower().split())
    all_words = title_words.union(aim_words)
    
    # Track used icons to ensure uniqueness
    used_icons = set()
    
    # First try exact matches in title
    for keyword in icon_mapping:
        if keyword.lower() in title.lower():
            icon_color = icon_mapping[keyword]
            if icon_color['icon'] not in used_icons:
                used_icons.add(icon_color['icon'])
                return icon_color
    
    # Then try matches in all words
    for keyword in icon_mapping:
        if keyword.lower() in ' '.join(all_words):
            icon_color = icon_mapping[keyword]
            if icon_color['icon'] not in used_icons:
                used_icons.add(icon_color['icon'])
                return icon_color
    
    # If no match found, try to make an educated guess based on common words
    common_words = {
        'system': icon_mapping['Computing Systems'],
        'computer': icon_mapping['Computer'],
        'computing': icon_mapping['Computing'],
        'desktop': icon_mapping['Desktop'],
        'workstation': icon_mapping['Workstation'],
        'terminal': icon_mapping['Terminal'],
        'shell': icon_mapping['Shell'],
        'command': icon_mapping['Command Line'],
        'operating': icon_mapping['Operating System'],
        'architecture': icon_mapping['Computer Architecture'],
        'hardware': icon_mapping['Computer Hardware'],
        'network': icon_mapping['Computer Network'],
        
        # Keep other existing mappings
        'application': icon_mapping['Software'],
        'framework': icon_mapping['API'],
        'tool': icon_mapping['Code'],
        'method': icon_mapping['Algorithm'],
        'principle': icon_mapping['Data Structure'],
        'fundamental': icon_mapping['Data'],
        'introduction': icon_mapping['Study'],
        'advanced': icon_mapping['Machine Learning'],
        'practical': icon_mapping['Code'],
        'theory': icon_mapping['Data Structure'],
        'laboratory': icon_mapping['Experiment'],
        'workshop': icon_mapping['Code'],
        'computation': icon_mapping['Data'],
        'interface': icon_mapping['API'],
        'scripting': icon_mapping['Code'],
        'engineering': icon_mapping['Software Engineering']
    }
    
    for word, mapping in common_words.items():
        if word in ' '.join(all_words):
            if mapping['icon'] not in used_icons:
                used_icons.add(mapping['icon'])
                return mapping
    
    return icon_mapping['default']

def update_csv_icons(filename):
    """Update icons and colors in a CSV file."""
    try:
        df = pd.read_csv(filename)
        description_col = 'Description' if 'Description' in df.columns else None
        
        # Create a set to track used icons
        used_icons = set()
        education_icon_index = 0
        
        # Update icons and colors
        for index, row in df.iterrows():
            if filename == 'module_display_settings.csv':
                icon_color = get_icon_and_color(row['Module_Title'], row['Aim'])
            else:
                desc = row[description_col] if description_col else ''
                icon_color = get_icon_and_color(row['Name'], desc)
            
            attempts = 0
            max_attempts = 10  # Prevent infinite loop
            
            # If icon is already used, try to find an alternative
            while icon_color['icon'] in used_icons and attempts < max_attempts:
                found_alternative = False
                for keyword in icon_mapping:
                    if (keyword.lower() in row['Module_Title'].lower() or 
                        keyword.lower() in row['Aim'].lower()):
                        if icon_mapping[keyword]['icon'] not in used_icons:
                            icon_color = icon_mapping[keyword]
                            found_alternative = True
                            break
                if not found_alternative:
                    # If no alternative found, use the next education icon
                    next_icon = education_icons[education_icon_index % len(education_icons)]
                    while next_icon['icon'] in used_icons and attempts < len(education_icons):
                        education_icon_index += 1
                        next_icon = education_icons[education_icon_index % len(education_icons)]
                        attempts += 1
                    icon_color = next_icon
                    education_icon_index += 1
                attempts += 1
            
            df.at[index, 'Icon'] = icon_color['icon']
            df.at[index, 'Color'] = icon_color['color']
            used_icons.add(icon_color['icon'])
        
        # Save the updated CSV
        df.to_csv(filename, index=False)
        print(f"Updated {filename} with new icons and colors")
        
        # Print distribution of icons
        print("\nIcon distribution:")
        icon_counts = df['Icon'].value_counts()
        print(f"Number of unique icons used: {len(icon_counts)}")
        print(icon_counts)
        print("\n" + "="*50 + "\n")
        
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

# Update both files
update_csv_icons('module_display_settings.csv')
