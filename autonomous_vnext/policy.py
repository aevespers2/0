from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from shlex import split


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class PolicyEvaluator:
    allowed_command_prefixes: tuple[tuple[str, ...], ...] = field(default_factory=tuple)
    allowed_path_prefixes: tuple[Path, ...] = field(default_factory=tuple)

    def evaluate(self, command: str) -> PolicyDecision:
        if not command.strip():
            return PolicyDecision(False, "empty commands are denied")

        try:
            parts = tuple(split(command))
        except ValueError as exc:
            return PolicyDecision(False, f"command parse failed: {exc}")

        if not any(parts[: len(prefix)] == prefix for prefix in self.allowed_command_prefixes):
            return PolicyDecision(False, "command prefix is not allowed")

        if self.allowed_path_prefixes and not self._paths_stay_within_guard(parts):
            return PolicyDecision(False, "command path is outside allowed prefixes")

        return PolicyDecision(True, "allowed")

    def require_allowed(self, command: str) -> None:
        decision = self.evaluate(command)
        if not decision.allowed:
            raise PermissionError(decision.reason)

    def _paths_stay_within_guard(self, parts: tuple[str, ...]) -> bool:
        path_like = [part for part in parts[1:] if "/" in part or part.startswith(".")]
        for value in path_like:
            path = Path(value).expanduser()
            if not path.is_absolute():
                path = (Path.cwd() / path).resolve()
            else:
                path = path.resolve()
            if not any(_is_relative_to(path, prefix.resolve()) for prefix in self.allowed_path_prefixes):
                return False
        return True


def _is_relative_to(path: Path, prefix: Path) -> bool:
    try:
        path.relative_to(prefix)
        return True
    except ValueError:
        return False
