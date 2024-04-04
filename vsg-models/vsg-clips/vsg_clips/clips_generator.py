import argparse
from vsg_clips.generator.snippets_generator import SnippetsGenerator


def main(arguments):
    vid_path = arguments.video_path
    themes_path = arguments.themes_path
    proj_name = arguments.project_name
    clips_out_path = arguments.clips_out_path

    sg = SnippetsGenerator(
        vid_path=vid_path,
        themes_path=themes_path,
        project_name=proj_name,
        clips_out_path=clips_out_path
    )
    sg.process_and_generate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--video_path",
                        default="data/external/NottaAI.mp4", type=str, help="json file of the website")
    parser.add_argument("--themes_path",
                        default="data/external/notta_themes.json", type=str, help="json file of the website")
    parser.add_argument("--project_name",
                        default="nottaai", type=str, help="json file of the website")
    parser.add_argument("--clips_out_path",
                        default="data/processed/", type=str, help="json file of the website")
    args = parser.parse_args()

    main(args)

