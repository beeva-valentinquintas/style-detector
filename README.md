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
Your API is running on port 5000

#### Endpoints

###### POST /labels

Parameters

    Byte image in octect-stream format base 64 encoded

Response
```
{
  "image_stream": "ASDAISDMIAMIAWDIMWDIWMDIWD",
  "labels": [
    {
        'description': 'beard',
        'score': 0.88
    },
    {
        'description': 'tartan',
        'score': 0.65
    }
  ],
  "styles": [
    {
        'style': 'hipster',
        'label': 'beard',
        'points': 1
    },
    {
        'style': 'hipster',
        'label': 'tartan',
        'points': 1
    }
  ]
}
```
