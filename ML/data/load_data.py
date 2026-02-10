from datasets import load_dataset

def load_skit():
    return load_dataset("skit-ai/skit-s2i")

def load_axon():
    return load_dataset("AxonData/multilingual-call-center-speech-dataset")

if __name__ == "__main__":
    skit = load_skit()
    print(skit)
    print(skit["train"][0])
