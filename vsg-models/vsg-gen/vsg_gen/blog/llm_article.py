import json
import os
from llama_cpp import Llama


class BlogGenerator:
    def __init__(self, project_name, clip_number, transcription, project_description, models_path, out_base_path):
        self.project_name = project_name
        self.clip_number = clip_number
        self.out_path = f"{os.path.join(out_base_path, self.project_name)}/{clip_number:04d}_blog.json"
        self.models_base_path = models_path
        self.model_type = "mixtral"

        # ----------------------------------------------------
        # init prior knowledge data
        # transcript of the short video
        with open(transcription, "r") as file:
            self.transcription = json.load(file)

        # company details
        with open(project_description, "r") as file:
            self.project_description = \
                json.load(file).get('content')

        # prepare data
        self._process_short_transcription()

        # initialize LLMA
        self.models_path_mistral = \
            os.path.join(
                self.models_base_path,
                self.model_type,
                "mixtral-8x7b-instruct-v0.1.Q2_K.gguf"
            )
        self.llm = Llama(model_path=self.models_path_mistral, n_ctx=4012)

    def _process_short_transcription(self):
        transcription = []
        for segment in self.transcription.get('segments'):
            transcription.append(segment.get('text'))

        transcription = " ".join(transcription)

        self.transcription = transcription

    def _save_to_file_json(self, response):
        with open(self.out_path, "w") as file:
            json.dump(response, file, indent=4)

    def gen_blog_article(self):

        prompt = (f"TASK: Rewrite the transcript of a video and write as a technical blog. "
                  f"Take into consideration the brand description. "
                  f"# Company Description\n{self.project_description}"
                  f"# Video Transcript\n{self.transcription}")

        output = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ]
        )
        self._save_to_file_json(output)
