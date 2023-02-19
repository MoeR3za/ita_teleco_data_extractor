# Telecom Italia 2015 Telecommunications Activity data extractor

A python script used to extract desired data from TelecomItalia Telecommunications Activity dataset


#### clone
```
git clone https://github.com/MoeR3za/ita_teleco_data_extractor.git
```
#### install
```
pip install -r requirements.exe
```
make sure script file is in the same directory as the dataset files downloaded from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/EGZHFV
#### Usage
```
    python DataExtractor.py square_id column (default: internet)
    python DataExtractor.py square_id all (all columns)
```

Script will save extracted data to a csv file in 'output' directory
