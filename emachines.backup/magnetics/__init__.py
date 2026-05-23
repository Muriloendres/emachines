"""Magnetics: BH curve models, iron loss, electrical steel database, PM materials."""

from .iron_loss import (
    steinmetz, modified_steinmetz, bertotti,
    fit_steinmetz, fit_modified_steinmetz, fit_bertotti,
    fit_loss_model, MODEL_NAMES,
)
from .bh_models import frolich, fit_frolich, linear_region
from .electrical_steel import SteelGrade, SteelDatabase, SAMPLE_BH, SAMPLE_LOSS
from .pm_materials import MagnetGrade, MAGNET_LIBRARY, MagnetData

__all__ = [
    "steinmetz", "modified_steinmetz", "bertotti",
    "fit_steinmetz", "fit_modified_steinmetz", "fit_bertotti",
    "fit_loss_model", "MODEL_NAMES",
    "frolich", "fit_frolich", "linear_region",
    "SteelGrade", "SteelDatabase", "SAMPLE_BH", "SAMPLE_LOSS",
    "MagnetGrade", "MAGNET_LIBRARY", "MagnetData",
]
