from pathlib import Path
import os


def getSecretPath():
    current = Path(__file__).resolve()
    for parent in current.parents:
        secretFile = parent / "secret.txt"
        if secretFile.exists():
            return secretFile
    return None

    # loads secrets from file for running on machine


def loadSecrets():
    secretPath = getSecretPath()
    if secretPath and os.path.exists(secretPath):
        with open(secretPath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
