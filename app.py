import streamlit as st
import traceback
from processpiper.text2diagram import render
from PIL import Image

sample_codes = {
    "Sample 1": """#Showcase Process Piper plain text to diagram capability
title: Make pizza process
colourtheme: BLUEMOUNTAIN

# Define the swimlane and BPMN elements
lane: Pizza Shop
    (start) as start
    [Put the pizza in the oven] as put_pizza_in_oven
    [Check to see if pizza is done] as check_pizza_done
    <@exclusive Done baking?> as done_baking
    [Take the pizza out of the oven] as take_pizza_out_of_oven
    (end) as end

# Connect all the elements    
start->put_pizza_in_oven->check_pizza_done->done_baking
done_baking-"Yes"->take_pizza_out_of_oven->end
done_baking-"No"->put_pizza_in_oven""",
    "Sample 2": """title: Sample Test Process
colourtheme: BLUEMOUNTAIN
    lane: End User
        (start) as start
        [Enter Keyword] as enter_keyword
        (end) as end
pool: System Search
    lane: Database System
        [Login] as login
        [Search Records] as search_records
        <Result Found?> as result_found
        [Display Result] as display_result
        [Logout] as logout
    lane: Log System
        [Log Error] as log_error

start->login->enter_keyword->search_records->result_found->display_result->logout->end
result_found->log_error->display_result

footer: Generated by ProcessPiper
    """,
}

help_text = """
                The syntax for defining a process map is as follows:

- `title`: The title of the diagram.
- `colourtheme`: The colour theme to use
- `lane`: The name of the lane.
- `pool`: The name of the pool.
- To add elements to the lane, use one of the following tags. You place your element description within the tag:
  - Use `(` and `)` to create event element
    - use `(start)` to create a start event
    - use `(end)` to create an end event
    - use `(@timer` and `)` to create a timer event. Example `(@timer Trigger every 1 hour) as timer_event`
    - use `(@intermediate` and `)` to create an intermediate event. Example `(@intermediate Message Received) as intermediate_event`
  - Use `[` and `]` to create an activity. By default, the activity type is `TASK`. Example `[Place Order] as place_order`
    - use `[@subprocess]` to create a subprocess. Example `[@subprocess Get Approval] as get_approval`` 
  - Use `<` and `>` to create a gateway. By default, the gateway type is `EXCLUSIVE`. Example `<Result Found?> as result_found`
    - Use `<@parallel` and `>` to create a parallel gateway. Example `<@parallel Span Out> as span_out`
    - Use `<@inclusive` and `>` to create an inclusive gateway. Example `<@inclusive Condition Met?> as condition_met`
- To connect two elements, use `->`. You can chain multiple connections using `->`:
  - Example: 
    - login->enter_keyword
    - start->login->enter_keyword->search_records->result_found->display_result->logout->end
- `footer`: The footer text to display on the diagram.

Indentation is not required. However, it is recommended to use indentation to make the diagram easier to read.
                """


def generate_diagram(input_text: str):
    output_image_file = "output.png"
    # Call the render function to generate the diagram
    try:
        generated_code, generated_image = render(input_text, output_image_file)
        st.text("Generated code:")
        st.code(generated_code)
        # st.success("Diagram generated successfully")
        # generated_image = Image.open(output_image_file)
        # return generated_image
        return output_image_file
    except Exception as e:
        print(e)
        return


st.set_page_config(
    page_title="Piperita: Business Process Diagram Generator",
    page_icon=":herb:",
    layout="centered",
    menu_items={
        "Get Help": "https://github.com/csgoh/processpiper/wiki/Usage-Documentation",
        "Report a bug": "https://github.com/csgoh/processpiper/issues",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)
st.markdown(
    "<div style='text-align:center'>Made in New Zealand by <a href='https://github.com/csgoh'>CSGOH</a>. Source code available on <a href='https://github.com/csgoh/Piperita'>GitHub</a>.</div>",
    unsafe_allow_html=True,
)

# st.title("Piperita: Business Process Diagram Generator")
st.header("Piperita: Business Process Diagram Generator")
st.markdown(
    "Piperita is a web frontend to showcase the [ProcessPiper](https://github.com/csgoh/processpiper) python package. ProcessPiper is a package for generating business process diagrams from plain text."
)

st.markdown(
    "For help on the syntax, refer to the [Usage Documentation](https://github.com/csgoh/processpiper/wiki/Usage-Documentation#method-1-generate-bpmn-diagram-using-plain-text)."
)

st.write("Select a sample diagram from dropdown.")
selected_sample = st.selectbox("Pick one", list(sample_codes.keys()), index=0)
if selected_sample:
    code = sample_codes[selected_sample]
else:
    code = ""

generate_buton = st.button("Generate")


code = st.text_area(
    "Select a sample from the sidebar or enter your code below:", value=code, height=400
)


if generate_buton:
    try:
        output_image_file = generate_diagram(code)
        st.write(f"output image fie :[{output_image_file}]")
        diagram = Image.open(output_image_file)
        # gen_image = st.image(
        #     diagram,
        #     caption="Generated Business Process Diagram",
        #     use_column_width=True,
        # )

    except Exception as e:
        # st.error(f"Error generating diagram: {e}")
        # Get the entire traceback as a string
        tb_str = traceback.format_exc()

        # Display the error message with the entire traceback
        st.error(f"Error generating diagram: {e}\n{tb_str}")
