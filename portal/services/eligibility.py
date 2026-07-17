"""Return eligibility engine.

Rules are configured in ``portal/data/rules.yaml`` and evaluated in order —
first matching rule wins.  Built-in rules are implemented as :class:`Rule`
subclasses and registered on the :class:`RuleRegistry`, keyed by the ``id``
used in the config file.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar

import yaml

from portal.types import Article, ArticleEligibility, Order

_RULES_PATH = Path(__file__).resolve().parent.parent / "data" / "rules.yaml"


class Rule(ABC):
    """A single eligibility rule.

    :meth:`evaluate` returns a human-readable rejection reason when the rule
    blocks the return, or ``None`` when the rule does not apply.
    """

    rule_id: ClassVar[str] = ""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def evaluate(self, article: Article, order: Order) -> str | None:
        """Return a rejection reason, or ``None`` if the rule does not block."""


class RuleRegistry:
    """Global registry of built-in rule implementations."""

    _registry: ClassVar[dict[str, type[Rule]]] = {}

    @classmethod
    def register(cls, rule_id: str) -> Callable[[type[Rule]], type[Rule]]:
        def decorator(rule_cls: type[Rule]) -> type[Rule]:
            rule_cls.rule_id = rule_id
            cls._registry[rule_id] = rule_cls
            return rule_cls

        return decorator

    @classmethod
    def create(cls, rule_id: str, config: dict[str, Any]) -> Rule:
        if rule_id not in cls._registry:
            raise KeyError(f"Unknown eligibility rule: {rule_id!r}")
        return cls._registry[rule_id](config)


@RuleRegistry.register("already_returned")
class AlreadyReturnedRule(Rule):
    """Items that have already been returned cannot be returned again."""

    def evaluate(self, article: Article, order: Order) -> str | None:
        if article.quantity_returned:
            return "This item has already been returned."
        return None


@RuleRegistry.register("digital")
class DigitalItemRule(Rule):
    """Digital goods are delivered instantly and cannot be returned."""

    def evaluate(self, article: Article, order: Order) -> str | None:
        if article.is_digital:
            return "Digital items cannot be returned."
        return None


@RuleRegistry.register("final_sale")
class FinalSaleRule(Rule):
    """Final-sale items are sold as-is."""

    def evaluate(self, article: Article, order: Order) -> str | None:
        if article.is_final_sale:
            return "Final-sale items cannot be returned."
        return None


@RuleRegistry.register("return_window")
class ReturnWindowRule(Rule):
    """Returns are only accepted within a number of days after delivery."""

    def evaluate(self, article: Article, order: Order) -> str | None:
        days = int(self.config.get("days", 30))
        age_days = (datetime.now() - order.delivery_date).days
        if age_days > days:
            return f"The {days}-day return window has expired."
        return None


def _load_rules() -> list[Rule]:
    with _RULES_PATH.open() as f:
        config: dict[str, Any] = yaml.safe_load(f)
    rules: list[Rule] = []
    for entry in config.get("rules", []):
        rule_id = str(entry.get("id", ""))
        rules.append(RuleRegistry.create(rule_id, entry))
    return rules


def evaluate_eligibility(order: Order) -> list[ArticleEligibility]:
    """Evaluate return eligibility for every article in *order*.

    Returns:
        A list of :class:`ArticleEligibility`, one per article in the order.
    """
    rules = _load_rules()

    results: list[ArticleEligibility] = []
    for article in order.articles:
        returnable = True
        reason = ""
        matched_rule = ""
        for rule in rules:
            rejection = rule.evaluate(article, order)
            if rejection is not None:
                returnable = False
                reason = rejection
                matched_rule = rule.rule_id
                break
        results.append(
            ArticleEligibility(
                article=article,
                returnable=returnable,
                reason=reason,
                matched_rule=matched_rule,
            )
        )
    return results
