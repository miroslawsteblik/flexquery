import os
import shutil
import markdown
from pathlib import Path
from flexquery.config.pathconfig import AppPaths

class DocsGenerator:
    """Generates HTML documentation from markdown files."""
    
    def __init__(self):
        """Initialize the DocsGenerator."""
        self.docs_serve_dir = os.path.join(os.path.expanduser("~"), "Documents",".flexquery", "docs")
        os.makedirs(self.docs_serve_dir, exist_ok=True)
        self.template = AppPaths.get_templates_dir() / 'web_docs' / 'web_template.html'

        
    def generate_docs(self, force=True):
        """
        Generate HTML documentation.
        
        Returns:
            str: Path to the generated documentation index file
        """

        index_path = os.path.join(self.docs_serve_dir, "index.html")
        
        if force or not os.path.exists(index_path):
            self._clean_docs_dir()
            self._copy_static_files()
            self._generate_html_files()
            self._index_content()
        
            
        return index_path
    
    def _clean_docs_dir(self):
        """Clean the docs directory."""
        for item in os.listdir(self.docs_serve_dir):
            if item.endswith(('.html', '.css')):
                path = os.path.join(self.docs_serve_dir, item)
                if os.path.isfile(path):
                    os.remove(path)

    
    def _copy_static_files(self):
        """Copy static files to the temp directory."""
        static_dir = self._get_static_dir()
        if not static_dir:
            return 
        
        for item in os.listdir(static_dir):
            src = os.path.join(static_dir, item)
            dest = os.path.join(self.docs_serve_dir, item)
            if os.path.isfile(src):
                if item.endswith('.md'):
                    continue
                shutil.copy2(src, dest)

    def _get_static_dir(self):
        """Get the static directory."""
        static_dir = AppPaths.get_docs_dir()
        if not os.path.exists(static_dir):
            return None
        return static_dir
            
    
    def _generate_html_files(self):
        """Generate HTML files from markdown."""
        docs_dir = self._get_static_dir()
            
        # Find and convert markdown files
        for md_file in Path(docs_dir).glob("**/*.md"):

            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
                
            html_content = self._md_to_html(md_content, str(md_file))
            
            # Replace .md with .html
            rel_path = md_file.relative_to(docs_dir)
            out_path = os.path.join(self.docs_serve_dir, rel_path.with_suffix('.html'))
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
            # Write HTML file
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def _load_template(self):
        """Load the HTML template from file."""
        try:
            # First try to load from package directory
            if os.path.exists(self.template):
                with open(self.template, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Failed to load template: {e}")
            
        # Fallback to hardcoded minimal template
        return """<!DOCTYPE html>
        <html>
        <head><title>FlexQuery - {{title}}</title></head>
        <body>
            <h1>FlexQuery Documentation</h1>
            <nav><p>{{nav_html}}</p></nav>
            <hr>
            {{content}}
        </body>
        </html>"""

    
    def _md_to_html(self, md_content, filename):
        """Convert markdown to HTML with styling."""

        title = os.path.basename(filename).replace('.md', '')

        # Generate navigation links dynamically
        nav_links = ['<a href="index.html">Home</a>']
        
        # Add links to other HTML files
        try:
            for html_file in os.listdir(self.docs_serve_dir):
                if html_file.endswith('.html') and html_file != 'index.html':
                    link_name = html_file.replace('.html', '').capitalize()
                    nav_links.append(f'<a href="{html_file}">{link_name}</a>')
        except Exception:
            raise
        
        nav_html = " | ".join(nav_links)
        content = markdown.markdown(md_content, extensions=[
                    'tables', 
                    'fenced_code',
                    'extra',
                    'sane_lists',
                    'nl2br',
                    ])


        template = self._load_template()
        html = (template
                .replace("{{title}}", title)
                .replace("{{nav_html}}", nav_html)
                .replace("{{content}}", content)
                )
        
        return html
    
    def _index_content(self):
        """Generate default documentation if no files found."""
        try:
            index_content = """# FlexQuery Documentation\n\n## Overview\n\nFlexQuery is a flexible SQL query tool..."""
            
            index_path = os.path.join(self.docs_serve_dir, "index.html")
            
            # Write index.html
            with open(index_path, 'w', encoding='utf-8') as f:  
                f.write(self._md_to_html(index_content, "index.md"))
                
        except Exception as e:
            raise