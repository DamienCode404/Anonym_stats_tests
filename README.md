
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
## Execute the launch.py file, specifying the 3 arguments

```bash 
python3 launch.py ../data/multivariate/ ../data/CSV_output/ ../gener_simulated_data_meth/
```
## Choice of statistical tests and parameter selection

```bash 
Voulez-vous effectuer des tests stats ? (O/n): O
Voulez-vous passer par une interface graphique ? (O/n): O
```
## A graphical interface will appear, giving you a choice of several parameters

![Capture d’écran du 2024-01-02 17-57-54](https://github.com/DamienCode404/Anonym_stats_tests/assets/116463750/e6189e0e-9e02-4083-a43e-07459f5e3225)

## If you're on a server and can't display an interface

system of arguments or text files to fill in parameters
