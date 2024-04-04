import argparse

from vsg_gen.blog.llm_article import BlogGenerator


def main(arguments):
    transcription = arguments.transcription_path
    project_description = arguments.project_description_path
    out_path = arguments.blog_out_path
    models_path = arguments.models_path
    project_name = arguments.project_name
    clip_number = arguments.clip_number

    generator = BlogGenerator(
        project_name,
        clip_number,
        transcription,
        project_description,
        models_path,
        out_path
    )
    generator.gen_blog_article()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--transcription_path",
                        default="data/processed/nottaai/0001_transcription.json",
                        type=str,
                        help="json file of the website")
    parser.add_argument("--clip_number",
                        default="6",
                        type=int,
                        help="json file of the website")
    parser.add_argument("--project_description_path",
                        default="data/external/notta.json",
                        type=str,
                        help="json file of the website")
    parser.add_argument("--project_name",
                        default="nottaai",
                        type=str,
                        help="json file of the website")
    parser.add_argument("--blog_out_path",
                        default="data/processed/",
                        type=str,
                        help="json file of the website")
    parser.add_argument("--models_path",
                        default="models/",
                        type=str,
                        help="json file of the website")
    args = parser.parse_args()

    main(args)
