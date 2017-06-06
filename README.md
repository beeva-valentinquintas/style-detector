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

Not found response

Status 200
```
{
    "message": "Couldn't find any similarities"
}
```


Found response

Status 200
```
{
    'myself': {
        'styles': [
            {
                'style': 'hipster',
                'labels': ['beard', 'moustache'],
                'points': 2
            },
            {
                'style': 'business',
                'labels': ['necktie'],
                'points': 1
            },
            {
                'style': 'sport',
                'labels': [],
                'points': 0
            },
            {
                'style': 'geek',
                'labels': [],
                'points': 0
            }
        ],
        'image': 'ASDAJSNDANWDNAWNWNXUNWXWX...'
    },
    'twin': {
        'styles': [
            {
                'style': 'hipster',
                'labels': ['beard', 'moustache'],
                'points': 2
            },
            {
                'style': 'business',
                'labels': [],
                'points': 0
            },
            {
                'style': 'sport',
                'labels': [],
                'points': 0
            },
            {
                'style': 'geek',
                'labels': [],
                'points': 0
            }
        ],
        'image': 'PNUNADNWASDASDASDNAWNWNXU...'
    }
}
```

Test it
```
python test.py
```
