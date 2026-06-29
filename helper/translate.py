'''
Obtain tags and translate
'''

from typing import cast
from pathlib import Path
from os import getenv
from json import loads
from subprocess import run, PIPE
from yaml import safe_load, YAMLError, safe_dump
from openai import OpenAI
from dotenv import load_dotenv
from constants import ROOT_DIR
from frontmatter import load_frontmatter, dump_frontmatter
from modified import get_changed_files


def load_static() -> dict:
    try:
        with open(ROOT_DIR / '_config.before.yml', encoding="utf-8") as f:
            config_before = safe_load(f)
    except FileNotFoundError:
        config_before = {}
    return config_before


def load_known() -> dict[str, str]:
    try:
        with open(ROOT_DIR / "known_tags.yaml", encoding="utf-8") as f:
            known_translate = safe_load(f) or {}
    except FileNotFoundError:
        known_translate = {}
    return known_translate


def load_openai() -> tuple[OpenAI, str] | tuple[None, None]:
    load_dotenv(ROOT_DIR / '.env')

    endpoint = getenv("LLM_ENDPOINT")
    model = getenv("LLM_MODEL")
    api_key = getenv("LLM_API_KEY")

    if endpoint and model and api_key:
        client = OpenAI(api_key=api_key, base_url=endpoint)
        return client, model
    return None, None


def scan_files(files: set[Path]) -> tuple[set[str], set[str], set[str], set[Path]]:
    print("Scanning posts...")
    print(f"Found {len(files)} changed files")

    exist_tags: set[str] = set()
    exist_categories: set[str] = set()
    exist_category_paths: set[str] = set()
    need_analyze: set[Path] = set()

    for file in files:
        print(f"Scanning {file}")

        content = file.read_text('utf-8')
        data, _ = load_frontmatter(content)

        tags = cast(list[str], data.get("tags") or [])
        exist_tags.update(tags)

        categories = cast(list[str], data.get("categories") or [])
        exist_categories.update(categories)
        exist_category_paths.add("/".join(categories))

        if not data.get("ai_analyzed"):
            need_analyze.add(file)

    print(f"Gathered {len(exist_tags)} tags and {len(exist_categories)} categories. ")
    return exist_tags, exist_categories, exist_category_paths, need_analyze


def analyze(
    need_analyze: set[Path],
    exist_tags: set[str],
    exist_categories: set[str],
    exist_category_paths: set[str],
    client: OpenAI,
    model: str
) -> tuple[set[str], set[str], set[str]]:
    print(f"Need to analyze {len(need_analyze)} posts.")

    SYSTEM_PROMPT = """
    系统会给出现有标签和分类，以及一个Markdown文档。
    请分析文档内容，并根据现有标签和分类，对文档进行合理分类，并使用JSON格式返回。
    若现有标签无法对文档进行合理分类和标注，或有不全面的地方，可以适当新增标签和分类。

    示例输入：
    ````txt
    Tags: C++, GESP, Python, 数据结构, LeetCode, Android, Windows, Linux, MacOS, iOS
    Categories: 编程/算法, 编程/应用, 日志, 软件, 数学, 哲学
    Document:
    ```md
    # 题目描述
    给你一个整数数组 `nums` 和一个整数 `k`。

    每一步操作中，你需要从数组中选出并删除一个元素。

    返回使数组中剩余元素的总和等于 `k` 所需的最少操作数。
    ```
    ````

    示例返回：
    ```json
    {
        "tags": ["C++", ...],
        "categories": ["编程", "算法"]
    }
    ```

    返回的categories中的内容由左至右为层级关系，如 `["编程", "算法"]` 即表示 `编程/算法` 这个分类。而tags中的内容为平级关系。
    输入的categories（不包括Document frontmatter）表示在整个知识库范围内已存在的层级关系列表，但你也可以灵活运用，比如直接使用 `编程` 这个父分类或 `日志/日常` 这种子分类。
    需要注意的是你应该尽量避免在两个地方出现同一个分类名，比如 `编程/算法` 和 `算法`、`数学/算法`...
    """

    added_tags: set[str] = set()
    added_categories: set[str] = set()
    added_category_paths: set[str] = set()

    for filepath in need_analyze:
        print(f"Analyzing {filepath}")

        content = filepath.read_text('utf-8')

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Tags: {', '.join(exist_tags | added_tags)}\n"
                        f"Categories: {', '.join(exist_category_paths | added_category_paths)}\n"
                        f"Document:\n```md\n{content}\n```",
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
            )

            json_obj: dict[str, list[str]] = loads(
                response.choices[0].message.content or "{}"
            )
            new_tags: set[str] = set(json_obj.get("tags") or [])
            new_categories: list[str] = json_obj.get("categories") or []
            category_path = "/".join(new_categories)
            added_tags |= new_tags - exist_tags
            added_categories |= set(new_categories) - exist_categories

            if category_path not in exist_category_paths:
                added_category_paths.add(category_path)

            frontmatter, body = load_frontmatter(content)
            frontmatter["tags"] = list(new_tags)
            frontmatter["categories"] = list(new_categories)
            frontmatter["ai_analyzed"] = True

            print(f"New tags: {new_tags}")
            print(f"New categories: {new_categories}")

            updated_content = dump_frontmatter(body, frontmatter)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)

        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")

    print(
        f"Totally added {len(added_tags)} tags and {len(added_categories)} categories: \n{', '.join(added_tags | added_categories)}"
    )
    return added_tags, added_categories, added_category_paths


def translate(
    waiting_translate: set[str],
    known_translate: dict[str, str],
    client: OpenAI,
    model: str
) -> dict[str, str]:
    print(f"Waiting to translate {len(waiting_translate)} tags.")

    SYSTEM_PROMPT = """
    系统会给出标签的中文名称，用英文逗号隔开，你需要返回一个 JSON 格式的字符串，包含标签的中文名称和 URL 友好的名称。

    示例：

    Input
    ```txt
    编程, C++, GESP, Python, 算法, 数据结构, LeetCode, 力扣
    ```

    Output
    ```json
    {
        "编程": "programming",
        "C++": "cpp",
        "GESP": "gesp",
        "Python": "python",
        "算法": "algorithm",
        "数据结构": "data-structure",
        "LeetCode": "leetcode",
        "力扣": "leetcode"
    }
    ```
    """

    print()
    print("Sending request to LLM...")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": ", ".join(waiting_translate)},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        json_obj: dict[str, str] = loads(response.choices[0].message.content or "{}")

        print("New knowledge get:")
        for tag, url_friendly in json_obj.items():
            known_translate[tag] = url_friendly
            print(f"{tag}: {url_friendly}")

        known_translate.update(json_obj)
        with open(ROOT_DIR / "known_tags.yaml", "w", encoding="utf-8") as f:
            safe_dump(known_translate, f, allow_unicode=True)

        print(f"Updated {len(json_obj)} tags.")

    except Exception as e:
        print(f"Error translating tags: {e}")

    return known_translate


def generate_config(
    exist_tags: set[str],
    exist_categories: set[str],
    known_translate: dict[str, str]
) -> None:
    print()
    print("Generating _config.yml...")

    config = load_static()

    config["tag_map"] = {
        tag: known_translate[tag] for tag in exist_tags if tag in known_translate
    }

    config["category_map"] = {
        category: known_translate[category]
        for category in exist_categories
        if category in known_translate
    }

    with open(ROOT_DIR / "_config.yml", "w", encoding="utf-8") as f:
        safe_dump(config, f, allow_unicode=True)

    print(
        f"Generated _config.yml with {len(config['tag_map'])} tags and {len(config['category_map'])} categories."
    )


def update_baseline() -> None:
    result = run(["git", "rev-parse", "HEAD"], stdout=PIPE, text=True)
    current_commit = result.stdout.strip()

    if current_commit:
        with open(ROOT_DIR / "last_scanned_commit.txt", "w", encoding="utf-8") as f:
            f.write(current_commit)
        print(f"Updated baseline to commit: {current_commit}")


def main() -> None:
    print("Starting translation workflow...")

    client, model = load_openai()
    if not client or not model:
        print("OpenAI client not configured. Exiting.")
        return

    known_translate = load_known()
    changed_files = get_changed_files()

    exist_tags, exist_categories, exist_category_paths, need_analyze = scan_files(changed_files)

    if need_analyze:
        added_tags, added_categories, added_category_paths = analyze(
            need_analyze, exist_tags, exist_categories, exist_category_paths, client, model
        )
        exist_tags |= added_tags
        exist_categories |= added_categories
        exist_category_paths |= added_category_paths

    print()
    print(f"Total {len(exist_tags)} tags and {len(exist_categories)} categories. ")

    merged = exist_tags | exist_categories
    waiting_translate: set[str] = set()
    for tag in merged:
        print(
            f"{tag}: Tag: {tag in exist_tags}, Category: {tag in exist_categories}, Known: {known_translate.get(tag)}"
        )
        if tag not in known_translate:
            waiting_translate.add(tag)

    if waiting_translate:
        translate(waiting_translate, known_translate, client, model)

    generate_config(exist_tags, exist_categories, known_translate)
    update_baseline()


if __name__ == '__main__':
    main()