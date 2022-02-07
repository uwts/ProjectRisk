This contains all files necessary to build a docker container of the flask webapp to deploy to serverless cloud services. To deploy on Google Cloud Run, refer to their quickstart documentation at [https://cloud.google.com/run/docs/quickstarts/prebuilt-deploy](https://cloud.google.com/run/docs/quickstarts/prebuilt-deploy)

A working demo of this web app has been deployed at [https://riskgenrrun-sutjj3wk2q-uc.a.run.app/](https://riskgenrrun-sutjj3wk2q-uc.a.run.app/)

Keep in mind:
* When using the demo, upload a small txt file only (truncate to 2,000 words or less, ~4 pages)
* Demo infers on CPU (instead of GPU), can take some time to run
* Only trained the T5 sequence to sequence model on ~10 examples so there can occassionally be results that are not useful. But this also means there’s lots of potential to improve the results (generate more training examples, add more/varied gates to the pipeline to prune out nonsense).

 
