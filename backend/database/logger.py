import json
import os
from datetime import datetime


class Logger:

    def __init__(self):

        self.file = "data/logs/analysis.json"


        os.makedirs(
            "data/logs",
            exist_ok=True
        )


    def save(self, data):

        try:

            if os.path.exists(self.file):

                with open(self.file, "r") as f:
                    logs = json.load(f)

            else:

                logs = []


            data["time"] = str(datetime.now())


            logs.append(data)


            with open(self.file, "w") as f:
                json.dump(
                    logs,
                    f,
                    indent=4
                )


        except Exception as e:

            print("Logger error:", e)