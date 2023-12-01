from collections import OrderedDict
from pathlib import Path

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UndefinedVariableInTemplate
from cookiecutter.generate import generate_context
from cookiecutter.prompt import (
    prompt_choice_for_config,
    read_user_choice,
    read_user_variable,
    render_variable,
)
from jinja2.exceptions import UndefinedError


def _prompt_choice_and_subitems(cookiecutter_dict, env, key, options, no_input):
    result = {}

    # first, get the selection
    rendered_options = [
        render_variable(env, list(raw.keys())[0], cookiecutter_dict) for raw in options
    ]

    if no_input:
        selected = rendered_options[0]
    else:
        selected = read_user_choice(key, rendered_options)

    selected_item = [
        list(c.values())[0] for c in options if list(c.keys())[0] == selected
    ][0]

    result[selected] = {}

    # then, fill in the sub values for that item
    if isinstance(selected_item, dict):
        for subkey, raw in selected_item.items():
            # We are dealing with a regular variable
            val = render_variable(env, raw, cookiecutter_dict)

            if not no_input:
                val = read_user_variable(subkey, val)

            result[selected][subkey] = val
    elif isinstance(selected_item, list):
        val = prompt_choice_for_config(
            cookiecutter_dict, env, selected, selected_item, no_input
        )
        result[selected] = val
    elif isinstance(selected_item, str):
        result[selected] = selected_item

    return result


def prompt_for_config(context, no_input=False):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.
    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = OrderedDict([])
    env = StrictEnvironment(context=context)

    # First pass: Handle simple and raw variables, plus choices.
    # These must be done first because the dictionaries keys and
    # values might refer to them.
    for key, raw in context["cookiecutter"].items():
        if key.startswith("_"):
            cookiecutter_dict[key] = raw
            continue

        try:
            if isinstance(raw, list):
                if isinstance(raw[0], dict):
                    val = _prompt_choice_and_subitems(
                        cookiecutter_dict, env, key, raw, no_input
                    )
                    cookiecutter_dict[key] = val
                else:
                    # We are dealing with a choice variable
                    val = prompt_choice_for_config(
                        cookiecutter_dict, env, key, raw, no_input
                    )
                    cookiecutter_dict[key] = val
            elif not isinstance(raw, dict):
                # We are dealing with a regular variable
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input:
                    val = read_user_variable(key, val)

                cookiecutter_dict[key] = val
        except UndefinedError as err:
            msg = "Unable to render variable '{}'".format(key)
            raise UndefinedVariableInTemplate(msg, err, context)

    # Second pass; handle the dictionaries.
    for key, raw in context["cookiecutter"].items():
        try:
            if isinstance(raw, dict):
                # We are dealing with a dict variable
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input:
                    val = read_user_dict(  # noqa: F821 referencable in patched context
                        key, val
                    )

                cookiecutter_dict[key] = val
        except UndefinedError as err:
            msg = "Unable to render variable '{}'".format(key)
            raise UndefinedVariableInTemplate(msg, err, context)

    return cookiecutter_dict


def generate_context_wrapper(*args, **kwargs):
    """Hardcoded in cookiecutter, so we override:
    https://github.com/cookiecutter/cookiecutter/blob/2bd62c67ec3e52b8e537d5346fd96ebd82803efe/cookiecutter/main.py#L85
    """
    # replace full path to cookiecutter.json with full path to ccds.json
    kwargs["context_file"] = str(Path(kwargs["context_file"]).with_name("ccds.json"))

    parsed_context = generate_context(*args, **kwargs)

    # replace key
    parsed_context["cookiecutter"] = parsed_context["ccds"]
    del parsed_context["ccds"]
    return parsed_context
