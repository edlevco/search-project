import gradio as gr
import matplotlib.pyplot as plt
import io, random
from PIL import Image


## this functions draws the visualization frame
def draw_frame(arr, left, mid, right, explanation):
    colors = []
    for i in range(len(arr)):
        if i == mid:
            colors.append("orange")
        elif i == left:
            colors.append("green")
        elif i == right:
            colors.append("red")
        else:
            colors.append("darkgrey")

    plt.figure(figsize=(7, 3))
    plt.bar(range(len(arr)), arr, color=colors)
    plt.title(f"left={left}, mid={mid}, right={right}")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return Image.open(buf), explanation


## This shows the current frame
def compute_frame(state, prefix=""):
    arr = state["arr"]
    left = state["left"]
    right = state["right"]
    target = state["target"]

    if left > right:
        img, exp = draw_frame(
            arr, None, None, None,
            prefix + f"❌ No more range available. Target {target} not found."
        )
        return img, exp

    mid = (left + right) // 2
    state["mid"] = mid

    explanation = prefix + f"Checking index {mid} (value={arr[mid]})."
    img, exp = draw_frame(arr, left, mid, right, explanation)
    return img, exp

## this start search function validates inputs like target number and array
def start_search(array_str, target):
    # Validate that target is an integer
    try:
        target_val = float(target)
    except:
        return None, None, "❌ ERROR: Target must be a number."

    # Make sure it's an integer (no decimals allowed)
    if not target_val.is_integer():
        return None, None, "❌ ERROR: Target must be an integer (no decimals)."

    target_val = int(target_val)

    # Validate the array
    try:
        arr = [int(x.strip()) for x in array_str.split(",")]
    except:
        return None, None, "❌ ERROR: Array must contain comma-separated integers (nothing else)."
    
    # Validate the arrays order

    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            return None,None, "❌ ERROR: Array must be in increasing order."
            

    # Build initial state
    state = {
        "arr": arr,
        "left": 0,
        "right": len(arr) - 1,
        "mid": None,
        "target": target
    }

    img, exp = compute_frame(state, "Starting search. ")
    return img, state, exp


## This is the function if the user chooses left as their option to search
def choose_left(state):
    arr = state["arr"]
    mid = state["mid"]
    target = state["target"]

    ## If the middle is the target
    if arr[mid] == target:
        img, exp = draw_frame(
            arr, state["left"], mid, state["right"],
            f"❌ Incorrect — the target {target} is RIGHT HERE at index {mid}!"
        )
        return img, exp


    ## this checks if the got the correct direction
    correct = target < arr[mid]
    if correct:
        feedback = f"✅ Correct! {target} < {arr[mid]}, so go LEFT."
        state["right"] = mid - 1
    else:
        feedback = f"❌ Incorrect. {target} > {arr[mid]}, so binary search SHOULD go RIGHT."
        state["left"] = mid + 1

    # Check if search is finished BEFORE computing the next frame
    if state["left"] > state["right"]:
        img, exp = draw_frame(arr, None, None, None, feedback + f" ❌ No more range. Target {target} not found.")
        return img, exp

    return compute_frame(state, feedback + " ")

## this function is called if the user selects right to search
def choose_right(state):
    arr = state["arr"]
    mid = state["mid"]
    target = state["target"]

    if arr[mid] == target:
        img, exp = draw_frame(
            arr, state["left"], mid, state["right"],
            f"❌ Incorrect — the target {target} is RIGHT HERE at index {mid}!"
        )
        return img, exp

    correct = target > arr[mid]
    if correct:
        feedback = f"✅ Correct! {target} > {arr[mid]}, so go RIGHT."
        state["left"] = mid + 1
    else:
        feedback = f"❌ Incorrect. {target} < {arr[mid]}, so binary search SHOULD go LEFT."
        state["right"] = mid - 1

    # Check termination FIRST
    if state["left"] > state["right"]:
        img, exp = draw_frame(arr, None, None, None, feedback + f" ❌ No more range. Target {target} not found.")
        return img, exp

    return compute_frame(state, feedback + " ")


## if the user chooses found this function is called and confirms their check
def choose_found(state):
    arr = state["arr"]
    mid = state["mid"]
    target = state["target"]

    # Correct guess
    if arr[mid] == target:
        img, exp = draw_frame(
            arr, state["left"], mid, state["right"],
            f"🎯 Correct! {target} IS at index {mid}!"
        )
        return img, exp

    # Wrong guess — continue binary search correctly
    if arr[mid] < target:
        state["left"] = mid + 1
        feedback = f"❌ Incorrect. {arr[mid]} < {target}, so search SHOULD go RIGHT."
    else:
        state["right"] = mid - 1
        feedback = f"❌ Incorrect. {arr[mid]} > {target}, so search SHOULD go LEFT."

    # Termination
    if state["left"] > state["right"]:
        img, exp = draw_frame(
            arr, None, None, None,
            feedback + f" ❌ No more range. Target {target} not found."
        )
        return img, exp

    return compute_frame(state, feedback + " ")



## This function is used to generate a random increasing array for the user
def generate_random_array():
    arr = sorted(random.sample(range(1, 101), 20))
    return ",".join(str(x) for x in arr)

## This is how the site is planned out and visualized
with gr.Blocks(title="Binary Search Helper") as demo:

    gr.Markdown("## Binary Search Helper\nChoose LEFT, RIGHT, or FOUND at each step. Get feedback!")

    with gr.Row():
        array_in = gr.Textbox(
            value="6,7,10,11,12,17,19,22,24,26,29,41,43,50,66,70,73,76,86,88",
            label="Array (comma separated)"
        )
        random_btn = gr.Button("Generate Random Array")

    target_in = gr.Number(label="Target Value")

    start_btn = gr.Button("Start Search", variant="primary")

    img_out = gr.Image(label="Visualization")
    text_out = gr.Textbox(label="Explanation", lines=3)
    state = gr.State()

    with gr.Row():
        left_btn = gr.Button("⬅️ LEFT")
        right_btn = gr.Button("➡️ RIGHT")
        found_btn = gr.Button("🎯 FOUND")

    random_btn.click(generate_random_array, outputs=array_in)
    start_btn.click(start_search, [array_in, target_in], [img_out, state, text_out])

    left_btn.click(choose_left, [state], [img_out, text_out])
    right_btn.click(choose_right, [state], [img_out, text_out])
    found_btn.click(choose_found, [state], [img_out, text_out])

demo.launch()



