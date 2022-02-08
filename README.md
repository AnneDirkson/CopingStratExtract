# Coping Strategy Extraction
## Pipeline to extract coping strategies for side effects from medical social media. 

Under /src are the scripts and requirements for extracting coping strategies from medical social media. View the example-data file to see the required format for input data.
Aside from the packages in requirements.txt, it is also necessary to download a spacy model with: 

python -m spacy download en_core_web_sm

Under /annotation, are the different annotation guidelines for labelling NER, labelling relations between side effects and coping strategies and for labelling the extracted concepts with ontology labels.

Under /dashboard, one can find the scripts and requirements to generate a visualization of the results obtained in the pipeline. 

Here is a small demo of the visualization:
https://www.loom.com/share/dda9794a0d354589b95e5b01b5ab23a5

The ontology (coping_strategy_v3.rdf) was created in owlready2 (python). IT can be viewed in python using owlready or with Protege. It is also available HERE> 

We also provide the conversion file (dictionary_CSix_labels) to view how the labels in the ontology (which reflect the origin of the label i.e. which ontology it was sourced from) are converted into labels for the extraction. Not all labels were included as target labels during extraction. 
