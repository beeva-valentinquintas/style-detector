## Style detector

#### Up & Running

Set Google Cloud service credentials
```
export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE
```
Install Google Cloud SDK [documentation](https://cloud.google.com/sdk/docs/)

Authenticate to use your local machine
```
gcloud auth application-default login
```

Generate virtual environment
```
virtualenv -p python2 virtual_env_folder
source virtual_env_folder/bin/activate
cd modernometro
pip install -r requirements.txt
```

Run it
```
python main.py
```
Your API id running on port 5000

#### Endpoints

###### /labels
