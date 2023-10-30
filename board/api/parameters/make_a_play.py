from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi

position_key = openapi.Schema(
    title=_("Position"),
    type=openapi.TYPE_STRING,
    description=_(
        "Position in the board for the next move, the value is presented as 'column_row', where column goes from 'A' to 'C' and row goes from 1 to 3, any other value is unacceptable and the string must be capitalized."
    ),
)

board_id_key = openapi.Schema(
    title=_("Board ID"),
    type=openapi.TYPE_INTEGER,
    format=openapi.FORMAT_INT32,
    description=_("ID of the board in which the play takes place."),
)

make_a_play_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["*"],
    properties={"position": position_key, "board_id": board_id_key},
)

make_a_play_response_dict = {
    "200": openapi.Response(
        description=_("Correct Request and the info is shown in a payload."),
        schema=openapi.Schema(
            title=_("Check status after move."),
            type=openapi.TYPE_OBJECT,
            read_only=True,
            description=_("Schema of a 200 status code response for this view"),
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    read_only=True,
                    description=_(
                        "Message saying wether its the next player's turn to play, or if the game reulted in victory or draw."
                    ),
                ),
                "success": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    read_only=True,
                    description=_("Boolean value, True if the play was successful"),
                ),
            },
        ),
        examples={
            "application/json": {
                "success": True,
                "message": _("Great! Now wait for your opponent to play."),
            }
        },
    ),
    "400": openapi.Response(
        description=_(
            "There was a validation error with the data and description of it will be shown."
        ),
        schema=openapi.Schema(
            title=_("Invalid move or data."),
            type=openapi.TYPE_OBJECT,
            read_only=True,
            description=_("Schema of a 400 status code response for this view."),
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    read_only=True,
                    description=_(
                        "Brief description of the error, 'BAD_REQUEST' by default"
                    ),
                    default=_("BAD_REQUEST"),
                ),
                "errors": openapi.Schema(
                    title="Serializer Errors",
                    type=openapi.TYPE_OBJECT,
                    description="Possible validation errors from serializers or pydantic.",
                    properties={
                        "field_name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default="Description of the error/s "
                            "related to the field appearing"
                            " as key.",
                            read_only=True,
                        )
                    },
                ),
            },
        ),
        examples={
            "application/json": {
                "type": "BAD_REQUEST",
                "errors": {"board_id": ["'board_id' must be a valid integer."]},
            }
        },
    ),
    "412": openapi.Response(
        description=_("There was a problem with the sent payload."),
        schema=openapi.Schema(
            title=_("Invalid Payload."),
            type=openapi.TYPE_OBJECT,
            read_only=True,
            description=_("Schema of a 412 status code response for this view."),
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    read_only=True,
                    description=_(
                        "Brief description of the error, 'PRECONDITION_FAILED' by default"
                    ),
                    default=_("PRECONDITION_FAILED"),
                ),
                "errors": openapi.Schema(
                    title="Serializer Errors",
                    type=openapi.TYPE_OBJECT,
                    description="Errors describing the sent payload's issues.",
                    properties={
                        "field_name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default="Description of the error/s "
                            "related to the field appearing"
                            " as key.",
                            read_only=True,
                        )
                    },
                ),
            },
        ),
        examples={
            "application/json": {
                "type": "PRECONDITION_FAILED",
                "errors": {"board_id": ["This is a required field."]},
            }
        },
    ),
}
