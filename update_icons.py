import os
import re
import yaml

# Icon mapping based on keywords in titles
ICON_MAPPING = {
    # Communications & Skills
    r'communications?': {
        'type': 'mdi:message-text',
        'color': '4CAF50'  # Green
    },
    r'professional practice': {
        'type': 'carbon:certificate',
        'color': '795548'  # Brown
    },
    
    # Programming & Development
    r'programming|software': {
        'type': 'ph:code-bold',
        'color': '2196F3'  # Blue
    },
    r'web.*development': {
        'type': 'carbon:development',
        'color': '03A9F4'  # Light Blue
    },
    r'app development': {
        'type': 'mdi:cellphone-link',
        'color': '00BCD4'  # Cyan
    },
    
    # Mathematics & Analytics
    r'mathematics': {
        'type': 'ph:function-bold',
        'color': 'FF9800'  # Orange
    },
    r'statistics': {
        'type': 'carbon:chart-line-data',
        'color': 'FF5722'  # Deep Orange
    },
    r'algorithms': {
        'type': 'carbon:flow',
        'color': 'FFC107'  # Amber
    },
    
    # Systems & Networks
    r'computer systems': {
        'type': 'carbon:bare-metal-server',
        'color': '9C27B0'  # Purple
    },
    r'networks?': {
        'type': 'ph:nodes-bold',
        'color': '673AB7'  # Deep Purple
    },
    r'database': {
        'type': 'mdi:database',
        'color': '3F51B5'  # Indigo
    },
    
    # Design & UX
    r'design': {
        'type': 'ph:paint-brush-bold',
        'color': 'E91E63'  # Pink
    },
    r'user experience|ux': {
        'type': 'carbon:user-interface',
        'color': 'F06292'  # Light Pink
    },
    r'graphic': {
        'type': 'ph:pencil-circle-bold',
        'color': 'FF4081'  # Pink A200
    },
    
    # Business & Enterprise
    r'business': {
        'type': 'carbon:analytics',
        'color': '795548'  # Brown
    },
    r'enterprise': {
        'type': 'carbon:enterprise',
        'color': '8D6E63'  # Brown 400
    },
    r'entrepreneurship': {
        'type': 'ph:rocket-launch-bold',
        'color': '6D4C41'  # Brown 600
    },
    
    # Security & Infrastructure
    r'security': {
        'type': 'mdi:shield-lock',
        'color': 'F44336'  # Red
    },
    r'forensics': {
        'type': 'mdi:magnify-scan',
        'color': 'E57373'  # Red 300
    },
    r'cloud': {
        'type': 'carbon:cloud',
        'color': '03A9F4'  # Light Blue
    },
    r'infrastructure': {
        'type': 'carbon:cloud-services',
        'color': 'E57373'  # Red 300
    },
    
    # Psychology & Social Sciences
    r'psychology': {
        'type': 'ph:brain-bold',
        'color': '009688'  # Teal
    },
    r'social': {
        'type': 'ph:users-three-bold',
        'color': '26A69A'  # Teal 400
    },
    
    # Languages & International
    r'french': {
        'type': 'emojione-v1:flag-for-france',
        'color': '3F51B5'  # Indigo
    },
    r'german': {
        'type': 'emojione-v1:flag-for-germany',
        'color': '5C6BC0'  # Indigo 400
    },
    r'international': {
        'type': 'carbon:earth',
        'color': '7986CB'  # Indigo 300
    },
    
    # Project Work & Placement
    r'project': {
        'type': 'carbon:task',
        'color': '607D8B'  # Blue Grey
    },
    r'placement': {
        'type': 'carbon:workspace',
        'color': '78909C'  # Blue Grey 400
    },
    r'portfolio': {
        'type': 'carbon:portfolio',
        'color': '90A4AE'  # Blue Grey 300
    },
    
    # Media & Animation
    r'animation': {
        'type': 'ph:film-reel-bold',
        'color': 'FF4081'  # Pink A200
    },
    r'media': {
        'type': 'carbon:media-library',
        'color': 'FF80AB'  # Pink A100
    },
    r'video': {
        'type': 'ph:video-camera-bold',
        'color': 'C2185B'  # Pink 700
    },
    r'audio': {
        'type': 'ph:wave-sine-bold',
        'color': 'E91E63'  # Pink
    },
    
    # Operating Systems & Tools
    r'operating systems': {
        'type': 'carbon:terminal',
        'color': '424242'  # Grey 800
    },
    r'tools': {
        'type': 'ph:wrench-bold',
        'color': '616161'  # Grey 700
    },
    
    # Game Development
    r'game': {
        'type': 'ph:game-controller-bold',
        'color': '7C4DFF'  # Deep Purple A200
    },
    
    # Research & Analysis
    r'research': {
        'type': 'carbon:research',
        'color': '00BFA5'  # Teal A700
    },
    r'analysis': {
        'type': 'carbon:data-vis-4',
        'color': '1DE9B6'  # Teal A400
    },
    
    # Degree Programs
    r'BSc.*Information Technology': {
        'type': 'mdi:school',
        'color': '1565C0'  # Blue 800
    },
    r'BSc.*Creative Computing': {
        'type': 'mdi:palette-swatch',
        'color': '6200EA'  # Deep Purple A700
    },
    r'BSc.*Computer Science': {
        'type': 'mdi:laptop',
        'color': '2962FF'  # Blue A700
    },
    r'BSc.*Computing': {
        'type': 'mdi:monitor',
        'color': '304FFE'  # Indigo A700
    },
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

def update_markdown_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Skip files that don't need icons
                if not content.strip() or content.startswith('---'):
                    continue

                # Extract the title from the markdown
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                    
                    # Find matching icon
                    icon_info = None
                    for pattern, icon in ICON_MAPPING.items():
                        if re.search(pattern, title, re.IGNORECASE):
                            icon_info = icon
                            break
                    
                    if icon_info:
                        # Create frontmatter with icon
                        frontmatter = f"---\nicon:\n  type: {icon_info['type']}\n  color: {icon_info['color']}\n---\n\n"
                        
                        # Add frontmatter to content
                        updated_content = frontmatter + content
                        
                        # Write back to file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                            print(f"Updated: {file_path}")

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    update_markdown_files(script_dir)
    process_directory(script_dir)
