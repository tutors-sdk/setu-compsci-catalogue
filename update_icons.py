import os
import re
import yaml

# Icon mapping based on keywords in titles
ICON_MAPPING = {
    # Communications & Skills
    r'communications?': {
        'type': 'material-symbols:chat-bubble-outline',
        'color': '4CAF50'  # Green
    },
    r'professional practice': {
        'type': 'material-symbols:workspace-premium',
        'color': '795548'  # Brown
    },
    
    # Programming & Development
    r'programming|software': {
        'type': 'material-symbols:code',
        'color': '2196F3'  # Blue
    },
    r'web.*development': {
        'type': 'material-symbols:web',
        'color': '03A9F4'  # Light Blue
    },
    r'app development': {
        'type': 'material-symbols:apps',
        'color': '00BCD4'  # Cyan
    },
    
    # Mathematics & Analytics
    r'mathematics': {
        'type': 'material-symbols:functions',
        'color': 'FF9800'  # Orange
    },
    r'statistics': {
        'type': 'material-symbols:monitoring',
        'color': 'FF5722'  # Deep Orange
    },
    r'algorithms': {
        'type': 'material-symbols:schema',
        'color': 'FFC107'  # Amber
    },
    
    # Systems & Networks
    r'computer systems': {
        'type': 'material-symbols:computer',
        'color': '9C27B0'  # Purple
    },
    r'networks?': {
        'type': 'material-symbols:lan',
        'color': '673AB7'  # Deep Purple
    },
    r'database': {
        'type': 'material-symbols:database',
        'color': '3F51B5'  # Indigo
    },
    
    # Design & UX
    r'design': {
        'type': 'material-symbols:palette-outline',
        'color': 'E91E63'  # Pink
    },
    r'user experience|ux': {
        'type': 'material-symbols:person-play',
        'color': 'F06292'  # Light Pink
    },
    r'graphic': {
        'type': 'material-symbols:brush',
        'color': 'FF4081'  # Pink A200
    },
    
    # Business & Enterprise
    r'business': {
        'type': 'material-symbols:business-center',
        'color': '795548'  # Brown
    },
    r'enterprise': {
        'type': 'material-symbols:corporate-fare',
        'color': '8D6E63'  # Brown 400
    },
    r'entrepreneurship': {
        'type': 'material-symbols:rocket-launch',
        'color': '6D4C41'  # Brown 600
    },
    
    # Security & Infrastructure
    r'security': {
        'type': 'material-symbols:security',
        'color': 'F44336'  # Red
    },
    r'cloud': {
        'type': 'material-symbols:cloud',
        'color': '03A9F4'  # Light Blue
    },
    r'infrastructure': {
        'type': 'material-symbols:dns',
        'color': 'E57373'  # Red 300
    },
    
    # Psychology & Social Sciences
    r'psychology': {
        'type': 'material-symbols:psychology',
        'color': '009688'  # Teal
    },
    r'social': {
        'type': 'material-symbols:groups',
        'color': '26A69A'  # Teal 400
    },
    
    # Languages & International
    r'french': {
        'type': 'material-symbols:translate',
        'color': '3F51B5'  # Indigo
    },
    r'german': {
        'type': 'material-symbols:language',
        'color': '5C6BC0'  # Indigo 400
    },
    r'international': {
        'type': 'material-symbols:public',
        'color': '7986CB'  # Indigo 300
    },
    
    # Project Work & Placement
    r'project': {
        'type': 'material-symbols:work',
        'color': '607D8B'  # Blue Grey
    },
    r'placement': {
        'type': 'material-symbols:badge',
        'color': '78909C'  # Blue Grey 400
    },
    r'portfolio': {
        'type': 'material-symbols:folder-special',
        'color': '90A4AE'  # Blue Grey 300
    },
    
    # Media & Animation
    r'animation': {
        'type': 'material-symbols:animation',
        'color': 'FF4081'  # Pink A200
    },
    r'media': {
        'type': 'material-symbols:perm-media',
        'color': 'FF80AB'  # Pink A100
    },
    r'video': {
        'type': 'material-symbols:videocam',
        'color': 'C2185B'  # Pink 700
    },
    r'audio': {
        'type': 'material-symbols:music-note',
        'color': 'E91E63'  # Pink
    },
    
    # Operating Systems & Tools
    r'operating systems': {
        'type': 'material-symbols:terminal',
        'color': '424242'  # Grey 800
    },
    r'tools': {
        'type': 'material-symbols:tools',
        'color': '616161'  # Grey 700
    },
    
    # Game Development
    r'game': {
        'type': 'material-symbols:sports-esports',
        'color': '7C4DFF'  # Deep Purple A200
    },
    
    # Research & Analysis
    r'research': {
        'type': 'material-symbols:research',
        'color': '00BFA5'  # Teal A700
    },
    r'analysis': {
        'type': 'material-symbols:analytics',
        'color': '1DE9B6'  # Teal A400
    }
}

# Default icon for unmatched content
DEFAULT_ICON = {
    'type': 'material-symbols:school',
    'color': '398126'  # Original green color
}

def determine_icon(title):
    """Determine the appropriate icon based on the title."""
    title_lower = title.lower()
    for pattern, icon in ICON_MAPPING.items():
        if re.search(pattern, title_lower):
            return icon
    return DEFAULT_ICON

def update_markdown_file(file_path):
    """Update the icon in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Extract the title (assuming it's after the frontmatter)
        title_match = re.search(r'---\n.*?\n---\n\s*(.*?)\n', content, re.DOTALL)
        if not title_match:
            return False
            
        title = title_match.group(1).strip()
        
        # Determine the appropriate icon
        icon_data = determine_icon(title)
        
        # Create new frontmatter
        new_frontmatter = f"""---
icon:
  type: {icon_data['type']}
  color: {icon_data['color']}
---"""
        
        # Replace existing frontmatter
        updated_content = re.sub(r'---\n.*?\n---', new_frontmatter, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
            
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_directory(directory):
    """Process all markdown files in the directory and its subdirectories."""
    success_count = 0
    total_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and 'talk-' in file:
                total_count += 1
                file_path = os.path.join(root, file)
                if update_markdown_file(file_path):
                    success_count += 1
                    print(f"Updated: {file_path}")
                else:
                    print(f"Failed to update: {file_path}")
    
    print(f"\nProcessed {success_count} of {total_count} files successfully")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    process_directory(base_dir)
