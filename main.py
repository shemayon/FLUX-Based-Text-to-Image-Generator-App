import gradio as gr
from utils.pipeline import generate

# -----------------------------  GRADIO INTERFACE  ---------------------------
CSS = """
#app-container {max-width: 600px;margin-left:auto;margin-right:auto;}
#title-container {display:flex;align-items:center;justify-content:center;}
#title-icon {width:32px;height:auto;margin-right:10px;}
#title-text {font-size:24px;font-weight:bold;}
"""

DEFAULT_NEG_PROMPT = (
    "(deformed, distorted, disfigured), poorly drawn, bad anatomy, wrong anatomy, "
    "extra limb, missing limb, floating limbs, (mutated hands and fingers), "
    "disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, "
    "misspellings, typos"
)



with gr.Blocks(theme="Nymbo/Nymbo_Theme", css=CSS) as app:
    gr.HTML(
        """
        <center>
            <div id="title-container">
                <h1 id="title-text">Text to Image Generator using Flux</h1>
            </div>
        </center>
        """
    )

    with gr.Column(elem_id="app-container"):
        with gr.Row():
            with gr.Column(elem_id="prompt-container"):
                with gr.Row():
                    txt_prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="Enter a prompt here",
                        lines=2,
                        elem_id="prompt-text-input",
                    )
                with gr.Row():
                    with gr.Accordion("Advanced Settings", open=False):
                        neg_prompt = gr.Textbox(
                            label="Negative Prompt",
                            placeholder="What should not be in the image",
                            value=DEFAULT_NEG_PROMPT,
                            lines=3,
                            elem_id="negative-prompt-text-input",
                        )
        with gr.Row():
            gen_btn = gr.Button("🚀 Generate")
        img_out = gr.Image(label="Result", interactive=False)
        path_out = gr.Markdown()

    gen_btn.click(
        fn=generate,
        inputs=[txt_prompt, neg_prompt],
        outputs=[img_out, path_out],
    )

app.launch(share=True)
