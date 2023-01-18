import pynecone as pc

from .client_models import Train


def render_train(State, train: Train):
    return pc.vstack(
        pc.heading(train.departure_station + " - " + train.arrival_station, font_size="1.5em"),
        pc.text(train.departure_date),
        pc.text(train.departure_time),
        pc.hstack(
            pc.foreach(train.classes, lambda train_class: pc.vstack(
                pc.button(train_class.seat_class,
                          on_click=lambda: State.select_train_seat_class(train, train_class)),
            ))
        ),
        pc.divider(),
    )


def book_tickets_view(State):
    return pc.center(
        pc.vstack(
            pc.heading("Thank you, your ticket has been booked", font_size="1.5em"),
            # pc.text("Selected train: " + State.selected_train_seat_class['seat_class']),
            # pc.button(
            #     "Back",
            #     on_click=[State.set_selected_train],
            #     width="100%",
            # ),
            # pc.divider(),
            # pc.foreach(State.trains, lambda item: render_train(State, item)),
            # bg="white",
            # padding="2em",
            # shadow="lg",
            # border_radius="lg",
        ),
        width="100%",
        height="100vh",
        bg="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%)",
    )
