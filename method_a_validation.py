import os
import numpy as np
import pandas as pd


class MethodAValidation:

    def __init__(self, output_folder):

        self.output_folder = output_folder

        os.makedirs(output_folder, exist_ok=True)


    def validate(self, dataframe):

        report = []

        report.append("=" * 60)
        report.append("METHOD A VALIDATION REPORT")
        report.append("=" * 60)
        report.append("")

        report.append(f"Total Spectra Processed : {len(dataframe)}")
        report.append(f"Samples Found           : {dataframe['Sample'].nunique()}")
        report.append("")

        ##################################################
        # Missing Values
        ##################################################

        report.append("Missing Values")
        report.append("-" * 40)

        missing = dataframe.isnull().sum()

        for column, value in missing.items():

            report.append(f"{column:<20} {value}")

        report.append("")

        ##################################################
        # Zero Reference Area
        ##################################################

        zero_ref = dataframe[dataframe["ARef"] <= 0]

        report.append("Reference Area Check")
        report.append("-" * 40)

        report.append(f"ARef <= 0 : {len(zero_ref)}")

        report.append("")

        ##################################################
        # Negative CaF Area
        ##################################################

        negative = dataframe[dataframe["ACaF"] < 0]

        report.append("Negative CaF Area")
        report.append("-" * 40)

        report.append(f"Negative ACaF : {len(negative)}")

        report.append("")

        ##################################################
        # Infinite Ratios
        ##################################################

        infinite = dataframe[
            np.isinf(dataframe["ACaF_ARef"])
        ]

        report.append("Infinite Ratios")
        report.append("-" * 40)

        report.append(f"Infinite Ratios : {len(infinite)}")

        report.append("")

        ##################################################
        # NaN Ratios
        ##################################################

        nan_ratio = dataframe[
            dataframe["ACaF_ARef"].isna()
        ]

        report.append("NaN Ratios")
        report.append("-" * 40)

        report.append(f"NaN Ratios : {len(nan_ratio)}")

        report.append("")

        ##################################################
        # Sample Statistics
        ##################################################

        report.append("Sample Summary")
        report.append("-" * 40)

        grouped = dataframe.groupby("Sample")

        for sample, df in grouped:

            report.append(f"Sample : {sample}")

            report.append(f"Shots      : {len(df)}")

            report.append(f"Mean Ratio : {df['ACaF_ARef'].mean():.6f}")

            report.append(f"Std Dev    : {df['ACaF_ARef'].std():.6f}")

            report.append(f"Minimum    : {df['ACaF_ARef'].min():.6f}")

            report.append(f"Maximum    : {df['ACaF_ARef'].max():.6f}")

            report.append("")

        ##################################################
        # Outlier Detection
        ##################################################

        report.append("Potential Outliers (3σ)")
        report.append("-" * 40)

        total_outliers = 0

        for sample, df in grouped:

            mean = df["ACaF_ARef"].mean()

            std = df["ACaF_ARef"].std()

            if std == 0 or np.isnan(std):

                continue

            outliers = df[
                np.abs(df["ACaF_ARef"] - mean) > 3 * std
            ]

            total_outliers += len(outliers)

            report.append(f"{sample:<15} {len(outliers)}")

        report.append("")
        report.append(f"Total Outliers : {total_outliers}")
        report.append("")

        ##################################################
        # Save Report
        ##################################################

        filename = os.path.join(
            self.output_folder,
            "MethodA_Validation_Report.txt"
        )

        with open(filename, "w") as file:

            file.write("\n".join(report))

        print("\nValidation report saved:")
        print(filename)

        return filename