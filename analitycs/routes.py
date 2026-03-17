from fastapi import APIRouter
from db import DbConnection
from dal import DataInteract
from DigitalHunter_map import plot_map_with_geometry

router = APIRouter()

db = DbConnection()
data_inter = DataInteract(db)


@router.get('/moving-targets/')
def get_moving_targets_api():
    return data_inter.get_moving_targets()


@router.get('/signal-count/')
def get_signal_count_api():
    return data_inter.get_signal_count()


@router.get('/top_unknown_entities/')
def get_top_3_unknown_entities_api():
    return data_inter.get_top_3_unknown_entities()


@router.get('/extreme-entities/')
def get_extreme_entities_api():
    return data_inter.get_extreme_entities()


def plot_map(entity_id: str):
    records = data_inter.get_cords_order_by_date(entity_id)
    cords = [(record["reported_lon"], record["reported_lat"]) for record in records]
    plot_map_with_geometry(cords)

