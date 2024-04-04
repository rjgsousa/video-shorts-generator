import json
import os.path

from clipsai import MediaEditor, ClipFinder, Transcriber, AudioVideoFile


class SnippetsGenerator:
    """
    A class for generating video snippets/shorts based on themes and long video.

    """
    def __init__(self, vid_path: str, themes_path: str, project_name: str, clips_out_path: str):
        """

        Args:
            vid_path: path for the video
            themes_path: path for the file containing the project theme/keywords
            project_name: the name of the project
            clips_out_path: the path where the generated vsg_clips where be written
        """

        self.vid_path = vid_path
        self.themes_path = themes_path
        self.project_name = project_name
        self.clips_out_path = clips_out_path
        self.clipsai_transcription_path = \
            os.path.join(
                self.clips_out_path,
                self.project_name,
                "clipsai_transcription.json"
            )

        # init transcriber
        self.transcriber = Transcriber(precision='int8')

        # the following variables are going to be defined
        # in specific parts of the code
        self.clips_information = None

    def _get_clean_transcription(self, media_path):
        editor = MediaEditor()
        media_file = editor.instantiate_as_temporal_media_file(media_path)

        transcription = self.transcriber._model.transcribe(
            media_file.path, language=None, batch_size=8

        )
        return transcription

    def _process(self):
        transcription = self.transcriber.transcribe(audio_file_path=self.vid_path)

        # save transcription
        transcription.store_as_json_file(self.clipsai_transcription_path)

        clip_finder = ClipFinder(
            min_clip_duration=30,
            max_clip_duration=90,
        )
        clips = clip_finder.find_clips(transcription=transcription)

        self.clips_information = {'vsg_clips': clips, 'transcription': transcription}

    def _generate(self):
        if not self.clips_information:
            raise ValueError('You need to process the video first before generating vsg_clips')

        media_editor = MediaEditor()
        media_file = AudioVideoFile(self.vid_path)

        for pos, clip in enumerate(self.clips_information.get('vsg_clips')):
            if pos == 0:
                pass

            # path where trimmed videos/snippets/shorts will be saved
            filename = f"{pos:04d}"
            path = f"{os.path.join(self.clips_out_path, self.project_name)}/{filename}.mp4"
            _ = media_editor.trim(
                media_file=media_file,
                start_time=clip.start_time,
                end_time=clip.end_time,
                trimmed_media_file_path=path,
            )

            transcription = self._get_clean_transcription(path)

            # save partial transcription
            partial_transcription_path = \
                f"{os.path.join(self.clips_out_path, self.project_name)}/{filename}_transcription.json"
            with open(partial_transcription_path, "w") as file:
                json.dump(transcription, file, indent=4)

    def process_and_generate(self):
        # identify all relevant vsg_clips
        self._process()

        # trim video based on the vsg_clips
        self._generate()
