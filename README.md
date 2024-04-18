# VSG: Video Shorts Generator

The Video Shorts Generator (VSG) is a comprehensive solution for creating video and blog content tailored to brands that aim to increase their online presence. This project leverages technologies, including Natural Language Processing (NLP), video analysis, and generative AI, to streamline the video creation process and deliver relevant and captivating video shorts.

## Requirements

To enable themes generation, you will need fastText

```bash
wget -O models/fastText/cc.en.300.bin.gz https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz
cd models/fastText/ && gunzip cc.en.300.bin.gz
```

To enable the model for generating blog content, navigate to the project's root directory and execute the command below. For optimal performance, it is advisable to utilize this service on a GPU-equipped system.

```bash
wget -O models/mixtral/mixtral-8x7b-instruct-v0.1.Q2_K.gguf -c https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q2_K.gguf
```

## Reproducibility

1. Create a conda environment
```bash
conda create -n vsg python=3.10
conda activate vsg
```
2. Install project with `make run-experiment-standalone`

3. Check results in `data/processed/nottaai/`

## Documentation

To generate the documentation file, you first are required to have the LaTeX suite installed in our system.

1. Install the TexLive base
```bash 
sudo apt-get install texlive-latex-base
```

2. Also, it is recommended to install the recommended and extra fonts.
```bash
sudo apt install texlive-fonts-recommended
sudo apt install texlive-fonts-extra
sudo apt install latexmk
```

You must have the project installed. For that, it is suggested to have a conda environment:
```bash
conda create -n vsg python=3.10
conda activate vsg
```
Then, install "poetry" (tested with 1.8.2) and "sphinx": 
```bash
pip install -U sphinx
pip install poetry==1.8.2
make install
```

Then, at the root folder of the project `$ make documentation`

# Acknowledgements 

We would like to express our gratitude to the following individuals and organizations for their contributions to the VSG project:

1. The open-source community for providing invaluable libraries, tools, and resources that were essential in the development of this project.
2. [ClipsAI](https://github.com/ClipsAI/clipsai) for providing the groundwork for the generation of the shorts.
