from yaml import YAMLError, safe_dump, safe_load

FrontMatterType = dict[str, str | list[str] | bool]

def load_frontmatter(content: str) -> tuple[FrontMatterType, str]:
    print('Parsing frontmatter')
    splitted = content.split("---", 2)
    if len(splitted) < 3 or splitted[0].strip():
        print('No frontmatter found!')
        return {}, content
    try:
        return safe_load(splitted[1]), splitted[2].strip()
    except YAMLError as e:
        print(f'Invalid frontmatter: {e}')
    return {}, content

def dump_frontmatter(content: str, frontmatter: FrontMatterType) -> str:
    print('Dumping frontmatter')
    splitted = content.split("---", 2)
    if len(splitted) < 3 or splitted[0].strip():
        print('No frontmatter found! Creating new...')
        splitted = ['', '', f'\n\n{content.strip()}\n']
    splitted[1] = f'\n{safe_dump(frontmatter, allow_unicode=True)}'
    return '---'.join(splitted)