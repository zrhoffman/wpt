import pytest

import webdriver.bidi.error as error


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
@pytest.mark.asyncio
async def test_params_context_invalid_type(bidi_session, value):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.browsing_context.set_viewport(context=value, viewport={
            "width": 100,
            "height": 200,
        })


@pytest.mark.asyncio
async def test_params_context_invalid_value(bidi_session):
    with pytest.raises(error.NoSuchFrameException):
        await bidi_session.browsing_context.set_viewport(context="_invalid_")


@pytest.mark.asyncio
async def test_params_context_iframe(bidi_session, new_tab, get_test_page):
    url = get_test_page(as_frame=True)
    await bidi_session.browsing_context.navigate(
        context=new_tab["context"],
        url=url,
        wait="complete")

    contexts = await bidi_session.browsing_context.get_tree(root=new_tab["context"])
    assert len(contexts) == 1
    frames = contexts[0]["children"]
    assert len(frames) == 1
    frame_context = frames[0]["context"]

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.browsing_context.set_viewport(context=frame_context)


@pytest.mark.parametrize("viewport", [False, 42, "", {}, [], {"width": 100}, {"height": 100}])
@pytest.mark.asyncio
async def test_params_viewport_invalid_type(bidi_session, new_tab, viewport):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.browsing_context.set_viewport(context=new_tab["context"], viewport=viewport)


@pytest.mark.parametrize("width", [None, False, "", {}, []])
@pytest.mark.asyncio
async def test_params_viewport_width_invalid_type(bidi_session, new_tab, width):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.browsing_context.set_viewport(context=new_tab["context"], viewport={
            "width": width,
            "height": 100,
        })


@pytest.mark.parametrize("height", [None, False, "", {}, []])
@pytest.mark.asyncio
async def test_params_viewport_height_invalid_type(bidi_session, new_tab, height):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.browsing_context.set_viewport(context=new_tab["context"], viewport={
            "width": 100,
            "height": height,
        })


@pytest.mark.parametrize("viewport", [
    {"width": -1, "height": 100},
    {"width": 100, "height": -1},
    {"width": -1, "height": -1},
], ids=["width negative", "height negative", "both negative"])
@pytest.mark.asyncio
async def test_params_viewport_invalid_value(bidi_session, new_tab, viewport):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.browsing_context.set_viewport(context=new_tab["context"], viewport=viewport)
