import ollama
import os
import csv

# Caminho para o diretório raiz do dataset
dataset_path = "dataset"

# Função para gerar a descrição de uma imagem com LLaVA
def descrever_imagem(image_path):
  """
  Gera a descrição de uma imagem usando o modelo LLaVA.

  Args:
    image_path: Caminho para a imagem.

  Returns:
    Uma string com a descrição da imagem.
  """
  print(f"Descrevendo imagem: {image_path}")  # Print para mostrar a imagem sendo processada
  res = ollama.chat(
      model="llava",
      messages=[
          {
              'role': 'user',
              'content': 'Describe the gesture in the image, focus on the hands gesture:',
              'images': [image_path]
          }
      ]
  )
  return res['message']['content']


# Função para analisar um gesto e gerar as anotações
def analisar_gesto(user_path, gesture_path):
  """
  Analisa um gesto e gera as anotações.

  Args:
    user_path: Caminho para o diretório do usuário.
    gesture_path: Caminho para o diretório do gesto.

  Returns:
    Um dicionário com as anotações do gesto.
  """
  imagens = os.listdir(gesture_path)
  c_type = "dinâmico" if len(imagens) > 1 else "estático"
  c_num = len(imagens)
  c_description = ""

  # Gera a descrição do gesto com base nas imagens
  for imagem in imagens:
    image_path = os.path.join(gesture_path, imagem)
    c_description += descrever_imagem(image_path) + " "

  # Define o nome do gesto com base no nome do diretório
  gesture_name = os.path.basename(gesture_path)
  gesture_mapping = {
      "c1": "increase_volume",
      "c2": "decrease_volume",
      "c3": "mute_mic",
      "c4": "unmute_mic",
      "c5": "turn_off_camera",
      "c6": "turn_on_camera",
      "c7": "ask_to_talk",
      "c8": "end_call",
  }
  c_gesture_name = gesture_mapping.get(gesture_name, "")

  anotacoes = {
      "c_type": c_type,
      "c_num": c_num,
      "c_gesture_name": c_gesture_name,
      "c_description": c_description.strip(),
  }
  return anotacoes


# Abre o arquivo CSV para escrita
with open("anotacoes_llava.csv", "w", newline="") as csvfile:
  # Define o cabeçalho do CSV
  fieldnames = [
      "id_user", "c1_type", "c1_num", "c1_increase_volume", "c1_description",
      "c2_type", "c2_num", "c2_decrease_volume", "c2_description", "c3_type",
      "c3_num", "c3_mute_mic", "c3_description", "c4_type", "c4_num",
      "c4_unmute_mic", "c4_description", "c5_type", "c5_num",
      "c5_turn_off_camera", "c5_description", "c6_type", "c6_num",
      "c6_turn_on_camera", "c6_description", "c7_type", "c7_num",
      "c7_ask_to_talk", "c7_description", "c8_type", "c8_num", "c8_end_call",
      "c8_description"
  ]
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  # Itera sobre os usuários
  for user in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user)
    if os.path.isdir(user_path):
      print(f"Processando usuário: {user}")  # Print para mostrar o usuário sendo processado
      anotacoes_user = {"id_user": user}
      # Itera sobre os gestos
      for gesture in os.listdir(user_path):
        gesture_path = os.path.join(user_path, gesture)
        if os.path.isdir(gesture_path):
          print(f"Analisando gesto: {gesture}")  # Print para mostrar o gesto sendo analisado
          # Analisa o gesto e gera as anotações
          anotacoes_gesto = analisar_gesto(user_path, gesture_path)
          # Adiciona as anotações do gesto às anotações do usuário
          anotacoes_user.update({
              f"{gesture}_type": anotacoes_gesto["c_type"],
              f"{gesture}_num": anotacoes_gesto["c_num"],
              f"{gesture}_{anotacoes_gesto['c_gesture_name']}": anotacoes_gesto["c_gesture_name"],
              f"{gesture}_description": anotacoes_gesto["c_description"],
          })
      # Escreve as anotações do usuário no CSV
      writer.writerow(anotacoes_user)
      print(f"Usuário {user} processado com sucesso!")  # Print para indicar o término do processamento do usuário