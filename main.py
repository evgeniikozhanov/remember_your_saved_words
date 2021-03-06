import csv
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from models import SavedWord


class UploadWordsPairsRequest(BaseModel):
    filename: str


app = FastAPI()


@app.post("/upload/")
async def upload_words_pairs(upload_words_pairs_request: UploadWordsPairsRequest):
    inserting_date = datetime.now()
    with open(upload_words_pairs_request.filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        objects_list = []
        for from_language, to_language, from_word, to_word in csv_reader:
            objects_list.append(SavedWord(from_language=from_language, to_language=to_language, from_word=from_word,
                                          to_word=to_word, words_group_name=upload_words_pairs_request.filename,
                                          cdate=inserting_date))
    async with in_transaction():
        try:
            await SavedWord.filter(words_group_name=upload_words_pairs_request.filename).delete()
            await SavedWord.bulk_create(objects_list, batch_size=100)
        except OperationalError as e:
            return {'ok': False, 'errors': [str(e), ]}

    return {'ok': True, 'errors': []}


@app.on_event("startup")
async def startup_event():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
