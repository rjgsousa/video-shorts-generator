import argparse

from vsg_themes.analysis.lexical_chains import ThemeLexicalChains
from vsg_themes.analysis.theme_keywords import ThemeKeywords
from vsg_themes.analysis.theme_transformer import ThemeTransformer
from vsg_themes.extract.from_web import get_data_from_url
from vsg_utils.files import load_json_data


def main(arguments):
    url = arguments.website
    output_file = arguments.out_file_path

    # get data from url
    get_data_from_url(url, output_file)

    # load data from a file
    data = load_json_data(output_file)

    # perform analysis
    content = data.get('content', '')

    outfile_themes_path = arguments.outfile_themes_file_path
    method = arguments.method

    if method == "transformer":
        tf = ThemeTransformer()
        tf.conduct_analysis_and_create_report(content, out_file_path=outfile_themes_path)
    elif method == "tfidf":
        kw = ThemeKeywords()
        kw.conduct_analysis_and_create_report(content, outfile_themes_path)
    elif method == "lc":
        lc = ThemeLexicalChains()
        lc.build_lexical_chains(content)
        lc.extract_lexical_chains(out_file_path=outfile_themes_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--method",
                        choices=['transformer', 'tfidf', 'lc'], default="transformer", help="website to extract html")
    parser.add_argument("--website",
                        default="https://www.notta.ai/en", type=str, help="website to extract html")
    parser.add_argument("--out_file_path",
                        default="data/external/notta.json", type=str, help="json file of the website")
    parser.add_argument("--outfile_themes_file_path",
                        default="data/external/notta_themes.json", type=str, help="json file of the website")
    args = parser.parse_args()

    main(args)
