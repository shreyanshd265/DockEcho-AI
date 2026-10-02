import keras_hub
from src.config import MODEL_PRESET,ENCODER_LENGTH,DECODER_LENGTH,MAX_SUMMARY_LENGTH,CHUNK_WORD_LIMIT

def load_model():
    preprocessor=keras_hub.models.BartSeq2SeqLMPreprocessor.from_preset(
        MODEL_PRESET,
        encoder_sequence_length=ENCODER_LENGTH,
        decoder_sequence_length=DECODER_LENGTH
    )
    model=keras_hub.models.BartSeq2SeqLM.from_preset(
        MODEL_PRESET,
        preprocessor=preprocessor
    )
    return model



def summarize_chunk(model,chunk):
    generated_summary=model.generate(
        {"encoder_text":[chunk], "decoder_text":[""]},
        max_length=MAX_SUMMARY_LENGTH
    )
    return generated_summary[0]

def summarize_full_text(model,chunks):
    generated_summaries=[]
    for i in range (len(chunks)):
        mid_string=summarize_chunk(model,chunks[i]);
        generated_summaries.append(mid_string)
    final_ans=" ".join(generated_summaries)
    if (len(final_ans.split())>CHUNK_WORD_LIMIT):
        final_ans=summarize_chunk(model,final_ans)
    return final_ans

##if __name__ == "__main__":
    model = load_model()
    print("model loaded successfully")

    from src.pdf_utils import extract_text_from_pdf, clean_text, chunk_text

    raw_text = extract_text_from_pdf("src/MYOS.pdf")
    cleaned = clean_text(raw_text)
    chunks = chunk_text(cleaned, CHUNK_WORD_LIMIT)

    final_summary = summarize_full_text(model, chunks)
    print("the final summary created successfully")
    from src.tts import text_to_speech, translate_text
    language=input("enter the language in which you want the summary?")
    lang_dictionary={"english":"en","hindi":"hi","french":"fr","tamil":"ta","japanese":"ja"};
    code_of_language=lang_dictionary[language.lower()]
    if code_of_language != "en":
        final_summary = translate_text(final_summary, code_of_language)
    output_path = text_to_speech(final_summary, code_of_language)
    print("the audio file saved successfully")