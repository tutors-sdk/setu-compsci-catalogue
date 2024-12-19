import pandas as pd
import random

# Define a mapping of keywords to icons and colors - with unique icons for each type
icon_mapping = {
    # Automotive & IoT
    'Advanced Driver Assistance': {'icon': 'mdi:car-cruise-control', 'color': 'FF5252'},
    'Automotive Diagnostic': {'icon': 'mdi:car-wrench', 'color': 'FF4081'},
    'Automotive Software': {'icon': 'mdi:car-cog', 'color': 'E040FB'},
    'Connected Car': {'icon': 'mdi:car-connected', 'color': '7C4DFF'},
    'Embedded Systems': {'icon': 'mdi:chip', 'color': '536DFE'},
    'Industrial Automation': {'icon': 'mdi:robot-industrial', 'color': '448AFF'},
    'IoT': {'icon': 'mdi:iot', 'color': '40C4FF'},
    'Model-Based': {'icon': 'mdi:graph', 'color': '18FFFF'},
    
    # Database & Analytics
    'NoSQL': {'icon': 'mdi:database', 'color': '64FFDA'},
    'Business Intelligence': {'icon': 'mdi:chart-box', 'color': '69F0AE'},
    'Data Warehouse': {'icon': 'mdi:database-clock', 'color': '76FF03'},
    'Data Analytics': {'icon': 'mdi:chart-bell-curve', 'color': 'EEFF41'},
    'Data Mining': {'icon': 'mdi:pickaxe', 'color': 'FFFF00'},
    'Data Science': {'icon': 'mdi:flask', 'color': 'FFD740'},
    'Database Admin': {'icon': 'mdi:database-cog', 'color': 'FFAB40'},
    'Database Design': {'icon': 'mdi:database-edit', 'color': 'FF6E40'},
    'Database Systems': {'icon': 'mdi:database-sync', 'color': 'FF5252'},
    'Multimedia Database': {'icon': 'mdi:database-image', 'color': 'FF4081'},
    'Relational Database': {'icon': 'mdi:table', 'color': 'E040FB'},
    
    # Electronics & Engineering
    'Electronics': {'icon': 'mdi:circuit-board', 'color': '7C4DFF'},
    'Digital': {'icon': 'mdi:memory', 'color': '536DFE'},
    'Analog': {'icon': 'mdi:sine-wave', 'color': '448AFF'},
    'Microcontroller': {'icon': 'mdi:chip', 'color': '40C4FF'},
    'PCB': {'icon': 'mdi:circuit-board', 'color': '18FFFF'},
    
    # Forensics & Security
    'Forensics': {'icon': 'mdi:magnify-scan', 'color': '64FFDA'},
    'Security': {'icon': 'mdi:shield-lock', 'color': '69F0AE'},
    'Cybersecurity': {'icon': 'mdi:security', 'color': '76FF03'},
    'Network Security': {'icon': 'mdi:shield-network', 'color': 'EEFF41'},
    'Cryptography': {'icon': 'mdi:encryption', 'color': 'FFFF00'},
    
    # Game Development
    'Game': {'icon': 'mdi:gamepad-variant', 'color': 'FFD740'},
    'Game Engine': {'icon': 'mdi:unity', 'color': 'FFAB40'},
    'Game Physics': {'icon': 'mdi:physics', 'color': 'FF6E40'},
    'Game AI': {'icon': 'mdi:robot', 'color': 'FF5252'},
    
    # Graphics & Animation
    'Graphics': {'icon': 'mdi:palette', 'color': 'FF4081'},
    'Design': {'icon': 'mdi:pencil-ruler', 'color': 'E040FB'},
    'Animation': {'icon': 'mdi:animation', 'color': '7C4DFF'},
    '3D': {'icon': 'mdi:cube-outline', 'color': '536DFE'},
    
    # Information Systems
    'Information Systems': {'icon': 'mdi:sitemap', 'color': '448AFF'},
    'Systems Analysis': {'icon': 'mdi:chart-gantt', 'color': '40C4FF'},
    'Enterprise': {'icon': 'mdi:office-building', 'color': '18FFFF'},
    'Business Process': {'icon': 'mdi:flowchart', 'color': '64FFDA'},
    
    # Mathematics & Physics
    'Mathematics': {'icon': 'mdi:function', 'color': '69F0AE'},
    'Physics': {'icon': 'mdi:atom', 'color': '76FF03'},
    'Statistics': {'icon': 'mdi:chart-bell-curve-cumulative', 'color': 'EEFF41'},
    'Linear Algebra': {'icon': 'mdi:matrix', 'color': 'FFFF00'},
    
    # Networks & Cloud
    'Networks': {'icon': 'mdi:lan', 'color': 'FFD740'},
    'Cloud': {'icon': 'mdi:cloud', 'color': 'FFAB40'},
    'DevOps': {'icon': 'mdi:infinity', 'color': 'FF6E40'},
    'Infrastructure': {'icon': 'mdi:server', 'color': 'FF5252'},
    
    # Software Development
    'Software': {'icon': 'mdi:code-braces', 'color': 'FF4081'},
    'Web': {'icon': 'mdi:web', 'color': 'E040FB'},
    'Programming': {'icon': 'mdi:code-tags', 'color': '7C4DFF'},
    'Development': {'icon': 'mdi:developer-board', 'color': '536DFE'},
    'Testing': {'icon': 'mdi:test-tube', 'color': '448AFF'},
    'Agile': {'icon': 'mdi:sync', 'color': '40C4FF'},
    'Project': {'icon': 'mdi:clipboard-check', 'color': '18FFFF'},
    
    # Default (fallback)
    'default': {'icon': 'mdi:school', 'color': '78909C'}
}

# Default education-related icons for variety
education_icons = [
    {'icon': 'mdi:book-open-page-variant', 'color': 'A435F0'},
    {'icon': 'mdi:book-open-variant', 'color': '0056D2'},
    {'icon': 'mdi:book-education', 'color': '02262B'},
    {'icon': 'mdi:book-lock', 'color': 'F15B2A'},
    {'icon': 'mdi:book-lock-open', 'color': '149EF2'},
    {'icon': 'mdi:book-minus', 'color': '58CC02'},
    {'icon': 'mdi:book-minus-multiple', 'color': '0A0A23'},
    {'icon': 'mdi:book-multiple', 'color': '1F4056'},
    {'icon': 'mdi:book-multiple-variant', 'color': '14BF96'},
    {'icon': 'mdi:book-open', 'color': '00FF84'}
]

def get_icon_and_color(title, aim):
    """Determine the most appropriate icon and color based on module title and aim."""
    title = title.lower()
    aim = aim.lower() if aim else ""
    
    # Try to match based on title first
    for key, value in icon_mapping.items():
        if key.lower() in title:
            return value['icon'], value['color']
    
    # If no match in title, try matching based on aim
    for key, value in icon_mapping.items():
        if aim and key.lower() in aim:
            return value['icon'], value['color']
    
    # If still no match, try to make an educated guess based on common words
    common_words = {
        'automotive': icon_mapping['Automotive Diagnostic'],
        'automation': icon_mapping['Industrial Automation'],
        'robot': icon_mapping['Game AI'],
        'business': icon_mapping['Business Intelligence'],
        'enterprise': icon_mapping['Enterprise'],
        'database': icon_mapping['Database Systems'],
        'analytics': icon_mapping['Data Analytics'],
        'data': icon_mapping['Data Science'],
        'electronics': icon_mapping['Electronics'],
        'circuit': icon_mapping['PCB'],
        'engineering': icon_mapping['Microcontroller'],
        'forensics': icon_mapping['Forensics'],
        'security': icon_mapping['Security'],
        'cyber': icon_mapping['Cybersecurity'],
        'game': icon_mapping['Game'],
        'gaming': icon_mapping['Game'],
        'graphics': icon_mapping['Graphics'],
        'design': icon_mapping['Design'],
        'animation': icon_mapping['Animation'],
        'media': icon_mapping['Graphics'],
        'production': icon_mapping['Graphics'],
        'communication': icon_mapping['Graphics'],
        'information': icon_mapping['Information Systems'],
        'modeling': icon_mapping['Systems Analysis'],
        'mathematics': icon_mapping['Mathematics'],
        'physics': icon_mapping['Physics'],
        'statistics': icon_mapping['Statistics'],
        'network': icon_mapping['Networks'],
        'cloud': icon_mapping['Cloud'],
        'infrastructure': icon_mapping['Infrastructure'],
        'software': icon_mapping['Software'],
        'web': icon_mapping['Web'],
        'programming': icon_mapping['Programming'],
        'development': icon_mapping['Development'],
        'sports': icon_mapping['Game'],
        'fitness': icon_mapping['Game']
    }
    
    for word, icon_info in common_words.items():
        if word in title or (aim and word in aim):
            return icon_info['icon'], icon_info['color']
    
    # If no specific match found, return a random education icon
    random_icon = random.choice(education_icons)
    return random_icon['icon'], random_icon['color']

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
                icon, color = get_icon_and_color(row['Module_Title'], row['Aim'])
            else:
                desc = row[description_col] if description_col else ''
                icon, color = get_icon_and_color(row['Name'], desc)
            
            attempts = 0
            max_attempts = 10  # Prevent infinite loop
            
            # If icon is already used, try to find an alternative
            while icon in used_icons and attempts < max_attempts:
                found_alternative = False
                for keyword in icon_mapping:
                    if (keyword.lower() in row['Module_Title'].lower() or 
                        keyword.lower() in row['Aim'].lower()):
                        if icon_mapping[keyword]['icon'] not in used_icons:
                            icon = icon_mapping[keyword]['icon']
                            color = icon_mapping[keyword]['color']
                            found_alternative = True
                            break
                if not found_alternative:
                    # If no alternative found, use the next education icon
                    next_icon = education_icons[education_icon_index % len(education_icons)]
                    while next_icon['icon'] in used_icons and attempts < len(education_icons):
                        education_icon_index += 1
                        next_icon = education_icons[education_icon_index % len(education_icons)]
                        attempts += 1
                    icon = next_icon['icon']
                    color = next_icon['color']
                    education_icon_index += 1
                attempts += 1
            
            df.at[index, 'Icon'] = icon
            df.at[index, 'Color'] = color
            used_icons.add(icon)
        
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
