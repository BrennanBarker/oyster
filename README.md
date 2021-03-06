# Oyster
### Oyster is a package for conducting causal inference using causal diagrams.

Unsure what "causal inference" is or what's so awesome about causal diagrams?
Check out the [walkthrough](walkthrough/0_intro_and_TOC.ipynb) for
an overview of causal inference and an explanation of Oyster's features.  

## Installation
1) Clone this repository.

    ```git clone https://github.com/BrennanBarker/oyster.git```


2) (Optional) Create a virtual environment.

    This will help keep Oyster and its dependencies separate from your other 
    packages. I recommend [pyenv+virtualenv](https://github.com/pyenv/pyenv) 
    but any environment manager (conda, etc.) will work.

3) Install the Oyster package manually using `pip`.  

    ***DO NOT FORGET THE "-e"!*** This project is not currently listed on the 
    [Python Package Index (PyPi)](https://pypi.org). There is another `oyster` 
    package on PyPi that will install instead if you forget the '-e'.

    ```pip install -e oyster```


4) (Optional) Install Jupyter Lab or Jupyter Notebook to view the walkthrough 
interactively.

    Oyster doesn't need these packages to run on its own so for the sake of 
    cleanliness they're not included as requirements.

    ```pip install jupyterlab```
  
    **OR**
    
    ```pip install notebook```
