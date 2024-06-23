import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

base_path = '/app/OpenVoice/'

ckpt_converter = base_path + 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_v2'

print(" > Loading tone color converter.")
tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

print(" > Loading SE extractor.")
reference_speaker = base_path + 'resources/example_reference.mp3' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

from melo.api import TTS

texts = {
    'EN_NEWEST': "Did you ever hear a folk tale about a giant turtle?",  # The newest English base speaker model
    'EN': "Did you ever hear a folk tale about a giant turtle?",
    #'ES': "El resplandor del sol acaricia las olas, pintando el cielo con una paleta deslumbrante.",
    #'FR': "La lueur dorée du soleil caresse les vagues, peignant le ciel d'une palette éblouissante.",
}

print(texts.items())

src_path = f'{output_dir}/tmp.wav'

# Speed is adjustable
speed = 1.0

for language, text in texts.items():
    print(language)
    model = TTS(language=language, device=device)
    speaker_ids = model.hps.data.spk2id
    
    for speaker_key in speaker_ids.keys():
        speaker_id = speaker_ids[speaker_key]
        speaker_key = speaker_key.lower().replace('_', '-')
        
        print(f'  > Speaker {speaker_key}')
        source_se = torch.load(f'{base_path}checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
        model.tts_to_file(text, speaker_id, src_path, speed=speed)
        save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

        print(f'  > Saving {save_path}')
        # Run the tone color converter
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=src_path, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=save_path,
            message=encode_message)
        
print("Finished!")
        