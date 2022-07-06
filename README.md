# ML Slack Bots

Examples of Slack Bots that runs ML tasks via [Replicate](https://replicate.com/docs/api), [Hugging Face](https://huggingface.co/inference-api) and [OpenAI](https://beta.openai.com/).

Supported models:

- [dalle-mini](https://replicate.com/borisdayma/dalle-mini)
- [min-dalle](https://replicate.com/kuprel/min-dalle)
- [cogview2](https://replicate.com/thudm/cogview2)
- [latent-diffusion](https://huggingface.co/spaces/multimodalart/latentdiffusion)

## How to use

### Setup AWS Lambda

- Rename example.env to .env and fill it with your own API keys.
- Run make_package.sh and upload .zip to lambda function.

### Setup Slack App

- TBD
