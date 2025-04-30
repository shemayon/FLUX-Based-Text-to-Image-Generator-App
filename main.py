import torch
torch.cuda.empty_cache()
from diffusers import FluxPipeline
import json
import os
import re

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)

pipe.enable_sequential_cpu_offload()
pipe.enable_model_cpu_offload()
# pipe.to("cpu")


# Load the LoRA weights
pipe.load_lora_weights(
    "kudzueye/boreal-flux-dev-v2", 
    weight_name="boreal-v2.safetensors"
)

# Fuse LoRA with scaling
pipe.fuse_lora(lora_scale=0.8)

# Reduces memory use during attention computations
pipe.enable_attention_slicing()


## Run inference

# Set run ID
def get_next_run_id(outputs_dir='outputs'):
    # Regular expression pattern to match filenames
    pattern = re.compile(r'^run(\d+)_\w+_\w+_\w+\.png$')

    # Make sure the outputs folder exists
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
        return 1

    run_ids = []

    for filename in os.listdir(outputs_dir):
        match = pattern.match(filename)
        if match:
            run_ids.append(int(match.group(1)))

    return max(run_ids, default=0) + 1

# Get run ID for the current run
current_run_id = get_next_run_id()

# Set constant negative prompt
negative_prompt = """messy hair, exaggerated makeup, low resolution, shadows on face, blurry, harsh lighting,
busy background, distorted features, poor posture, open mouth, casual clothing,
artistic style, cartoon, painting, sketch, unrealistic skin texture"""

with open('prompts.json', 'r') as f:
    prompts_data = json.load(f)

# Iterate through the prompts and call the generation function
for image_id, details in prompts_data.items():
    prompt = details['prompt']
    gender = details['gender']
    age = details['age']
    
    # Generate image
    print('Genration started for image ID:', image_id)
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=1024,
        width=1024,
        num_inference_steps=30
    ).images[0]

    # Save image
    image.save(f"outputs/run{current_run_id}_{image_id}_{gender}_{age}.png")