'''
Gathering modified posts
'''

from pathlib import Path
from subprocess import run, PIPE
from constants import POST_DIR, BASELINE_FILE



def get_changed_files() -> set[Path]:
    """
    Gather modified posts
    """
    
    try:
        with open(BASELINE_FILE, encoding="utf-8") as f:
            last_commit = f.read().strip()
        print(f"Last scanned commit: {last_commit}")
        
        result = run(
            ["git", "diff", "--name-only", last_commit, "HEAD"],
            stdout=PIPE, stderr=PIPE, text=True
        )
        changed_files = set(result.stdout.strip().split("\n"))
    except FileNotFoundError:
        print('No baseline found. Scanning all...')
        return set(POST_DIR.glob('**/*.md'))

    result = run(["git", "ls-files", "--others", "--exclude-standard"], stdout=PIPE, text=True)
    untracked = set(result.stdout.strip().split("\n"))
    
    result = run(["git", "diff", "--name-only", "--cached"], stdout=PIPE, text=True)
    staged = set(result.stdout.strip().split("\n"))
    
    all_changed = changed_files | untracked | staged
    
    md_files: list[Path] = []
    for file in all_changed:
        file_obj = Path(file)
        if file_obj.is_relative_to(POST_DIR) and file_obj.suffix == '.md':
            md_files.append(file_obj)

    return set(md_files)

if __name__ == '__main__':
    print('\n'.join(str(x) for x in get_changed_files()))