import re

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the top header
content = re.sub(r'# Lab Lens\n## Vision-Based Laboratory Equipment Verification & Spatial Compliance System', 
                 '<h1 align="center">Lab-lens</h1>\n<h2 align="center">Vision-Based Laboratory Equipment Verification & Spatial Compliance System</h2>', 
                 content)

# Make all numbered headings sky blue
content = re.sub(r'### (\d+\.\s.*)', r'<h3 style="color: skyblue;">\1</h3>', content)

# Wrap everything in a div
wrapped_content = '<div style="font-family: \'Times New Roman\', Times, serif;">\n\n' + content + '\n\n</div>'

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(wrapped_content)
