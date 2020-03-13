import os
import re
from dataclasses import dataclass
from typing import List

import yaml


@dataclass
class GoogleAnalyticsCredentials:
    client_email: str
    private_key: str


@dataclass
class GoogleAnalyticsAccount:
    account: str
    webproperty: str
    profile: str


@dataclass
class Metric:
    table_name: str
    metrics: List[str]
    dimensions: List[str]
    start_date: str
    end_date: str


class Settings:
    def __init__(self, yaml_file: str):
        self.yaml_file = self.parse_config(path=yaml_file)

    @staticmethod
    def parse_config(path=None, data=None, tag="!ENV"):
        pattern = re.compile(".*?\${(\w+)}.*?")
        loader = yaml.SafeLoader
        loader.add_implicit_resolver(tag, pattern, None)

        def constructor_env_variables(loader, node):
            value = loader.construct_scalar(node)
            match = pattern.findall(value)  # to find all env variables in line
            if match:
                full_value = value
                for g in match:
                    full_value = full_value.replace(f"${{{g}}}", os.environ.get(g, g))
                return full_value
            return value

        loader.add_constructor(tag, constructor_env_variables)

        if path:
            with open(path) as conf_data:
                return yaml.load(conf_data, Loader=loader)
        elif data:
            return yaml.load(data, Loader=loader)
        else:
            raise ValueError("Either a path or data should be defined as input")

    @property
    def credentials(self):
        for record in self.yaml_file:
            if record.get("id", False) == "credentials":
                return GoogleAnalyticsCredentials(
                    client_email=record["client_email"],
                    private_key=record["private_key"],
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
                        profile=record["profile"],
                    )
                )
        return accounts

    @property
    def metrics(self):
        metrics = []
        for record in self.yaml_file:
            if record.get("metrics"):
                metrics.append(
                    Metric(**record["attributes"], table_name=record["metrics"])
                )
        return metrics
