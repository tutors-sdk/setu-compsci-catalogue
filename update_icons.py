import os
import re
import yaml

# Icon mapping based on keywords in titles
ICON_MAPPING = {
    # Core Skills & Communications
    r'communications?|professional practice|skills': {
        'type': 'material-symbols:chat-bubble-outline',
        'color': '4CAF50'  # Green
    },
    
    # Programming & Development
    r'programming|software|web|development|app': {
        'type': 'material-symbols:code',
        'color': '2196F3'  # Blue
    },
    
    # Mathematics & Analytics
    r'mathematics|statistics|algorithms|functions': {
        'type': 'material-symbols:functions',
        'color': 'FF9800'  # Orange
    },
    
    # Systems & Networks
    r'computer systems|networks?|database': {
        'type': 'material-symbols:lan',
        'color': '9C27B0'  # Purple
    },
    
    # Design & UX
    r'design|ux|user experience|graphic': {
        'type': 'material-symbols:palette-outline',
        'color': 'E91E63'  # Pink
    },
    
    # Business & Enterprise
    r'business|enterprise|entrepreneurship': {
        'type': 'material-symbols:business-center',
        'color': '795548'  # Brown
    },
    
    # Security & Infrastructure
    r'security|cloud|infrastructure': {
        'type': 'material-symbols:security',
        'color': 'F44336'  # Red
    },
    
    # Psychology & Social Sciences
    r'psychology|social': {
        'type': 'material-symbols:psychology',
        'color': '009688'  # Teal
    },
    
    # Languages & International
    r'french|german|international': {
        'type': 'material-symbols:translate',
        'color': '3F51B5'  # Indigo
    },
    
    # Project Work & Placement
    r'project|placement|portfolio': {
        'type': 'material-symbols:work',
        'color': '607D8B'  # Blue Grey
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
