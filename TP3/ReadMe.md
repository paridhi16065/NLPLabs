Instructions for running programs
Both scripts can be run by using the standard python command but will have to replace the file path where train and test files are specified
In spacy_tp3.py replace the filepath in test_file_2LetterLanguageSuffix with corresponding test file path in your system for each language (language code section indicated by comment)
Similarly in crf_tp3.py replace filepath in train_sentences and test_sentences variables with corresponding train and test file paths

Running time
The pretrained model computes the predictions and the classification report within 10 seconds for each language
The model trained by me takes just under 2 minutes to run for each language (due to extra time taken for training. Although I have constrained maximum iterations during training to 20 to keep running time low, although it affects fscore a bit)

Options selected for running spacy
I used the spacy library for running the pretrained models
For languages where a pretrained model was available I used that model
pt_core_news_sm for portuguese
zh_core_web_sm for chinese
sv_core_news_sm for swedish
hr_core_news_sm for croatian
en_core_web_sm for english
da_core_news_sm for danish

for slovak and serbian, I used xx_ent_wiki_sm  
