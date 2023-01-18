import os
from datetime import datetime
from typing import List

import pynecone as pc
from pydantic import parse_obj_as
from zeep import helpers, Client

from .client_models import Train

WSDL_URL = os.getenv("WSDL_URL")


class State(pc.State):
    """The app state."""
    trains: List[Train] = []
    selected_train: dict = None
    is_round_trip = False
    departure_station = ""
    arrival_station = ""
    departure_date: str = "2022-01-01"
    departure_time: str = "12:00:00"
    classes: List[str] = ['first', 'standard', 'business']
    selected_train_class = ""
    first: bool = False
    standard: bool = False
    business: bool = False

    def search_trains(self):
        """Get the image from the prompt."""
        client = Client(WSDL_URL)
        classes_filter_list = []
        if self.first:
            classes_filter_list.append('first')
        if self.standard:
            classes_filter_list.append('standard')
        if self.business:
            classes_filter_list.append('business')
        emptyArrayPlaceholder = client.get_type('ns0:stringArray')
        options = emptyArrayPlaceholder()
        for el in classes_filter_list:
            options['string'].append(el)
        response = client.service.search_trains(
            self.departure_station,
            self.arrival_station,
            options,
            datetime.strptime(self.departure_date, "%Y-%m-%d").date(),
            datetime.strptime(self.departure_time, "%H:%M:%S").time()
            # "2022-01-01T12:00:00"
        )
        if not response:
            self.trains = []
            return
        print(type(response))
        print(type(response[0]))
        print(response)
        res = helpers.serialize_object(response)
        print(res)
        self.trains = parse_obj_as(List[Train], res)
        print(self.trains)


def select_train(train_id: int):
    print(train_id)


def render_train(train: Train):
    """Render an item in the todo list."""
    # res = requests.get()
    # train.classes =

    return pc.vstack(
        pc.heading(train.departure_station + " - " + train.arrival_station, font_size="1.5em"),
        pc.text(train.departure_date),
        pc.text(train.departure_time),
        pc.hstack(
            pc.foreach(train.classes, lambda train_class: pc.vstack(
                pc.button(train_class.seat_class)
            ))
        ),
        pc.divider(),
    )


# def render_classes(train_id: int):
#     return pc.center(
#         pc.vstack(
#             pc.heading("Select classes", font_size="1.5em"),
#             pc.button(
#                 "Back",
#                 on_click=[State.set_selected_train],
#                 width="100%",
#             ),
#             pc.divider(),
#             pc.foreach(State.trains[train_id]["classes"], lambda item: render_class(item)),
#             bg="white",
#             padding="2em",
#             shadow="lg",
#             border_radius="lg",
#         ),
#         width="100%",
#         height="100vh",
#         bg="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%)",
#     )


def index():
    return pc.center(
        pc.vstack(
            pc.heading("Search trains", font_size="1.5em"),

            pc.input(placeholder="Departure Station", on_change=State.set_departure_station),
            pc.input(placeholder="Arrival Station", on_change=State.set_arrival_station),
            pc.input(placeholder="Departure Date", on_change=State.set_departure_date),
            pc.checkbox(
                "Round trip",
                on_change=State.set_is_round_trip,
            ),
            pc.text("Filter by classes"),
            pc.hstack(
                pc.checkbox("first", on_change=State.set_first),
                pc.checkbox("standard", on_change=State.set_standard),
                pc.checkbox("business", on_change=State.set_business),
            ),
            pc.button(
                "Search",
                on_click=[State.search_trains],
                width="100%",
            ),
            pc.foreach(State.trains, lambda train: render_train(train)),
            bg="white",
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        width="100%",
        height="100vh",
        bg="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%)",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Search trains")
app.compile()
