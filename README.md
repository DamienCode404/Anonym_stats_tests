
# Anonym_stats_tests

The aim of this project is to anonymize a set of real patient data. This is a method frequently used in science to respect medical confidentiality. This anonymization will be used, for example, to reuse medical data for statistical testing.


## Install Python dependencies using the install.txt file

```bash
pip install -r install.txt
```
## Move to the Makefile directory and run Make

```bash
cd anonym_meth
make
```
## Try out the program with a toy version in the exemple_meth directory

```bash
python3 launch_toy_exemple.py
```
## Execute the launch.py file in the anonym_meth directory, specifying the 4 arguments

```bash 
python3 launch.py ../data/multivariate/ ../data/CSV_output/ ../gener_simulated_data_meth/ 1000
```
## Choice of statistical tests and parameter selection

```bash 
Voulez-vous effectuer des tests stats ? (O/n): O
Voulez-vous passer par une interface graphique ? (O/n): O
```
## A graphical interface will appear, giving you a choice of several parameters

![Capture d’écran du 2024-01-02 17-57-54](https://github.com/DamienCode404/Anonym_stats_tests/assets/116463750/e6189e0e-9e02-4083-a43e-07459f5e3225)

## If you're on a server and can't display an interface

Use the parametres.txt file in the anonym_meth folder to fill in the variables to launch the statistics calculation.

## OUTPUT 

# stats : 
- In this directory, you'll obtain the results of mean, maximum, minimum and standard deviation values for each physiological variable by patient (anonymous and real).

# tests : Test results for each statistic obtained from the stats folder :
- statKS,pvalKS: test statistics and Kolmogorov-Smirnov p-value.
- statWMW_p,pvalWMW_p: Wilcoxon / Mann-Whiney paired test statistic and p-value.
- statWMW_up,pvalWMW_up: test statistic and p-value of the Wilcoxon / Mann-Whiney unpaired test.
- Euclidean distance.

# dissimilarités normalisées pour chaque patient + boxplot :
- For each of the anonymous patients, a number of real patients were randomly selected (10 recommended). We then calculated the univariate DTW between anonymous and random patients for each physiological parameter (HR, SBP, MAP, DBP). We then calculated the multivariate DTW (DTWm) as the mean of the previous 4 univariate DTWs. We keep the minimum DTWm_min on the 10 real patients. We calculated the mean (E) and standard deviation (S) on all DTWm_min, normalizing each dissimilarity: normalized DTWm_min = (DTWm_min-E)/S.

# graphs :
- Graphical comparison of values obtained in the stats directory.

## Resources

- See the repo for the progress bar in the cpp section [here](https://github.com/gipert/progressbar/tree/master)
- tqdm : A Fast, Extensible Progress Bar for Python and CLI [here](https://github.com/tqdm/tqdm)
- customtkinter : A modern and customizable python UI-library based on Tkinter [here](https://github.com/TomSchimansky/CustomTkinter)
- dtaidistance : Library for time series distances [here](https://dtaidistance.readthedocs.io/en/latest/)
- numpy : The fundamental package for scientific computing [here](https://numpy.org/)
- pandas : Open source data analysis and manipulation tool [here](https://pandas.pydata.org/)
- scipy : Fundamental algorithms for scientific computing [here](https://scipy.org/)
- seaborn : Statistical data visualization [here](https://seaborn.pydata.org/)