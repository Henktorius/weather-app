def test_initial_label(app):
    """Check if the starting text is correct."""
    app.root.update()
    assert app.label.cget("text") == "Enter City:"


def test_button_click_updates_label(app):
    """Simulate user input and a button click."""
    app.root.update()
    # 1. Simulate typing into the Entry widget
    app.city_input.insert(0, "London")

    # 2. Manually trigger the button command
    app.submit_btn.invoke()

    # 3. Force Tkinter to process the change
    app.root.update()

    # 4. Assert the result
    assert "London" in app.label.cget("text")
