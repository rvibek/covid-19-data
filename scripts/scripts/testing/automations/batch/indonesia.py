import requests
import pandas as pd

from cowidev.testing import CountryTestBase


class Indonesia(CountryTestBase):
    location: str = "Indonesia"

    def export(self):
        url = "https://data.covid19.go.id/public/api/pemeriksaan-vaksinasi.json"
        data = requests.get(url).json()

        df = pd.DataFrame(data["pemeriksaan"]["harian"])

        df["Cumulative total"] = df.jumlah_orang_pcr_tcm_kum.apply(
            lambda x: x["value"]
        ) + df.jumlah_orang_antigen_kum.apply(lambda x: x["value"])

        df = (
            df[["key_as_string", "Cumulative total"]]
            .rename(columns={"key_as_string": "Date"})
            .sort_values("Date")
            .drop_duplicates(subset=["Cumulative total"], keep="first")
        )

        df["Country"] = "Indonesia"
        df["Units"] = "people tested"
        df["Source URL"] = "https://covid19.go.id/peta-sebaran"
        df["Source label"] = "Government of Indonesia"
        df["Notes"] = pd.NA

        self.export_datafile(df)


def main():
    Indonesia().export()


if __name__ == "__main__":
    main()
