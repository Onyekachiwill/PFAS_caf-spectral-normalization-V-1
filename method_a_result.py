import os
import pandas as pd


class MethodAResults:

    def __init__(self, output_folder):

        self.output_folder = output_folder

        self.rows = []


    def add(
        self,
        sample,
        shot,
        acaf,
        aref,
        ratio
    ):

        self.rows.append({

            "Sample": sample,
            "Shot": shot,
            "ACaF": acaf,
            "ARef": aref,
            "ACaF_ARef": ratio

        })


    def save(self):

        os.makedirs(self.output_folder, exist_ok=True)

        df = pd.DataFrame(self.rows)

        df.to_csv(

            os.path.join(
                self.output_folder,
                "MethodA_Results.csv"
            ),

            index=False

        )

        return df
    
    