from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager
import numpy as np
import torch
import os
import io

class TTSManager:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        print("Initializing TTS Manager...")
        model_name = 'tts_models/multilingual/multi-dataset/xtts_v2'
        reference_audio = 'skull.wav'  # You'll need to create this reference audio
        
        print("Downloading XTTS Model:", model_name)
        ModelManager().download_model(model_name)
        model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
        
        print("Creating Model")
        config = XttsConfig()
        config.load_json(os.path.join(model_path, "config.json"))
        self.model = Xtts.init_from_config(config)
        self.model.load_checkpoint(config, checkpoint_dir=model_path, eval=True)
        self.model.to(device)
        
        # Get speaker conditioning from reference audio
        self.gpt_cond_latent, self.speaker_embedding = self.model.get_conditioning_latents(
            audio_path=f"audio/{reference_audio}",
            gpt_cond_len=30,
            gpt_cond_chunk_len=4,
            max_ref_length=60
        )

    def generate_audio_stream(self, text, language="en"):
        """Generate audio stream chunks"""
        chunks = self.model.inference_stream(
            text,
            language,
            self.gpt_cond_latent,
            self.speaker_embedding,
            stream_chunk_size=20,
            enable_text_splitting=True
        )
        
        for chunk in chunks:
            if isinstance(chunk, list):
                chunk = torch.cat(chunk, dim=0)
            chunk = chunk.clone().detach().cpu().numpy()
            chunk = chunk[None, : int(chunk.shape[0])]
            chunk = np.clip(chunk, -1, 1)
            chunk = (chunk * 32767).astype(np.int16)
            yield chunk.tobytes() 