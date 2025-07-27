"""
backend/saiki_site/guesser.py

...
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from .entities import HistoricalEntity


@dataclass(init=True, repr=True, eq=False, frozen=False, slots=True)
class GuessState:
    """Represents the state of the player in the Guess game mode."""

    key: str  # the player's session id
    selected: None | int  # a pointer to the entity currently selected
    attempted: list[int]  # already guessed...

    @staticmethod
    def from_request(request: WSGIRequest) -> GuessState:
        """Retrieves the Player's guessing state by the request.

        :param request: The Django request.
        :return: The user's guessing state. Creates a new if doesn't identify one.
        """

        key: None | str = request.COOKIES.get("key")

        if key is None:
            from .enc import generate_key
            key: str = generate_key()
            assert len(key) == 64

        selected: None | str = request.COOKIES.get("selected")

        try:
            selected: int = int(selected)

        except TypeError:
            # couldn't make the casting...
            pass

        try:
            b64_array: str = request.COOKIES.get("A#")
            if not b64_array:
                raise TypeError

            from .enc import b64_to_int_list
            attempted: list[int] = b64_to_int_list(b64_array, 4)

        except TypeError:
            attempted: list[int] = []

        """
        attempted: list[int] = []
        iterator: int = 0
        while True:
            try:
                attempted.append(
                    int(request.COOKIES.get(f"attempt_{iterator}"))
                )
            except TypeError:
                break

            iterator += 1
        """

        print(f"COOKIE GET. key: {key} ({type(key)}); selected: {selected} ({type(selected)}); attempted: {attempted}")

        return GuessState(
            key, selected, attempted
        )

    def set_cookie(self, response_json: JsonResponse, reset: bool = False) -> JsonResponse:
        """Set the cookies reply on the json response.
            :param response_json: The Json response the cookies will be set to.
            :param reset: If to reset the cookies."""

        if reset:
            response_json.delete_cookie("key", samesite="Lax")
            response_json.delete_cookie("selected", samesite="Lax")
            response_json.delete_cookie("A#", samesite="Lax")

            return response_json

        response_json.set_cookie("key", self.key, secure=False, httponly=True, samesite="Lax")
        response_json.set_cookie("selected", self.selected, secure=False, httponly=True, samesite="Lax")

        """
        from .enc import int_to_base64
        for i, v in enumerate(self.attempted):
            b64_v: str = int_to_base64(v, 4)
            response_json.set_cookie(f"A#", b64_v, secure=False, httponly=True, samesite="Lax")
        """
        from .enc import int_list_to_b64
        response_json.set_cookie(f"A#", int_list_to_b64(self.attempted, 4), secure=False, httponly=True, samesite="Lax")

        return response_json

    def add_attempt(self, attempt_index: int) -> None:
        """..."""

        if not isinstance(attempt_index, int):
            raise TypeError

        from .enc import permute
        self.attempted.append(
            permute(attempt_index, self.key, 1000)
        )

        return None

    @property
    def __real_indexes(self) -> list[int]:
        from .enc import unpermute
        return list(map(lambda x: unpermute(x, self.key, 1000), self.attempted))

    @property
    def attempted_names(self) -> list[str]:
        real_indexes: list[int] = self.__real_indexes
        return list(map(
            lambda index: guesser.get_entity(index)["name"], real_indexes
        ))

    def get_collection(self, data) -> JsonResponse:
        """Returns all the entity data serialized."""

        real_indexes: list[int] = self.__real_indexes

        print(data)

        # will hold the JSON data in python.
        response_list: list[dict] = list()

        # retrieving the data.
        for index in real_indexes:
            entity = guesser.get_entity(index)

            response = self.__check_entity(entity_name=entity["name"])

            response_list.append(
                response
            )

        return JsonResponse({
            "tries": len(response_list),
            "entities": response_list,
        })

    def __check_entity(self, entity_name: str) -> dict:
        """Checks the fields of the player's guessing. Returns the JSON format response (as a dictionary).

        :param entity_name: Name of the entity being guessed.
        :returns: Entity's guessing response in JSON format."""

        # making sure the state have a selected entity.
        guesser.select_entity(self)

        # the entity that is marked to be solved by the player.
        from .enc import unpermute
        real_selected_index: int = unpermute(self.selected, self.key, 1000)
        correct_entity: dict[str, list] | HistoricalEntity = guesser.get_entity2(real_selected_index)

        # the one matching what he inserted.
        match_entity: dict | None
        match_entity_index: int
        match_entity, match_entity_index = guesser.fetch_entity(entity_name)
        print("match entity:", match_entity)

        # will hold the JSON response back to the user.
        response: dict = {}

        if match_entity is not None:
            # meaning that at least it was found on the database...

            response: dict = {
                "name": match_entity["name"],
                "data": {},
                "guessed": "correct"
            }

            for field in match_entity["data"]:

                # if the field is correct, for all effects.
                # guess_type: str = GuessView.__compare_entity_field(match_entity["data"][field], correct_entity["data"][field])
                guess_type: str = correct_entity @ (field, match_entity["data"][field])

                # adding the respective field to the response...
                response["data"][field] = [match_entity["data"][field], guess_type]

                if response["guessed"] == "correct":
                    # if the response is correct up to now, it can potentially make the whole answer wrong.
                    response["guessed"] = guess_type

            self.add_attempt(match_entity_index)

        return response

    def guess(self, entity_name: str) -> JsonResponse:
        """Checks the fields of the player's guessing. Updates the guessing state (through the response).

        :param entity_name: Name of the entity being guessed.
        :returns: Returns the entity guessing response."""

        response = self.__check_entity(entity_name)
        response_json: JsonResponse = JsonResponse(response)

        to_reset_cookies: bool = response["guessed"] == "correct" if "guessed" in response else False
        self.set_cookie(response_json, to_reset_cookies)

        return response_json


class Guesser(object):
    """Handles the Guess game mode inner logical structure."""

    __static_json_data_stream: list[dict]

    def __init__(self) -> None:
        """Initializes the guesser state."""

        from os import path

        data_path: str = path.join(path.dirname(__file__), "test.json")

        # Currently, the database fetch is mocked.
        with open(data_path, "r", encoding="utf-8") as file:
            self.__static_json_data_stream: list[dict] = json.load(file)

        for entry in self.__static_json_data_stream:
            entry: dict = entry["data"]
            print("entry:", entry)

            for data_field in entry:
                if not isinstance(entry[data_field], list):
                    # then we have to list it.
                    entry[data_field] = [entry[data_field]]

    def fetch_entity(self, entity_name: str) -> tuple[None | dict, int]:
        """Fetches an entity by its name on the data pool."""

        entity_name: str = entity_name.lower()

        for i, entity in enumerate(self.__static_json_data_stream):
            # @TODO: to abstract and improve comparison!
            if entity["name"].lower() == entity_name:
                return entity, i

        return None, - 1

    def select_entity(self, state: GuessState) -> GuessState:
        """Collapses the entity selection; chooses one from the data pool as the correct.
            :param state: The current player's guess mode state.
            :return: the new state after the selection. The parameter is modified.
        """

        from random import randint

        if state.selected is not None:
            return state

        # choosing an entity at random; uniform distribution...
        state.selected = randint(0, len(self.__static_json_data_stream) - 1)

        # encrypting it
        from .enc import permute
        state.selected = permute(state.selected, state.key, 1000)

        return state

    def get_entity(self, index: int) -> dict[str, str | list]:
        """Retrieves an entity by its index in the data pool.
            :param index: The 0-based index.
            :return: The json dictionary associated with the entity entry.
            :raises TypeError: If the index is out of the bounds."""
        return self.__static_json_data_stream[index]

    def fetch_entity2(self, entity_name: str) -> tuple[None | HistoricalEntity, int]:
        """Fetches an entity by its name on the data pool.
        Alternative version, that returns the HistoricalEntity object."""

        for i, entity in enumerate(self.__static_json_data_stream):
            print(f"entity[{i}]: {entity}")
            if entity["name"].lower() == entity_name:
                return HistoricalEntity.from_type(entity["type"].lower(), entity_name, ** entity["data"]), i

        return None, - 1

    def get_entity2(self, index: int) -> HistoricalEntity:

        entity: dict = self.__static_json_data_stream[index]
        return HistoricalEntity.from_type(entity["type"].lower(), entity["name"], ** entity["data"])

    def match_name(self, state: GuessState, name: str) -> list[str]:
        """Matches an entity name over the collection. Returns a list of possible results. """

        from difflib import get_close_matches
        from typing import Iterable

        max_query_results: int = 5
        cutoff: float = 0.35

        attempt_names: list[str] = state.attempted_names
        name_list: Iterable[str] = filter(
            lambda x: x not in attempt_names, map(lambda x: x["name"], self.__static_json_data_stream)
        )
        matches: list[str] = get_close_matches(name, name_list, n=max_query_results, cutoff=cutoff)

        return matches


"""Global initialization"""

guesser: Guesser = Guesser()

if __name__ == "__main__":
    ...
