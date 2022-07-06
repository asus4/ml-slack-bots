# ML Slack Bots

Examples of Slack Bots that runs ML tasks via [Replicate](https://replicate.com/docs/api), [Hugging Face](https://huggingface.co/inference-api) and [OpenAI](https://beta.openai.com/).

![Screenshot of slack bot](https://user-images.githubusercontent.com/357497/177584534-cc971308-a357-4146-b623-0841ff8108cb.png)


Supported models:

- [dalle-mini](https://replicate.com/borisdayma/dalle-mini)
- [min-dalle](https://replicate.com/kuprel/min-dalle)
- [cogview2](https://replicate.com/thudm/cogview2)
- [latent-diffusion](https://huggingface.co/spaces/multimodalart/latentdiffusion)
- [OpenAI text-davinci-002](https://beta.openai.com/examples/)
- [erlich](https://replicate.com/laion-ai/erlich)

## Deploy this to your Slack workplace

### Setup AWS Lambda

- Rename example.env to .env and fill it with your own API keys.
- Run make_package.sh and upload .zip to lambda function.
- Upload it to AWS Lambda
- Enable `Function URL` in your lambda configuration

### Setup Slack App

- Create a new Slack App
- In Features/OAuth & Permissions, enable Scopes following:
  - `app_mentions:read`
  - `chat:write`
  - `commands`
  - `files:write`
- In Features/Event Subscriptions, add your lambda endpoint URL to the `Request URL`
- Add Slack Commands
  - /ml_dalle_mega
  - /ml_dalle_mini
  - /ml_latent_diffusion
  - /ml_cogview2
  - /ml_erlich_logo 
  - /ml_davinci

![Scopes](https://user-images.githubusercontent.com/357497/177586091-4fcb4062-4869-4f38-a09d-49556d8f8f20.png)
