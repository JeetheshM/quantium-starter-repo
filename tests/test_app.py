from dash import dcc, html

from app import app


def iter_components(component):
    yield component
    children = getattr(component, "children", None)

    if children is None:
        return

    if isinstance(children, (list, tuple)):
        for child in children:
            yield from iter_components(child)
    else:
        yield from iter_components(children)


def test_header_is_present():
    headers = [
        component
        for component in iter_components(app.layout)
        if isinstance(component, html.H1)
    ]

    assert any(header.children == "Pink Morsel Sales Visualiser" for header in headers)


def test_visualisation_is_present():
    graphs = [
        component
        for component in iter_components(app.layout)
        if isinstance(component, dcc.Graph)
    ]

    assert any(graph.id == "sales-chart" for graph in graphs)


def test_region_picker_is_present():
    radio_items = [
        component
        for component in iter_components(app.layout)
        if isinstance(component, dcc.RadioItems)
    ]

    region_picker = next((radio for radio in radio_items if radio.id == "region-selector"), None)

    assert region_picker is not None
    assert len(region_picker.options) == 5
