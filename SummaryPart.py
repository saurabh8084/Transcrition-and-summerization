import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def read_transcript(transcript_filename):
    text_file = open((transcript_filepath + transcript_filename), encoding="utf8")
    transcript_text = text_file.read()
    text_file.close()
    return transcript_text


def model_summarize(text,min_len,max_len):
    print(min_len)
    tokenizer_Abs = AutoTokenizer.from_pretrained("./Project-Models/Abstractive-Approach")
    inputs_Abs = tokenizer_Abs.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    model_Abs = AutoModelForSeq2SeqLM.from_pretrained("./Project-Models/Abstractive-Approach")
    if min_len != 'None':
        outputs = model_Abs.generate(
            inputs_Abs,
            max_length=max_len,
            min_length=min_len,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True)
    else:
        outputs = model_Abs.generate(
            inputs_Abs,
            max_length=max_len,
            min_length=None,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True)

    return tokenizer_Abs.decode(outputs[0])


def write_summary(summary_filename, summary_text):
    text_file = open(summary_filepath + summary_filename, "w+")
    text_file.write(summary_text)
    text_file.close()


transcript_filepath = "./Transcripts/"
summary_filepath = "./Summary/"


def start_SummaryPart(min_ratio):
    filename = os.listdir(transcript_filepath)
    transcript_filename = filename[0]
    text = read_transcript(transcript_filename)
    max_len=len(text.split())
    #min_len=int(float(min_ratio) * max_len)
    if min_ratio=='None':
        min_len = min_ratio
    else:
        min_len=int(min_ratio)
    summary_text = model_summarize(text, min_len, max_len)
    size=len(summary_text)
    summary_text=summary_text[13:size-4]
    summary_filename = transcript_filename.split('.')[0] + '_500summary' + '.txt'
    write_summary(summary_filename, summary_text)
    txt = ''
    count=0
    i=0
    while i<len(summary_text):
        if summary_text[i] == ' ':
            count += 1
        txt += summary_text[i]
        if summary_text[i] == '.':
            if count >= 400:
                break
        i += 1
    summary_filename = transcript_filename.split('.')[0] + '_400summary' + '.txt'
    write_summary(summary_filename, txt)
    txt = ''
    count=0
    i=0
    while i<len(summary_text):
        if summary_text[i] == ' ':
            count += 1
        txt += summary_text[i]
        if summary_text[i] == '.':
            if count >= 300:
                break
        i += 1
    summary_filename = transcript_filename.split('.')[0] + '_300summary' + '.txt'
    write_summary(summary_filename, txt)
    txt = ''
    count=0
    i=0
    while i<len(summary_text):
        if summary_text[i] == ' ':
            count += 1
        txt += summary_text[i]
        if summary_text[i] == '.':
            if count >= 200:
                break
        i += 1
    summary_filename = transcript_filename.split('.')[0] + '_200summary' + '.txt'
    write_summary(summary_filename, txt)
    txt = ''
    count = 0
    i = 0
    while i < len(summary_text):
        if summary_text[i] == ' ':
            count += 1
        txt += summary_text[i]
        if summary_text[i] == '.':
            if count >= 100:
                break
        i += 1
    summary_filename = transcript_filename.split('.')[0] + '_100summary' + '.txt'
    write_summary(summary_filename, txt)
    txt = ''
    count = 0
    i = 0
    while i < len(summary_text):
        if summary_text[i] == ' ':
            count += 1
        txt += summary_text[i]
        if summary_text[i] == '.':
            if count >= 0:
                break
        i += 1
    summary_filename = transcript_filename.split('.')[0] + '_000summary' + '.txt'
    write_summary(summary_filename, txt)
    print('Summary Generated')