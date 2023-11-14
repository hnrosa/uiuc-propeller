uiuc_propeller
==============================

Desenvolvimento de modelos substitudos para predizer a performance da hélice com base nos dados disponibilizados pela UIUC

Project Organization / Organização do Projeto
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── pages              <- secondary pages for web application.
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   ├── data_cleaning.py
    |   |   ├── data_extraction.py
    |   |   └── feature_engineering.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── studies    <- Saved studies from Hyperparameter Optimization
    │   │   ├── eval_models.py
    │   │   ├── generate_models.py
    │   │   ├── generate_studies.py
    │   │   ├── make_train_test.py
    │   │   └── generate_models.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── SurrrogateProp.py  <- Surrogate Propeller model.
    ├── Main_Page.py       <- Main web application page.
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
    


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
