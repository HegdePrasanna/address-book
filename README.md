# Address Book
Welcome to the Address Book, a FastAPI service for simple Address Storage


## How to Run in Local Machine
To clone this repository, use the following command:
```bash
git clone https://github.com/HegdePrasanna/address-book.git
```

Create Anaconda Environment
```bash
conda env create -f environment.yml
```

Activate Conda Environment
```bash
conda activate addressportal
```

Run the APIs
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Swagger Documentation
The APIs are deployed on AWS and can be accessed using [this link](http://localhost:8000/api/docs/)
```bash
http://localhost:8000/api/docs/
```

## Features
1. Anybody Can Create New Address
2. Addresses Can be Updated and Retrieved only if they are created from the Same IP Address
3. Fetch the Nearby Locations