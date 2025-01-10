import csv
import json
from typing import Dict, Any

def save_as_csv(data: Dict[str, Any], file_path: str) -> None:
    """Save scraped data as Comma-Separated Values file."""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Type', 'Name', 'Details'])
        
        # Write basic information
        writer.writerow(['Title', data.get('title', 'No title'), ''])
        
        # Write classes information
        for class_name, info in data.get('classes', {}).items():
            writer.writerow(['Class', class_name, f"Used {info['count']} times"])
            writer.writerow(['', 'Tag Types', ', '.join(info['tag_types'])])
            for sample in info.get('sample_content', []):
                writer.writerow(['', 'Sample', sample[:100]])

def save_as_html(data: Dict[str, Any], file_path: str) -> None:
    """Save scraped data as formatted Hypertext Markup Language file."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Web Scraping Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .section {{ margin-bottom: 20px; }}
            .class-item {{ margin: 10px 0; padding: 10px; border: 1px solid #ccc; }}
            .sample {{ color: #666; margin-left: 20px; }}
        </style>
    </head>
    <body>
        <h1>Scraping Results</h1>
        <div class="section">
            <h2>Page Title</h2>
            <p>{data.get('title', 'No title')}</p>
        </div>
        
        <div class="section">
            <h2>HTML Classes</h2>
            {''.join([f'''
                <div class="class-item">
                    <h3>{class_name}</h3>
                    <p>Used {info['count']} times</p>
                    <p>Tags: {', '.join(info['tag_types'])}</p>
                    {''.join([f'<p class="sample">Sample: {sample}</p>' 
                             for sample in info['sample_content']])}
                </div>
            ''' for class_name, info in data.get('classes', {}).items()])}
        </div>
    </body>
    </html>
    """
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
