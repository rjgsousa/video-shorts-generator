import json
import argparse
from vsg_themes.extract.from_web import get_data_from_url, load_json_data
from vsg_themes.analysis.keywords import Keywords


def main(arguments):
    url = arguments.website
    output_file = arguments.outfile

    # get data from url
    get_data_from_url(url, output_file)

    # load data from a file
    data = load_json_data(output_file)

    # perform analysis
    content = data.get('content', '')

    outfile_themes_path = arguments.outfile_themes
    kw = Keywords()
    kw.conduct_analysis_and_create_report(content, outfile_themes_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--website",
                        default="https://www.notta.ai/en", type=str, help="website to extract html")
    parser.add_argument("--outfile",
                        default="data/external/notta.json", type=str, help="json file of the website")
    parser.add_argument("--outfile_themes",
                        default="data/external/notta_themes.json", type=str, help="json file of the website")
    args = parser.parse_args()

    main(args)
