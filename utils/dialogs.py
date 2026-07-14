from widgets.ConfirmModal import ConfirmModal


async def confirm_dialog(
    app,
    *,
    text: str = "Are you sure?",
    cancel_label: str = "NO",
    confirm_label: str = "YES",
    only_acknowledge: bool = False,
) -> bool:
    """Show a confirmation dialog and await the result."""
    result = await app.push_screen_wait(
        ConfirmModal(
            text=text,
            cancel_label=cancel_label,
            confirm_label=confirm_label,
            only_acknowledge=only_acknowledge,
        )
    )
    return result
