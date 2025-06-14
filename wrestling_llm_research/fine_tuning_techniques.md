# In-Depth Fine-Tuning Methodologies for Wrestling LLMs

This document provides a more detailed exploration of specific fine-tuning techniques relevant to adapting Small Language Models (SLMs) for the professional wrestling domain, with a focus on Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA and various prompt tuning strategies.

## LoRA (Low-Rank Adaptation)

LoRA is a highly effective and popular PEFT technique that significantly reduces the number of trainable parameters during fine-tuning, making the process more accessible and efficient.

### Core Concept

The fundamental idea behind LoRA is that the change in weights of a pre-trained model during adaptation (ΔW) can be represented by a low-rank matrix. Instead of updating all the weights (W) of a layer, LoRA introduces two smaller, trainable matrices (A and B) whose product (AB) approximates ΔW. The original weights (W) are kept frozen.

*   **Pre-trained Weight Matrix (W_0):** Dimensions `d x k` (frozen).
*   **LoRA Matrices:**
    *   `A`: Dimensions `d x r` (trainable, initialized with random Gaussian values).
    *   `B`: Dimensions `r x k` (trainable, initialized with zeros, so AB is zero at the start of training, meaning no initial change to W_0).
*   **Rank (r):** A hyperparameter, typically a small integer (e.g., 4, 8, 16, 32). A smaller `r` means fewer trainable parameters.
*   **Modified Forward Pass:** `h = W_0x + α * BAx` (where `x` is the input, `h` is the output, and `α` is a scaling factor, often set to `1/r` or a constant like 1).

### Why it Works for Persona Tuning

*   **Efficiency:** Only `A` and `B` are trained. For a large weight matrix in a Transformer (e.g., in self-attention or feed-forward networks), the number of parameters in `A` and `B` (`d*r + r*k`) is much smaller than in `W` (`d*k`), especially when `r << d` and `r << k`.
*   **Modularity:** Different LoRA adapters (pairs of A and B matrices) can be trained for different tasks or personas. During inference, the appropriate adapter can be loaded and combined with the base model. This allows for many specialized versions without storing many full model copies.
*   **No Inference Latency (in principle):** Once trained, the LoRA matrices `A` and `B` can be merged with the original weights `W_0` by computing `W = W_0 + BA`. This means the adapted model has the same architecture and size as the original, incurring no additional inference latency compared to the base model. However, dynamically switching adapters without merging might have a small overhead.
*   **Effectiveness:** Despite its simplicity, LoRA has been shown to perform comparably to full fine-tuning on many tasks while being vastly more efficient.

### Implementation Details

*   **Target Layers:** LoRA is typically applied to the weight matrices in the self-attention mechanism (query, key, value projections: Wq, Wk, Wv) of Transformer models. It can also be applied to the feed-forward layers.
*   **Hugging Face `PEFT` Library:** The `peft` library from Hugging Face provides a straightforward way to implement LoRA. It allows users to specify the LoRA rank (`r`), `lora_alpha` (the scaling factor `α`), `lora_dropout`, and which modules (e.g., `q_proj`, `v_proj`) to apply LoRA to.
    ```python
    # Example conceptual snippet from Hugging Face PEFT
    from peft import LoraConfig, get_peft_model

    config = LoraConfig(
        r=8, # Rank
        lora_alpha=16, # Scaling factor (often 2*r)
        target_modules=["q_proj", "v_proj"], # Apply to query and value projections
        lora_dropout=0.05,
        bias="none", # Typically, biases are not trained with LoRA
        task_type="CAUSAL_LM" # Or "SEQ_2_SEQ_LM" depending on the model
    )

    # model = AutoModelForCausalLM.from_pretrained("base_model_name_or_path")
    # lora_model = get_peft_model(model, config)
    # lora_model.print_trainable_parameters() # Shows the drastic reduction
    ```

### Variations and Considerations

*   **QLoRA:** A more memory-efficient version that involves quantizing the base model to 4-bit precision and then applying LoRA. This further reduces memory footprint during training.
*   **Choosing `r` (Rank):** A higher rank means more expressive power for the adapter but also more parameters. The optimal rank can vary by task and dataset size and often requires some experimentation. Starting with a small rank like 8 or 16 is common.
*   **`lora_alpha`:** This scaling parameter can affect the learning process. A common heuristic is to set `lora_alpha` to be twice the rank `r`, but this can also be tuned.

For wrestling personas, LoRA allows for training individual adapters for different wrestlers, announcers, or promotional styles on top of a single, general wrestling-knowledgeable base model. This would be highly efficient for managing multiple distinct personalities.

## Prompt Tuning (and its variants like Prefix-Tuning)

Prompt Tuning is another set of PEFT techniques that, instead of modifying the LLM's weights, focuses on learning "soft prompts" or "virtual prompts" that are prepended to the input sequence to steer the model's behavior for specific tasks.

### Core Concept

The idea is that a sequence of continuous task-specific vectors (the soft prompt) can condition a frozen pre-trained model to perform well on a downstream task, similar to how natural language prompts guide LLMs in few-shot or zero-shot settings.

*   **Frozen Base Model:** The parameters of the pre-trained LLM remain entirely unchanged.
*   **Soft Prompt (P):** A sequence of `k` continuous embedding vectors (e.g., `P = [p_1, p_2, ..., p_k]`), each with the same dimension as the model's word embeddings. These prompt vectors are trainable parameters.
*   **Input Modification:** For an input sequence `X = [x_1, ..., x_m]`, the modified input becomes `[P, X] = [p_1, ..., p_k, x_1, ..., x_m]`.
*   **Training:** Only the soft prompt vectors `P` are updated during training to minimize the task-specific loss.

### Variants

1.  **Prompt Tuning (Lester et al., 2021):**
    *   Learns a sequence of `k` token embeddings (soft prompt) that are prepended to the input embeddings.
    *   The number of trainable parameters is very small (e.g., if `k=20` and embedding dimension is 768, only `20*768` parameters are trained).
    *   Surprisingly effective for large models (e.g., T5 11B), sometimes matching the performance of full fine-tuning.
    *   Performance can be sensitive to the length of the soft prompt (`k`) and initialization.

2.  **Prefix-Tuning (Li & Liang, 2021):**
    *   Similar to prompt tuning, but the trainable prefix vectors are added to the input of *every* Transformer layer, not just the input embedding layer.
    *   This gives the prefix more influence over the model's activations throughout its depth.
    *   The prefix parameters are typically generated by a smaller feed-forward network from a single prefix embedding, which helps stabilize training.
    *   Often more robust and performs better than prompt tuning, especially on smaller models or with limited data.

3.  **P-Tuning (Liu et al., 2021):**
    *   Introduces trainable continuous prompt embeddings but uses a small LSTM or MLP (a "prompt encoder") to generate these embeddings from a few discrete virtual prompt tokens. This can make the optimization more stable.
    *   Can be applied at the input layer.

### Why it Works for Persona Tuning

*   **Extreme Parameter Efficiency:** Even fewer parameters are trained compared to LoRA, making it very cheap to train and store multiple persona prompts.
*   **Preserves Base Model:** The base LLM's general knowledge and capabilities are fully preserved, which is beneficial as wrestling personas still rely on a vast amount of common sense and language understanding.
*   **Task-Specific Steering:** Soft prompts can learn to guide the model towards a specific style, tone, or knowledge domain relevant to a persona.
*   **Compositionality:** It might be possible to combine different soft prompts or use them in conjunction with other techniques like LoRA.

### Implementation Details

*   **Initialization:** The way soft prompt parameters are initialized can be crucial. Initializing them from the embeddings of relevant vocabulary words or task descriptions has been explored.
*   **Length of Soft Prompt (`k`):** This is a key hyperparameter. Longer prompts offer more capacity but are harder to tune. Typical lengths range from a few tokens to a few hundred.
*   **Hugging Face `PEFT` Library:** The `peft` library also supports various forms of prompt tuning.
    ```python
    # Example conceptual snippet for Prompt Tuning from Hugging Face PEFT
    from peft import PromptTuningConfig, get_peft_model, TaskType

    # For Prompt Tuning
    prompt_tuning_config = PromptTuningConfig(
        task_type=TaskType.CAUSAL_LM,
        prompt_tuning_init="TEXT", # Initialize with text
        num_virtual_tokens=20, # Length of the soft prompt
        prompt_tuning_init_text="Describe wrestling promos in an excited tone",
        tokenizer_name_or_path="base_model_name_or_path"
    )

    # model = AutoModelForCausalLM.from_pretrained("base_model_name_or_path")
    # prompt_tuned_model = get_peft_model(model, prompt_tuning_config)
    # prompt_tuned_model.print_trainable_parameters()
    ```
    ```python
    # Example conceptual snippet for Prefix Tuning from Hugging Face PEFT
    from peft import PrefixTuningConfig, get_peft_model, TaskType

    # For Prefix Tuning
    prefix_tuning_config = PrefixTuningConfig(
        task_type=TaskType.CAUSAL_LM,
        num_virtual_tokens=20, # Length of the prefix for each layer
        # prefix_projection=True # Older versions might have this, newer versions handle it differently
    )
    # model = AutoModelForCausalLM.from_pretrained("base_model_name_or_path")
    # prefix_tuned_model = get_peft_model(model, prefix_tuning_config)
    # prefix_tuned_model.print_trainable_parameters()
    ```

### Synergy with LoRA and Other Methods

*   **Prompt Tuning + LoRA:** It's conceivable to combine these methods. For instance, a general wrestling-domain LoRA adapter could be created, and then specific character personas could be further refined or steered using prompt tuning on top of that LoRA-adapted model.
*   **Instruction Fine-Tuning + Prompt Tuning:** If the base model is already instruction-tuned, prompt tuning can help it adapt to specific *styles* of instruction following, relevant for different wrestling personas (e.g., a polite announcer vs. a trash-talking wrestler).

For wrestling personas, prompt tuning offers a very lightweight way to create multiple character-specific behaviors. The challenge lies in crafting effective initialization for the soft prompts and finding the right length and training strategy to capture the nuances of complex personalities like those found in wrestling.

## Combining Techniques

A powerful approach for the wrestling domain could involve a multi-stage fine-tuning process:

1.  **Base SLM:** Start with a strong, general-purpose SLM (e.g., Mistral 7B, Llama 3.2 1B).
2.  **Domain Adaptation (Optional but Recommended):** Fine-tune this SLM on a broad corpus of general wrestling text (news, match results, general discussions) to make it "wrestling aware." This could be done with full fine-tuning if resources allow, or a general wrestling LoRA.
3.  **Role/Persona Adaptation:**
    *   Train separate LoRA adapters for specific roles (announcer, heel wrestler, face wrestler, promoter) or even highly distinct characters using curated datasets for each.
    *   Alternatively, or in combination, use prompt tuning (or prefix tuning) to instill the specific style of different characters/roles onto the domain-adapted model or the LoRA-adapted models.

This layered approach allows for building specialized capabilities efficiently while leveraging the strengths of different PEFT methods.
