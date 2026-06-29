'''
Fixing frontmatter
'''

from pathlib import Path
from datetime import datetime
from frontmatter import load_frontmatter, dump_frontmatter

def fix_frontmatter(files: set[Path]):
    print('Fixing frontmatter')

    for file in files:
        print(f'Fixing {file}')

        raw_content = file.read_text('utf-8')
        fm_orig, content = load_frontmatter(raw_content)

        frontmatter: dict[str, str | list[str] | bool] = {
            'title': file.name[:-3],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tags': [],
            'categories': [],
        }
        frontmatter |= fm_orig
        
        if "$" in content:
            frontmatter["mathjax"] = True

        file.write_text(dump_frontmatter(raw_content, frontmatter), 'utf-8')

if __name__ == '__main__':
    from modified import get_changed_files
    fix_frontmatter(get_changed_files())
