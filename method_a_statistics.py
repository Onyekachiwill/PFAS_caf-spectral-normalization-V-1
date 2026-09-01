import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MethodAStatistics:

    def __init__(self, output_folder):

        self.output_folder = output_folder

        os.makedirs(output_folder, exist_ok=True)


    def summary(self, dataframe):

        summary = dataframe.groupby("Sample")["ACaF_ARef"].agg(

            Count="count",
            Mean="mean",
            Median="median",
            Std="std",
            Min="min",
            Max="max"

        )

        summary.to_csv(

            os.path.join(
                self.output_folder,
                "SummaryStatistics.csv"
            )

        )

        return summary
    
    def histogram(self, dataframe):

        plt.figure(figsize=(8,5))

        for sample in dataframe["Sample"].unique():

            values = dataframe.loc[
                dataframe["Sample"] == sample,
                "ACaF_ARef"
            ]

            plt.hist(
                values,
                bins=20,
                alpha=0.5,
                label=sample
            )

        plt.xlabel("ACaF / ARef")
        plt.ylabel("Frequency")

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            os.path.join(
                self.output_folder,
                "Histogram.png"
            ),

            dpi=300

        )

        plt.close()

    def boxplot(self, dataframe):

        samples = dataframe["Sample"].unique()

        data = []

        for sample in samples:

            data.append(

                dataframe.loc[
                    dataframe["Sample"] == sample,
                    "ACaF_ARef"
                ]

            )

        plt.figure(figsize=(7,5))

        plt.boxplot(

            data,

            labels=samples,

            showmeans=True

        )

        plt.ylabel("ACaF / ARef")

        plt.tight_layout()

        plt.savefig(

            os.path.join(
                self.output_folder,
                "Boxplot.png"
            ),

            dpi=300

        )

        plt.close()

    def violin(self, dataframe):

        samples = dataframe["Sample"].unique()

        data = []

        for sample in samples:

            data.append(

                dataframe.loc[
                    dataframe["Sample"] == sample,
                    "ACaF_ARef"
                ]

            )

        plt.figure(figsize=(7,5))

        plt.violinplot(

            data,

            showmeans=True,

            showmedians=True

        )

        plt.xticks(

            np.arange(1, len(samples)+1),

            samples

        )

        plt.ylabel("ACaF / ARef")

        plt.tight_layout()

        plt.savefig(

            os.path.join(
                self.output_folder,
                "ViolinPlot.png"
            ),

            dpi=300

        )

        plt.close()

    def generate(self, dataframe):

        self.summary(dataframe)

        self.histogram(dataframe)

        self.boxplot(dataframe)

        self.violin(dataframe)
