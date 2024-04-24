import argparse
import markdownify
from bs4 import BeautifulSoup


def remove_trailing_newline(lst):
    if lst and lst[-1] == '\n':
        lst.pop()
    return lst


def remove_coverage_is_exists(readme_path):
    with open(readme_path, "r") as fp:
        lines = fp.readlines()

    lines = remove_trailing_newline(lines)

    with open(readme_path, "w") as fp:
        for line in lines:

            if line.strip("\n") != "## Coverage":
                fp.write(line)
            else:
                break


def write_coverage_in_readme(readme_path, h):
    file = open(readme_path, 'a')
    file.write('## Coverage')
    file.write(h)
    file.close()


def scrap_html(settings):
    html_path = settings['coverage_html_path']
    readme_path = settings['readme_path']

    with open(html_path, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        cov_table = soup.table

        h = markdownify.markdownify(str(cov_table), heading_style=markdownify.ATX)

        remove_coverage_is_exists(readme_path)
        write_coverage_in_readme(readme_path, h)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--coverage-html-path",
        default="../vsg-models/vsg-themes/htmlcov/index.html",
        type=str,
        help="Path to coverage html file"
    )
    parser.add_argument(
        "--readme-path",
        default="../vsg-models/vsg-themes/README.md",
        type=str,
        help="README file path"
    )
    args = parser.parse_args()
    all_paths = {
        'coverage_html_path': args.coverage_html_path,
        'readme_path': args.readme_path,
    }
    scrap_html(all_paths)
