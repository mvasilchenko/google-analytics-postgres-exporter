from dataclasses import dataclass
from typing import List

import yaml


@dataclass
class GoogleAnalyticsCredentials:
    client_id: str
    private_key: str


@dataclass
class GoogleAnalyticsAccount:
    account: str
    webproperty: str
    profile: str


@dataclass
class Metric:
    metrics: List[str]
    dimensions: List[str]
    start_date: str
    end_date: str


class Settings:
    def __init__(self, yaml_file: str):
        self.yaml_file = yaml.load(open(yaml_file))

    @property
    def credentials(self):
        for record in self.yaml_file:
            if record.get("id", False) == "credentials":
                return GoogleAnalyticsCredentials(
                    client_id=record["client_email"], private_key=record["private_key"]
                )

    @property
    def accounts(self):
        accounts = []
        for record in self.yaml_file:
            if record.get("id", False) == "ga settings":
                accounts.append(
                    GoogleAnalyticsAccount(
                        account=record["account"],
                        webproperty=record["webproperty"],
                        profile=record["webproperty"],
                    )
                )
        return accounts

    @property
    def metrics(self):
        metrics = []
        for record in self.yaml_file:
            if record.get("metrics"):
                metrics.append(Metric(**record["attributes"]))
        return metrics
