This contains the Python script that is used to finetune Google's T5 for sequence to sequence translation of risk indicators to risk statements. A demo of the finetuned model can be tested at 
To use this locally:
* Download the T5-small model from hugging face ([https://huggingface.co/t5-small](https://huggingface.co/t5-small)) to your project directory and change the aboslute folder path references currently in the code. Alternatively, you can use the transformers pretrainined functions to work with the remote model repo. 
* Update the output path (second to last line of code) to a folder on your machine.
* Adjust training arguments as neeed (e.g., fewer epochs to speed up finetuning)
