from fastapi import APIRouter, File, UploadFile, HTTPException
from database.connections import connect
import pandas as pd
import io

router = APIRouter(prefix="/Upload Data", tags=["Upload Data"])


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    try:
        conn = connect()
        cursor = conn.cursor()
        upload_csv_query = """
            INSERT INTO upload (merchant_id, mCode, name, type, PhoneNo, bank, account_number, ifsc_code, amount, fundTransferType)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        for index, row in df.iterrows():
            cursor.execute(
                "SELECT COUNT(*) FROM upload WHERE merchant_id = %s",
                (row["merchant_id"],),
            )
            count = cursor.fetchone()[0]
            if count == 0:  # If merchant_id does not exist, insert the row
                cursor.execute(upload_csv_query, tuple(row))
        conn.commit()
        return {"status": "file uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

    finally:
        cursor.close()
        conn.close()
