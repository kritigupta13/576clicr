# 576clicr

This file describes the significance of each our repository and the details of each file

We have a folder named 

1. "Analysis" that contains the analysis we performed both on CliCR and SQuAD v1.1 datasets. This is a breif  description of the 

  1.1 Analysis.ipynb file

  We observed that CliCR dataset is quite different from SQuAD dataset, and have made changes to CliCR dataset to bring it to SQuAD format.
  The changes we have made are briefly explained here -

    We are storing "start position of character of answer text" that SQuAD makes you of which is not there in the first place in CliCR
    We have kept only one answer for each query in CliCR (where we had multiple answers earlier which are synonyms of the actual answer)
    that can be found from the context (case report).
    We added a new variable ”is_impossible" which stores the boolean value of whether an answer can be exactly found in the context or not.
    Other minor name changes are made to bring our dataset to SQuAD v1.1 format

   We have also observed that out of 
   - 91344 queries we have in our training set, all the queries have an answer with origin as dataset and 40283 of those have an answer that
     cannot be exactly found in the context or case report
   - 6391 queries we have in our development set, all of them have an answer with origin as dataset and 2833 of those have an answer that
     cannot be exactly found in the context or case report
   - 7184 queries we have in test set, all of them have an answer with origin as dataset, and 3266 of them have an answer that cannot be found
     in the context
   
    As SQuAD v1.1 dataset contains only questions for which an exact answer can be found in the passage, we have removed all such queries for 
    which we cannot find an answer in the passage
    
  1.2 SquadAnalysis.ipynb 

  We have another file in this folder with the name SquadAnalysis.ipynb that contains the analysis we have done on SQuAD v1.1 dataset. It 
  is mostly to understand the variables that SQuAD makes use of and whether we can answer the question from the given context or not
  
 
2. "BERT" that contains the BERT model files we have used from the https://github.com/huggingface/transformers repo . We have made changes
in these files according to our dataset. The model description details and results we have achieved is clearly explained in our report.
For more details about the files we have in this folder, please visit the huggingface transformers github repository.

Command to run BERT -

python run_squad.py --model_type bert --do_eval --model_name_or_path  bert-base-uncased  --do_lower_case --train_file bert_train.json --predict_file bert_dev.json  --per_gpu_train_batch_size 16 --learning_rate 3e-5 --num_train_epochs 2.0  --max_seq_length 128  --gradient_accumulation_steps 2 --doc_stride 32 --output_dir output_bertbase_clicr_bert --logging_steps 5000 --save_steps 5000

In the above command -
"train_file" and "predict_file" arguments takes path of train and dev files respectively.
"output_dir" takes the path of the output directory where train checkpoints and predictions of the model will be stored

Command to run BioBERT -

python run_qa.py --vocab_file= vocab.txt --use_tpu=True --tpu_name=grpc://10.44.100.122:8470 --bert_config_file= config.json 
--init_checkpoint = model.ckpt --do_train=True --do_predict=True --max_seq_length=128 --train_batch_size=32 --learning_rate=5e-6 --doc_stride=32 --num_train_epochs=2.0 --do_lower_case=True --train_file bert_train.json --predict_file CSE576 bert_dev.json --output_dir output_bertbase_clicr_biobert --save_checkpoints_steps 5000 

In this command,

"train_file", "predict_file" takes path of train files, dev files respectively 
"output_dir" takes the path of output directory where train checkpoints and predictions of the model will be stored 

"vocab_file", "bert_config" and "init_checkpoint" takes vocabulary, bert configuration and model checkpoint files respectively. These files belong to BioBERT model and more information on how to download these files can be found in this repo - https://github.com/dmis-lab/biobert


Additionally,
we have made a script "data.py" using which we performed analysis on our dataset. This file returns the context, query and answer that can  be found in the passage. We have done the analysis by picking one case report each in training, development and test set. The screenshots of the outputs can be seen in Analysis folder of this repo



https://drive.google.com/drive/u/2/folders/1S6oSpvLdbs9P1g0-zFUxw6H8cLc2F5dl
  
 
