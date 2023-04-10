# transcription_and_summarization

Nowadays, we have access to a large amount of data resources. It is
difficult and time-consuming for human beings to extract the summary
of these large lectures manually. So, summarization can also help
improve document indexing for information retrieval. These
summarizers can generate a summary from long text data available.
Now, if we add a transcriber before these summarizers, then our system
will now generate summarized text of input data, whether it be audio,
video, or text.
“Transcriber and Summarize” is a python-based software designed to
generate summaries. We can give audio/video or text as input, and the
project will give a summarized text as output. The software will help
the learners get important information from large and lengthy data
materials.

**Transcription** - 
Speech recognition is the ability of software to identify words and
phrases in spoken language and convert them to human-readable
text. The transcribe feature converts speech to a text transcript. In
our Project, the user will have the option to enter either a text or
audio/video file. If the input is video, the first task is to extract the
audio from it, and then some modifications and pre-process are
done on the file (this is done to increase the accuracy). These
modifications include converting audio to .wav format, finding the
frame rate of the file, and converting it to stereo. This audio file
will then go through the transcriber.
Our transcriber uses the Google Speech-to-Text API to get the text
with proper speaker diarization and punctuation. Google Speech-
to-Text has been trained on various kinds of resources under
different conditions. It uses less time and, according to May 2020
benchmark on statista.com, also has an accuracy rate of 84 percent.



**Summarization**
Text summarization refers to the shortening of long pieces of text.
The intention is to create a fluent and coherent summary having
only the main points outlined in the document. Applying text
summarization reduces reading time, accelerates the process of
researching for information, and increases the amount and quality
of information that can fit in a given space. In our project, the text
acts as input for the summarizer, and the output is the summarized
text. The Content of this summary is based on input data.
In general, there are two types of summarizations, abstractive and
extractive summarization. The limited study is available for
abstractive summarization as it requires a deeper understanding of
the text as compared to the extractive approach.
In our project, we are going to focus on abstractive summarization.
This has been achieved by fine-tuning BART Model for English
Text Summarization. BART is a transformer encoder-encoder
(seq2seq) model with a bidirectional encoder and a decoder.

BART is pre-trained by:
1. Corrupting text with an arbitrary noising function, and
2. Learning a model to reconstruct the original text.

BART is particularly effective when fine-tuned for text generation
or comprehension tasks. We have used BART-large as our initial
point.

The model used in our project has been trained on CNN, XSUM,
and SAMSum datasets. And can summarize various types of text
including multiple-speaker, single-speaker or any descriptive text.

Steps for Fine-Tuning
1. Prepare the data and import it along with the mode.
2. The next step is handling where we specify the task, creating
a mini-batch of input and targets, etc.
3. In training, the learner function and loss functions are created.
4. After this, the model gets created that we can use for
summarization.
 
 

**PROPOSED WORK**

PREPOCESSES -
For our transcription work, we have used Speech-to-Text API by
Google. Google has trained these speech recognition models for
specific audio types and sources.
Like for any NLP task, an advanced model can be used as a starting

point. We have used BART-large as our initial point and then fine-
tuned it for processing summarization.

ALGORITHM DESIGN -
The flow of the project consists of the following steps:
1. Created frontend UI of the app.
2. Taking input type (audio/video/text) from user.
3. Taking input file.
4. Use google API to find the transcript of the file. (If required)
5. Run the Summarization model to find a summary.
6. Provide transcript and summary file as output
On the output UI page, user will have the option to check the ROUGE
score of summarizations.
