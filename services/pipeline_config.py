"""Load pipeline.yaml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class SourceConfig:
    type: str
    query_name: str | None = None


@dataclass
class TargetConfig:
    mysql_table: str
    load_mode: str
    primary_key: list[str] = field(default_factory=list)


@dataclass
class JobConfig:
    id: str
    enabled: bool
    refresh_interval_seconds: int
    source: SourceConfig
    target: TargetConfig
    column_map: dict[str, str] = field(default_factory=dict)


def load_pipeline_config(path: Path) -> list[JobConfig]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not raw or "jobs" not in raw:
        return []
    jobs: list[JobConfig] = []
    for j in raw["jobs"]:
        s = j["source"]
        t = j["target"]
        jobs.append(
            JobConfig(
                id=j["id"],
                enabled=bool(j.get("enabled", True)),
                refresh_interval_seconds=int(j.get("refresh_interval_seconds", 3600)),
                source=SourceConfig(
                    type=s["type"],
                    query_name=s.get("query_name"),
                ),
                target=TargetConfig(
                    mysql_table=t["mysql_table"],
                    load_mode=t.get("load_mode", "replace"),
                    primary_key=list(t.get("primary_key") or []),
                ),
                column_map=dict(j.get("column_map") or {}),
            )
        )
    return jobs
