from model.kategorie import Kategorie
from repository import KategorieRepository


def create_category(kategorie_name):
    new_kategorie = Kategorie(name=kategorie_name)
    KategorieRepository.add_kategorie(new_kategorie)


def update_category(kategorie_id, kategorie_name):
    KategorieRepository.set_kategorie_name_by_id(kategorie_id, kategorie_name)


def delete_category(kategorie_id):
    KategorieRepository.delete_kategorie_by_id(kategorie_id)
