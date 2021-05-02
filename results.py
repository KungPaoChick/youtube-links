import json
import colorama


def view_results(filename='search_results.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as j_source:
            source = json.load(j_source)

        for content in source['contents']:
            for key in content:
                print(colorama.Fore.YELLOW, f"[!] {key}", colorama.Style.RESET_ALL, f"- {content[key]}")

        print(colorama.Fore.GREEN, f"[*] Results: {source['info']['results']}",
                    colorama.Style.RESET_ALL)
    except FileNotFoundError:
        print(colorama.Fore.RED, f"[!!] You have no search results",
                    colorama.Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    view_results()
