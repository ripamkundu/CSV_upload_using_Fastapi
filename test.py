from fastapi import FastAPI, UploadFile, File, HTTPException
import csv

app = FastAPI()
data_store = []


def process_csv(file):
    try:
        decoded_file = file.file.read().decode("utf-8").splitlines()
        csv_reader = csv.DictReader(decoded_file)
        for row in csv_reader:
            data_store.append(row)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        process_csv(file)
        return {"detail": "CSV file successfully uploaded and processed"}
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file format. Only CSV files are allowed."
        )


@app.get("/data/")
async def get_data():
    return data_store
