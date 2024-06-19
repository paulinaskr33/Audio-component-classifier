"""
Source of this code: https://github.com/microsoft/CLAP/tree/main/examples

This is an example using CLAP for zero-shot inference.
"""
from msclap import CLAP
import torch.nn.functional as F
import torch.cuda

class AudioClassifier():
  def __init__(self) -> None:
    # Load and initialize CLAP
    # Setting use_cuda = True will load the model on a GPU using CUDA
    self.clap_model = CLAP(version = '2023', use_cuda=True)
    
  def predict(self, classes, audio_files ):
    # Add prompt
    prompt = 'this is a sound of '
    class_prompts = [prompt + x for x in classes]

    # compute text embeddings from natural text
    text_embeddings = self.clap_model.get_text_embeddings(class_prompts)

    # compute the audio embeddings from an audio file
    audio_embeddings = self.clap_model.get_audio_embeddings(audio_files, resample=True)
    
    # compute the similarity between audio_embeddings and text_embeddings
    similarity = self.clap_model.compute_similarity(audio_embeddings, text_embeddings)

    similarity = F.softmax(similarity, dim=1)
    values, indices = similarity[0].topk(1)

    return values, indices
  

if __name__ == '__main__':
  # Define classes for zero-shot
  # Should be in lower case and can be more than one word
  classes = ['Monkey chirping', 'Elephant', 'Lion rawring', 'Clapping', 'Laughter','Footsteps']
  ground_truth = ['Monkey']
  audio_files = ["../data/raw/test_monkey.wav"]

  clf = AudioClassifier()

  values, indices = clf.predict(classes, audio_files)
  # Print the results
  print("Ground Truth: {}".format(ground_truth))
  print("Top predictions:\n")
  for value, index in zip(values, indices):
      print(f"{classes[index]:>16s}: {100 * value.item():.2f}%")

  """
  The output (the exact numbers may vary):

  Ground Truth: coughing
  Top predictions:

          coughing: 98.55%
          sneezing: 1.24%
  drinking sipping: 0.15%
        breathing: 0.02%
    brushing teeth: 0.01%
  """
