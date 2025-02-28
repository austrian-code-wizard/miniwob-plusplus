# Generate Environments List page content.

import os

import gymnasium as gym
import pandas as pd

import miniwob  # noqa: F401

gym.logger.set_level(gym.logger.DISABLED)

ENV_TYPES = [
    {
        "name": "Original tasks",
        "description": "We use a subset of the original MiniWoB tasks that only involve (1) clicking and (2) typing text from the prompt.",
        "envs": [
            "choose-list",
            "click-button",
            "click-button-sequence",
            "click-checkboxes",
            "click-color",
            "click-dialog",
            "click-dialog-2",
            "click-link",
            "click-option",
            "click-shades",
            "click-shape",
            "click-tab",
            "click-tab-2",
            "click-test",
            "click-test-2",
            "click-widget",
            "count-shape",
            "email-inbox",
            "enter-date",
            "enter-password",
            "enter-text",
            "enter-text-dynamic",
            "enter-time",
            "focus-text",
            "focus-text-2",
            "grid-coordinate",
            "guess-number",
            "identify-shape",
            "login-user",
            "navigate-tree",
            "search-engine",
            "social-media",
            "tic-tac-toe",
            "use-spinner",
            "book-flight",
            "choose-date",
            "click-collapsible",
            "click-collapsible-2",
            "click-pie",
            "use-autocomplete",
            "book-flight-nodelay",
            "choose-date-nodelay",
            "click-collapsible-2-nodelay",
            "click-collapsible-nodelay",
            "click-pie-nodelay",
            "use-autocomplete-nodelay",
        ],
    },
    {
        "name": "Additional tasks",
        "description": "Some are harder versions of the existing tasks, while some are completely new.",
        "envs": [
            "click-checkboxes-large",
            "click-checkboxes-soft",
            "click-checkboxes-transfer",
            "click-tab-2-hard",
            "login-user-popup",
            "multi-layouts",
            "multi-orderings",
            "social-media-all",
            "social-media-some",
            "email-inbox-forward-nl",
            "email-inbox-forward-nl-turk",
            "email-inbox-nl-turk",
        ],
    },
    {
        "name": "Flight search tasks",
        "description": """These are server-free ports of the FormWoB tasks in the original World of Bits "paper.",
* The prompt is a list of key-value pairs (e.g., Departure City: New York)
* If the required fields are not filled, or if the agent navigates away from the page, the reward is "-1.",
* Otherwise, the reward is the fraction of key-value pairs that are satisfied """,
        "envs": ["flight.Alaska", "flight.Alaska-auto", "flight.AA"],
    },
    {
        "name": "Debug tasks",
        "description": "These are easier versions of existing tasks. They are used for debugging.",
        "envs": [
            "choose-date-easy",
            "choose-date-medium",
            "click-tab-2-easy",
            "click-tab-2-medium",
            "click-test-transfer",
            "email-inbox-delete",
            "email-inbox-forward",
            "email-inbox-important",
            "email-inbox-noscroll",
            "email-inbox-reply",
            "email-inbox-star-reply",
        ],
    },
    {
        "name": "Clicking non-elements",
        "description": "These tasks involve clicking at a specific point inside a canvas-like element.",
        "envs": [
            "bisect-angle",
            "circle-center",
            "count-sides",
            "find-midpoint",
            "number-checkboxes",
            "right-angle",
            "use-colorwheel",
            "use-colorwheel-2",
        ],
    },
    {
        "name": "Hovering",
        "description": "These tasks require hovering and moving the mouse cursor.",
        "envs": ["click-menu", "click-menu-2"],
    },
    {
        "name": "Dragging",
        "description": "These tasks involve dragging.",
        "envs": [
            "click-scroll-list",
            "drag-box",
            "drag-circle",
            "drag-cube",
            "drag-items",
            "drag-items-grid",
            "drag-shapes",
            "drag-sort-numbers",
            "highlight-text",
            "highlight-text-2",
            "resize-textarea",
            "scroll-text",
            "scroll-text-2",
            "text-editor",
            "use-slider",
            "use-slider-2",
        ],
    },
    {
        "name": "Typing free text",
        "description": "These tasks involve typing texts that are not substrings of the prompt. Some of these also require advanced reasoning (e.g., solving math problems).",
        "envs": [
            "copy-paste",
            "copy-paste-2",
            "enter-text-2",
            "find-word",
            "read-table",
            "read-table-2",
            "simple-algebra",
            "simple-arithmetic",
            "terminal",
            "text-transform",
            "visual-addition",
        ],
    },
    {
        "name": "Timing",
        "description": "These tasks require the agent to wait for events to happen before acting, and a 'nodelay' version is impossible to make.",
        "envs": ["chase-circle", "moving-items", "simon-says"],
    },
    {
        "name": "Timing",
        "description": "These tasks require the agent to wait for events to happen before acting, and a 'nodelay' version is impossible to make.",
        "envs": ["chase-circle", "moving-items", "simon-says"],
    },
]

ENVS_DESCRIPTIONS = {
    "choose-list": "Choose an item from a drop down list.",
    "click-button": "Click on a specific button in a generated form.",
    "click-button-sequence": "Click on buttons in a certain order.",
    "click-checkboxes": "Click desired checkboxes.",
    "click-color": "Click the specified color.",
    "click-dialog": "Click the button to close the dialog box.",
    "click-dialog-2": "Click a specific button in a dialog box.",
    "click-link": "Click on a specified link in text.",
    "click-option": "Click option boxes.",
    "click-shades": "Click the shades that match a specified color.",
    "click-shape": "Click on a specific shape.",
    "click-tab": "Click on a tab element.",
    "click-tab-2": "Click a link inside a specific tab element.",
    "click-test": "Click on a single button.",
    "click-test-2": "Click on one of two buttons.",
    "click-widget": "Click on a specific widget in a generated form.",
    "count-shape": "Count number of shapes.",
    "email-inbox": "Navigate through an email inbox and perform some actions.",
    "enter-date": "Use the date input to pick the correct date.",
    "enter-password": "Enter the password into the form.",
    "enter-text": "Enter given text to a textfield.",
    "enter-text-dynamic": "Enter dynamically generated text to a textfield.",
    "enter-time": "Enter the specified time into the input.",
    "focus-text": "Focus into a text input.",
    "focus-text-2": "Focus on a specific text input.",
    "grid-coordinate": "Find the Cartesian coordinates on a grid.",
    "guess-number": "Guess the number.",
    "identify-shape": "Identify a randomly generated shape.",
    "login-user": "Enter user login details into the form.",
    "navigate-tree": "Navigate a file tree to find a specified file or folder.",
    "search-engine": "Search through a bunch of results to find a specified link.",
    "social-media": "Interact with a social media feed.",
    "tic-tac-toe": "Win a game of tic-tac-toe.",
    "use-spinner": "Use a spinner to select given number.",
    "book-flight": "Search for flight results.",
    "choose-date": "Learn to operate a date picker tool.",
    "click-collapsible": "Click a collapsible element to expand it.",
    "click-collapsible-2": "Find and click on a specified link, from collapsible elements.",
    "click-pie": "Click items on a pie menu.",
    "use-autocomplete": "Use autocomplete element efficiently.",
    "book-flight-nodelay": "[book-flight]",
    "choose-date-nodelay": "[choose-date]",
    "click-collapsible-2-nodelay": "[click-collapsible-2]",
    "click-collapsible-nodelay": "[click-collapsible]",
    "click-pie-nodelay": "[click-pie]",
    "use-autocomplete-nodelay": "[use-autocomplete]",
    "click-checkboxes-large": "[click-checkboxes] Click at least 5 out of up to 12 checkboxes",
    "click-checkboxes-soft": "[click-checkboxes] Paraphrased entries",
    "click-checkboxes-transfer": "[click-checkboxes] Train and test on different number of targets",
    "click-tab-2-hard": "[click-tab-2] Varying number of tabs from 2 to 6",
    "login-user-popup": "[login-user] Random popup",
    "multi-layouts": "Fill in forms of varying layouts.",
    "multi-orderings": "Fill in forms with shuffled field orderings.",
    "social-media-all": "[social-media] Do some action on all matching entries",
    "social-media-some": "[social-media] Do some action on some matching entries",
    "email-inbox-forward-nl": "[email-inbox-forward] NL instruction (30 templates)",
    "email-inbox-forward-nl-turk": "[email-inbox-forward] NL instruction (100 templates)",
    "email-inbox-nl-turk": "[email-inbox] NL instruction (100 templates for each subtask)",
    "flight.Alaska": "port of Alaska FormWoB",
    "flight.Alaska-auto": "port of Alaska FormWoB but harder",
    "flight.AA": "port of American Airlines FormWoB (unused)",
    "choose-date-easy": "[choose-date] December only",
    "choose-date-medium": "[choose-date] December or November only",
    "click-tab-2-easy": "[click-tab-2] One 1 tab",
    "click-tab-2-medium": "[click-tab-2] Choose between a link or 'no match'",
    "click-test-transfer": "[click-test] Different buttons during train and test",
    "email-inbox-delete": "[email-inbox] No scrolling + 1 subtask",
    "email-inbox-forward": "[email-inbox] No scrolling + 1 subtask",
    "email-inbox-important": "[email-inbox] No scrolling + 1 subtask",
    "email-inbox-noscroll": "[email-inbox] No scrolling",
    "email-inbox-reply": "[email-inbox] No scrolling + 1 subtask",
    "email-inbox-star-reply": "[email-inbox] No scrolling + 2 subtasks",
    "bisect-angle": "Find the line that bisects an angle evenly in two.",
    "circle-center": "Find the center of a circle.",
    "count-sides": "Count the number of sides on a shape.",
    "find-midpoint": "Find the shortest mid-point of two points.",
    "number-checkboxes": "Draw a given number using checkboxes.",
    "right-angle": "Given two points, add a third point to create a right angle.",
    "use-colorwheel": "Use a color wheel.",
    "use-colorwheel-2": "Use a color wheel given specific random color.",
    "click-menu": "Click menu items.",
    "click-menu-2": "Find a specific item from a menu.",
    "click-scroll-list": "Click multiple items from a scroll list. (also require Shift + click) ",
    "drag-box": "Drag the smaller box into the larger box.",
    "drag-circle": "Drag an item in a specified direction.",
    "drag-cube": "Drag a 3D cube to show a specific face.",
    "drag-items": "Drag items in a list, in a specified direction",
    "drag-items-grid": "Drag items in a 2D grid around.",
    "drag-shapes": "Drag shapes into a box.",
    "drag-sort-numbers": "Drag numbers into sorted ascending order.",
    "highlight-text": "Highlight all the text.",
    "highlight-text-2": "Highlight the specified paragraph.",
    "resize-textarea": "Resize a textarea in a given direction.",
    "scroll-text": "Scroll through a text area element and enter last word into text area.",
    "scroll-text-2": "Scroll through a text area in a given direction.",
    "text-editor": "Modify a text's style in a text-editor.",
    "use-slider": "Use a slider to select a particular value.",
    "use-slider-2": "Use sliders to create a given combination.",
    "copy-paste": "Copy text and paste it into an input.",
    "copy-paste-2": "Copy text from a specific textarea and paste it into an input.",
    "enter-text-2": "Convert given text to upper or lower case.",
    "find-word": "Find nth word in a block of text.",
    "read-table": "Read information out from a table.",
    "read-table-2": "Read multiple pieces of information out from a table.",
    "simple-algebra": "Solve for X.",
    "simple-arithmetic": "Perform some arithmetic math operations.",
    "terminal": "Use the terminal to delete a file.",
    "text-transform": "Enter slightly transformed text into a text box.",
    "visual-addition": "Count the total number of blocks.",
    "chase-circle": "Keep your mouse inside a moving circle.",
    "moving-items": "Click moving items before they disappear.",
    "simon-says": "Push the buttons in the order shown.",
}

# all_envs = list(gym.envs.registry.values())
# filtered_envs = []

# # Obtain filtered "list",
# for env_spec in tqdm(all_envs):
#     if env_spec.namespace != "miniwob":
#         continue
#     filtered_envs.append(env_spec)
# filtered_envs.sort(key=lambda x: x.name)


# # Update "Docs",
# for i, env_spec in tqdm(enumerate(filtered_envs)):
#     print("ID:", env_spec.id)
#     env_spec = gym.spec(env_spec.id)
#     print(env_spec)

file_start_content = """# Environments List

```{toctree}
:hidden:
:glob:

../environments/*
```

"""

list_md_path = os.path.join(os.path.dirname(__file__), "..", "environments", "list.md")
with open(list_md_path, "w") as fp:
    content = file_start_content
    for env_type in ENV_TYPES:
        df = pd.DataFrame(
            {
                "Name": [f"[{env}](./{env})" for env in env_type["envs"]],
                "Description": [ENVS_DESCRIPTIONS[env] for env in env_type["envs"]],
            }
        )
        type_name = env_type["name"]
        type_desc = env_type["description"]
        content += f"## {type_name}\n\n"
        content += f"{type_desc}\n\n"
        content += df.to_markdown(index=False) + "\n\n"

    content += """
## Missing

These tasks are listed in the original paper but were missing from the OpenAI
website.

|                   |                                                                  |
| ----------------- | ---------------------------------------------------------------- |
| ascending-numbers | Click on the numbers in ascending order.                         |
| button-delay      | Wait a certain period of time before clicking the second button. |
| buy-ticket        | Buy a ticket that matches the requested criteria.                |
| daily-calendar    | Create an event on a daily calendar.                             |
| drag-shape        | Drag a randomly generated shape in a specified direction.        |
| drag-shapes-2     | Drag shapes into boxes, categorized by type.                     |
| draw-circle       | Draw a circle around a marked point.                             |
| draw-line         | Draw a line through a marked point.                              |
| find-greatest     | Find the card with the greatest number.                          |
| form-sequence     | Perform a series of instructions on a form.                      |
| form-sequence-2   | Perform a series of instructions on a form.                      |
| form-sequence-3   | Perform a series of instructions on a form.                      |
| generate-number   | Generate a random number that meets certain criteria.            |
| hot-cold          | Find and click on the hot area.                                  |
| hover-shape       | Hover over the colored shape.                                    |
| odd-or-even       | Mark each number as odd or even.                                 |
| order-food        | Order food items from a menu.                                    |
| phone-book        | Find a contact in a phone book.                                  |
| sign-agreement    | Sign a user agreement.                                           |
| stock-market      | Buy from the stock market below a specified price.               |
"""
    fp.write(content)
