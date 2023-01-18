import os
from datetime import datetime
from typing import List

import pynecone as pc
from pydantic import parse_obj_as
from zeep import helpers, Client

from .book_ticket import book_tickets_view
from .client_models import Train

WSDL_URL = os.getenv("WSDL_URL")


class State(pc.State):
    """The app state."""
    trains: List[Train] = []
    is_round_trip = False
    departure_station = ""
    arrival_station = ""
    departure_date: str = ""
    departure_time: str = ""
    classes: List[str] = ['first', 'standard', 'business']
    selected_train: dict = None
    selected_train_seat_class: dict = None
    first: bool = False
    standard: bool = False
    business: bool = False
    quantity: int = 1
    flexible = False

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
            datetime.strptime(self.departure_date, "%Y-%m-%d").date() if self.departure_date else None,
            datetime.strptime(self.departure_time, "%H:%M:%S").time() if self.departure_time else None,
            self.quantity
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

    def select_train_seat_class(self, selected_train: dict, selected_train_seat_class: dict):
        print("selected: " + str(selected_train['id']) + " " + str(selected_train_seat_class['id']))
        self.selected_train = selected_train
        self.selected_train_seat_class = selected_train_seat_class
        client = Client(WSDL_URL)
        response = client.service.book_tickets(1,
                                               selected_train_seat_class['available_seats_count'] - int(self.quantity))
        print(response)
        self.trains = []
        return pc.redirect("/book-tickets")

    def book_tickets(self):
        client = Client(WSDL_URL)
        response = client.service.book_tickets(1, 1)

        print(response)


def render_train(train: Train):
    return pc.vstack(
        pc.heading(train.departure_station + " - " + train.arrival_station, font_size="1.5em"),
        pc.text(train.departure_date),
        pc.text(train.departure_time),
        pc.hstack(
            pc.foreach(train.classes, lambda train_class: pc.vstack(
                pc.cond(State.flexible,
                        pc.button(train_class.seat_class + " (" + train_class.price_flexible + "€ x " +
                                  State.quantity + ")",
                                  on_click=lambda: State.select_train_seat_class(train, train_class)),
                        pc.button(train_class.seat_class + " (" + train_class.price_not_flexible + "€ x " +
                                  State.quantity + ")",
                                  on_click=lambda: State.select_train_seat_class(train, train_class))
                        )
                ,
            ))
        ),
        pc.divider(),
    )


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
            pc.text("Filter seats"),
            pc.hstack(
                pc.center(
                    pc.text("Quantity"),
                    pc.number_input(
                        on_change=State.set_quantity,
                        width="50%",
                        margin_left="10%",
                    ),
                )
            ),
            pc.hstack(
                pc.checkbox("first", on_change=State.set_first),
                pc.checkbox("standard", on_change=State.set_standard),
                pc.checkbox("business", on_change=State.set_business),
            ),
            pc.checkbox("Flexible ticket", on_change=State.set_flexible),
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


def book_tickets():
    # State.book_tickets()
    return book_tickets_view(State)


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Search trains")
app.add_page(book_tickets, title="Book tickets", path="/book-tickets")
app.compile()
