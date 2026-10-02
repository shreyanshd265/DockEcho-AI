# DocEcho.AI 📄🔊

**Live app:** https://dockecho-ai-o5sbuo7hxcnb5ojxkzgqvd.streamlit.app/

I built this project to learn how fine-tuning actually works in practice — not just reading about it, but taking a pretrained model, training it on real data, dealing with real deployment headaches, and shipping something that works end to end.

DocEcho.AI takes a PDF, summarizes it using a BART model I fine-tuned myself, and reads the summary out loud.

## What it does

1. You upload a PDF
2. The app pulls out the text and cleans it up
3. If the document is long, it's split into chunks, each chunk gets summarized, and then those summaries get combined and condensed one more time if needed
4. You get a text summary plus an audio version you can play right in the browser

## Tech stack

- **Model:** BART-base, fine-tuned with KerasHub (TensorFlow)
- **Dataset:** CNN/DailyMail (news articles paired with human-written summaries)
- **PDF handling:** pdfplumber
- **Text-to-speech:** gTTS
- **App + hosting:** Streamlit, deployed on Streamlit Community Cloud
- **Model hosting:** Hugging Face Hub

## How I trained it

I fine-tuned `facebook/bart-base` on 10,000 articles from CNN/DailyMail (with 1,000 held out for validation), for 2 epochs, using early stopping so it wouldn't overfit if things went sideways. All training happened on Google Colab's free GPU.

I didn't train on the full 287,000-article dataset — that would've taken way longer than was realistic on free compute. 10,000 examples felt like a fair middle ground: enough to actually fine-tune the model, small enough to finish without burning through Colab sessions for days.

## Did fine-tuning actually help? (ROUGE scores)

I ran both my fine-tuned model and the plain, un-fine-tuned base model on the same 50 test articles and compared them with ROUGE:

| Metric | Fine-tuned | Base model |
|---|---|---|
| ROUGE-1 | 0.296 | 0.277 |
| ROUGE-2 | 0.091 | 0.129 |
| ROUGE-L | 0.211 | 0.199 |
| ROUGE-Lsum | 0.274 | 0.230 |

Honestly, the results are mixed. Fine-tuning helped a bit on most metrics but actually did slightly worse on ROUGE-2. My best guess is that `bart-base` already comes with decent summarization ability baked in from pretraining, so 10,000 examples over a couple of epochs only nudges it a little rather than transforming it. I'd expect a bigger gap with more training data or more careful tuning — something I'd like to revisit.

## Something interesting I found

The model is noticeably better at summarizing **news-style writing** than **stories**. I tested it on Aesop's "The Tortoise and the Hare" and the summary grabbed surface details (who's in it, that there's a race) but completely missed the actual point of the story — the hare napping, the tortoise winning, the moral. Makes sense once you think about it: it was only ever trained on news articles, which read nothing like a fable. It's a good reminder that a fine-tuned model is only as flexible as the data you trained it on.

## Project layout


docecho-ai/
├── src/
│ ├── config.py # settings — model path, sequence lengths, chunk size
│ ├── pdf_utils.py # extracting and cleaning text from PDFs, chunking
│ ├── summarizer.py # loading the model, generating summaries
│ └── tts.py # turning text into audio
├── app.py # the Streamlit app itself
├── requirements.txt
└── NLP_experiments.ipynb # the full training/evaluation notebook from Colab


## Running it yourself

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What I'd do next if I kept going

- Train on more data and see if the gap over the base model actually widens
- Try to make it work decently on non-news text, maybe by mixing in a different dataset
- Look into quantizing the model to cut down its memory footprint
- I actually built multi-language audio output (translate the summary, then speak it in that language) but pulled it out — the free translation API kept hitting rate limits and silently failing, which felt worse than just not having the feature. Would be worth redoing properly with a paid translation API.

## A few things I ran into along the way

Deployment was honestly the hardest part of this whole project — harder than the actual ML. A few highlights:
- Windows kept breaking file paths when loading the model from Hugging Face (a backslash-vs-forward-slash bug deep in a library)
- Streamlit Community Cloud kept defaulting to a brand-new Python version that didn't have compatible TensorFlow wheels yet — had to manually pick an older Python version in the deploy settings to fix it
- `deep-translator`'s free tier turned out to be way too rate-limited to rely on, which is why the multi-language feature didn't make the final cut

None of this showed up in any tutorial I read beforehand — figuring it out was most of the learning.