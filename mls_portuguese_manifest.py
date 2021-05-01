import os
from pathlib import Path
import pandas as pd

os.system('wget https://dl.fbaipublicfiles.com/mls/mls_portuguese.tar.gz')
os.system('tar -xvf mls_portuguese.tar.gz')

folder = Path('mls_portuguese')

train_paths = list(folder.glob('train/audio/*/*/*.flac'))
dev_paths = list(folder.glob('dev/audio/*/*/*.flac'))
test_paths = list(folder.glob('test/audio/*/*/*.flac'))

train_df = pd.read_csv('mls_portuguese/train/transcripts.txt', sep='\t', encoding='utf-8', header=None)
dev_df = pd.read_csv('mls_portuguese/dev/transcripts.txt', sep='\t', encoding='utf-8', header=None)
test_df = pd.read_csv('mls_portuguese/test/transcripts.txt', sep='\t', encoding='utf-8', header=None)

train_df.columns = ['wav_paths', 'text']
dev_df.columns = ['wav_paths', 'text']
test_df.columns = ['wav_paths', 'text']

train_df['wav_paths'] = train_df['wav_paths'].apply(lambda x: f"mls_portuguese/train/audio/{x.split('_')[0]}/{x.split('_')[1]}/{x}.flac")
dev_df['wav_paths'] = dev_df['wav_paths'].apply(lambda x: f"mls_portuguese/dev/audio/{x.split('_')[0]}/{x.split('_')[1]}/{x}.flac")
test_df['wav_paths'] = test_df['wav_paths'].apply(lambda x: f"mls_portuguese/test/audio/{x.split('_')[0]}/{x.split('_')[1]}/{x}.flac")

train_df['new_wav_paths'] = train_df['wav_paths'].apply(lambda x: f"mls_portuguese/train/audios/{x.split('/')[-1]}")
dev_df['new_wav_paths'] = dev_df['wav_paths'].apply(lambda x: f"mls_portuguese/dev/audios/{x.split('/')[-1]}")
test_df['new_wav_paths'] = test_df['wav_paths'].apply(lambda x: f"mls_portuguese/test/audios/{x.split('/')[-1]}")

dfs = [train_df, dev_df, test_df]

if not os.path.exists('mls_portuguese/train/audios'):
    os.mkdir('mls_portuguese/train/audios')
if not os.path.exists('mls_portuguese/dev/audios'):
    os.mkdir('mls_portuguese/dev/audios')
if not os.path.exists('mls_portuguese/test/audios'):
    os.mkdir('mls_portuguese/test/audios')

for df in dfs:
  for row in df.index:
    os.rename(df['wav_paths'][row], df['new_wav_paths'][row])


os.system('rm -rf mls_portuguese/train/audio')
os.system('rm -rf mls_portuguese/train/limited_supervision')
os.system('rm -rf mls_portuguese/dev/audio')
os.system('rm -rf mls_portuguese/test/audio')
os.system('rm -rf mls_portuguese/*.txt')
os.system('rm -rf mls_portuguese/*/*.txt')

train_transcripts = train_df[['new_wav_paths', 'text']]
dev_transcripts = dev_df[['new_wav_paths', 'text']]
test_transcripts = test_df[['new_wav_paths', 'text']]

train_transcripts.columns = ['wav_paths', 'transcripts']
dev_transcripts.columns = ['wav_paths', 'transcripts']
test_transcripts.columns = ['wav_paths', 'transcripts']

train_transcripts.to_csv('mls_portuguese/train_transcripts.tsv', sep='\t', encoding='utf-8')
dev_transcripts.to_csv('mls_portuguese/dev_transcripts.tsv', sep='\t', encoding='utf-8')
test_transcripts.to_csv('mls_portuguese/test_transcripts.tsv', sep='\t', encoding='utf-8')