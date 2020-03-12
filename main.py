from os import environ

import googleanalytics as ga
from sqlalchemy import create_engine
import pandas as pd
from settings import Settings, Metric


class PostgresMaster:
    def __init__(self, postgres_url: str):
        self.engine = create_engine(postgres_url)


class GoogleAnalyticsQueryMaster:
    def __init__(self, yaml_file: str):
        self.settings = Settings(yaml_file)
        self.accounts = ga.authenticate(
            client_email=self.settings.credentials.client_email,
            private_key=self.settings.credentials.private_key,
        )

    @staticmethod
    def query(query: Metric, profile) -> dict:
        return (
            profile.core.query.set(metrics=query.metrics)
            .set(dimensions=query.dimensions)
            .set("start_date", query.start_date)
            .set("end_date", query.end_date)
            .as_dataframe()
        )


def main():
    G = GoogleAnalyticsQueryMaster(environ["SETTINGS_FILE"])
    P = PostgresMaster(environ["POSTGRES_URL"])
    for ga_account in G.settings.accounts:
        profile = (
            G.accounts[ga_account.account]
            .webproperties[ga_account.webproperty]
            .profiles[ga_account.profile]
        )
        for metrics in G.settings.metrics:
            df = pd.DataFrame(G.query(metrics, profile))
            df.to_sql(metrics.table_name, P.engine, if_exists="append")


if __name__ == "__main__":
    main()
