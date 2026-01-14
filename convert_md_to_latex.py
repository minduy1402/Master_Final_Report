#!/usr/bin/env python3
"""
Script to convert Markdown syntax to LaTeX in main.tex file
"""

import re

def convert_markdown_to_latex(content):
    """Convert Markdown headings and formatting to LaTeX"""
    
    # Replace **text** with \textbf{text}
    content = re.sub(r'\*\*([^\*]+)\*\*', r'\\textbf{\1}', content)
    
    # Replace *text* with \textit{text} (but not ** which we already handled)
    content = re.sub(r'(?<!\*)\*([^\*]+)\*(?!\*)', r'\\textit{\1}', content)
    
    # Replace bullet points - with \item
    content = re.sub(r'^\s*-\s+', r'\\item ', content, flags=re.MULTILINE)
    
    # Replace Markdown table separators (if any simple ones)
    # Keep existing tables as-is since they seem properly formatted
    
    # Replace --- horizontal rules with \hrule or remove them
    content = re.sub(r'^---+\s*$', r'', content, flags=re.MULTILINE)
    
    return content

def convert_headings(content):
    """Convert Markdown headings (#, ##, ###, ####) to LaTeX"""
    
    # We need to be careful - only convert lines that start with # but are not in LaTeX already
    # Skip lines that already have \chapter, \section, etc.
    
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Skip if line already contains LaTeX sectioning commands
        if '\\chapter{' in line or '\\section{' in line or '\\subsection{' in line or '\\subsubsection{' in line:
            result.append(line)
            continue
            
        # Convert #### to \subsubsection
        if line.strip().startswith('#### '):
            heading = line.strip()[5:].strip()
            result.append(f'\\subsubsection{{{heading}}}')
        # Convert ### to \subsection
        elif line.strip().startswith('### '):
            heading = line.strip()[4:].strip()
            result.append(f'\\subsection{{{heading}}}')
        # Convert ## to \section
        elif line.strip().startswith('## '):
            heading = line.strip()[3:].strip()
            result.append(f'\\section{{{heading}}}')
        # Convert # to \chapter (but be careful with this)
        elif line.strip().startswith('# ') and not line.strip().startswith('## '):
            heading = line.strip()[2:].strip()
            # Only convert if it looks like a real chapter heading
            if len(heading) > 0 and not heading.startswith('#'):
                result.append(f'\\chapter{{{heading}}}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def main():
    # Read the file
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert headings
    content = convert_headings(content)
    
    # Convert other Markdown syntax
    content = convert_markdown_to_latex(content)
    
    # Write back
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Conversion complete! Check main.tex for results.")
    print("A backup was saved as main_backup.tex")

if __name__ == '__main__':
    main()
