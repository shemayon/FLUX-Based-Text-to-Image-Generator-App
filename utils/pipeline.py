import torch
from diffusers import FluxPipeline
from utils.helper_functions import get_next_run_id

torch.cuda.empty_cache()

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)
pipe.enable_sequential_cpu_offload()
pipe.enable_model_cpu_offload()
pipe.load_lora_weights("kudzueye/boreal-flux-dev-v2", weight_name="boreal-v2.safetensors")
pipe.fuse_lora(lora_scale=0.8)
pipe.enable_attention_slicing()


def generate(prompt, neg_prompt):
    run_id = get_next_run_id()
    gender, age, safe_id = "na", "na", "custom"

    img = pipe(
        prompt=prompt,
        negative_prompt=neg_prompt,
        height=1024,
        width=1024,
        num_inference_steps=30,
    ).images[0]

    fname = f"outputs/run{run_id}_{safe_id}_{gender}_{age}.png"
    img.save(fname)
    return img, f"Saved ➜ {fname}"