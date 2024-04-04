import json
import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle video submission
        video_file = request.files['video']
        video_path = os.path.join('static', video_file.filename)
        video_file.save(video_path)

        # Call the service to get paths of other videos
        other_videos = get_other_videos()

        return render_template('index.html', video_path=video_path, other_videos=other_videos)

    return render_template('index.html')


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def get_other_videos():
    # response = requests.get('localhost')
    videos_path = ('{"videos": ['
                   '{"loc": "0003.mp4", "transcript": "kakk"},'
                   '{"loc": "0006.mp4", "transcript": "sksksk"}]'
                   '}')
    response = MockResponse(
        json.loads(f"{videos_path}"),
        200
    )

    if response.status_code == 200:
        other_videos = response.json_data
        return other_videos

    return []


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.175")
