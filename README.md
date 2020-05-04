# 576clicr

The project contains two Phases - Phase 1 and Phase 2 

Phase 1 contains

1. "Analysis" that contains the analysis we performed both on CliCR and SQuAD v1.1 datasets. This is a breif  description of the 

  1.1 Analysis.ipynb file

 We observed that CliCR dataset is quite different from SQuAD dataset, and have made changes to CliCR dataset to bring it to SQuAD format. The changes we have made are briefly explained here -

  We are storing "start position of character of answer text" that SQuAD makes you of which is not there in CliCR dataset.
  We have kept only one answer for each query in CliCR (where we had multiple answers earlier which are synonyms, acronyms of the actual   answer) that can be found from the context (case report). We added a new variable ”is_impossible" which stores the boolean value of     whether an answer can be exactly found in the context or not. Other minor name changes are made to bring our dataset to convert the     data into SQuAD v1.1 format.

   We have also observed that out of 
   - 91344 queries we have in our training set, all the queries have an answer with origin as dataset and 40283 of those have an answer     that cannot be exactly found in the context or case report
   - 6391 queries we have in our development set, all of them have an answer with origin as dataset and 2833 of those have an answer          that cannot be exactly found in the context or case report
   - 7184 queries we have in test set, all of them have an answer with origin as dataset, and 3266 of them have an answer that cannot be      found in the context
   
  As SQuAD v1.1 dataset contains only questions for which an exact answer can be found in the passage, we have removed all such queries   for which we cannot find an answer in the passage
    
  1.2 SquadAnalysis.ipynb 

  We have another file in this folder with the name SquadAnalysis.ipynb that contains the analysis we have done on SQuAD v1.1 dataset.     It is mostly to understand the variables that SQuAD makes use of and whether we can answer the question from the given context or not
  
 
2. "BERT" that contains the BERT model files we have used from the https://github.com/huggingface/transformers repo . We have made changes in these files according to our dataset. The model description details and results we have achieved is clearly explained in our report. For more details about the files we have in this folder, please visit the huggingface transformers github repository.

Command to run BERT -

python run_squad.py
--model_type bert \
--do_eval \
--model_name_or_path  bert-base-uncased \
--do_lower_case \
--train_file bert_train.json \
--predict_file bert_dev.json \
--per_gpu_train_batch_size 16 \
--learning_rate 3e-5 \
--num_train_epochs 2.0  \
--max_seq_length 128 \
--gradient_accumulation_steps 2  \
--doc_stride 32 \
--output_dir output_bertbase_clicr_bert \
--logging_steps 5000 \
--save_steps 5000 \

In the above command -
"train_file" and "predict_file" arguments takes path of train and dev files respectively.
"output_dir" takes the path of the output directory where train checkpoints and predictions of the model will be stored

Additionally,
we have made a script "data.py" using which we performed analysis on our dataset. This file returns the context, query and answer that can  be found in the passage. We have done the analysis by picking one case report each in training, development and test set. The screenshots of the outputs can be seen in Analysis folder of this repo

Phase 2 contains

Analysis file similar to phase 1 that contains the analysis and code we have used to prepare the version 2 of clicr data that is similar to squad v2.0

Summarization folder contains the contexthelper.py file that performs extractive summarization and returns the summarized context that the model makes use of to predict an answer. It reduces the search space for the model and forces it to find an answer in the reduced context rather than the whole context. 

Samples folder contains one sample each of the following types -
1. Actual answer is not empty and predicted answer is not empty
2. Actual answer is empty and predicted answer is not empty
3. Actual answer is empty and predicted answer is empty
4. Actual answer is not empty and predicted answer is an empty string

We have performed analysis on the above mentioned samples and observed that if the query and answer is not present in the same sentence, the model is returning an empty string. That count is given by the number of queries for which actual answer is not empty and can be found verbatim in the passage and predicted answer is empty. For the cases where the length of the predicted answer is more than the actual answer, we have done summarization by forcing the model to predict from a list of sentences rather than the entire context thereby reducing the noise and increasing the accuracy.

We have used 4 different versions of the clicr dataset and have performed our experiments on 5 different models.
1. Bert Large Uncased
2. Bert Large Wholeword Masking
3. BioBERT Large
4. BioBERT Base (Pubmed + PMC)
5. BioBERT (Pretrained on Squad Train set)

We have the following types of datasets.
                                            
Type 1 (Only one gold answer)
                                              
Version 1.1 - contains only those queries for which an answer can be found in the dataset
Version 2.0 - contains all the queries irrespective of whether an answer can be found in the dataset or not

Type 2 (Multiple gold answers)

Version 1.1 - contains only those queries for which an answer can be found in the dataset, but a query can have more than one gold answer.
Version 2.0 - contains all the queries irrespective of whether an answer can be found in the dataset or not. If an answer can be found verbatim in the passage for a query, such queries have more than one gold answer. If not, the gold answer for such queries is stored as an empty string.

We have ran the models on Google Colab using TPU. We have followed this link https://www.pragnakalp.com/nlp-tutorial-setup-question-answering-system-bert-squad-colab-tpu/ to setup a BERT QA system using TPU. Once the system is set, the following command is used 

!python bert/run_squad.py \
  --vocab_file=$BUCKET_NAME/biobert_large/vocab_cased_pubmed_pmc_30k.txt \
  --bert_config_file=$BUCKET_NAME/biobert_large/bert_config_bio_58k_large.json \
  --init_checkpoint=$BUCKET_NAME/biobert_large/bio_bert_large_1000k.ckpt \
  --do_train=True \
  --train_file=Summarizedv1/bert_train.json \
  --do_predict=True \
  --predict_file=Summarizedv1/bert_dev.json \
  --train_batch_size=24 \
  --learning_rate=3e-5 \
  --num_train_epochs=2.0 \
  --use_tpu=True \
  --tpu_name=grpc://10.47.230.114:8470 \
  --max_seq_length=384 \
  --doc_stride=128 \
  --version_2_with_negative=True \
  --output_dir=$OUTPUT_DIR
  
  run_squad.py file is used from the BERT repository provided by the authors of the BERT paper. Predictions file is stored in the directory that is passed to output_dir argument. Depending on the version of the dataset used, the following steps need to be taken to get EM and F1 scores.
  
For v1.1,
ClicrMetrics file is a python notebook that returns the EM and F1 scores when given a development set and prediction file as input.

For v2.0,
The following command should be run

python eval2.0.py  'testfile'  'predictionsfile'

  
 
