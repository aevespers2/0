from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalBeliefPatch:
    patch_id: str
    assignments: dict[str, str]


@dataclass(frozen=True)
class SheafConsistencyReport:
    consistent: bool
    conflicts: tuple[dict[str, str], ...]


def check_sheaf_consistency(patches: tuple[LocalBeliefPatch, ...]) -> SheafConsistencyReport:
    seen: dict[str, tuple[str, str]] = {}
    conflicts: list[dict[str, str]] = []
    for patch in patches:
        for key, value in patch.assignments.items():
            if key in seen and seen[key][1] != value:
                conflicts.append(
                    {
                        "variable": key,
                        "left_patch": seen[key][0],
                        "left_value": seen[key][1],
                        "right_patch": patch.patch_id,
                        "right_value": value,
                    }
                )
            else:
                seen[key] = (patch.patch_id, value)
    return SheafConsistencyReport(not conflicts, tuple(conflicts))
