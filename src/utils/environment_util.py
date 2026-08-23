from dotenv import load_dotenv


_ENV_LOADED = False


def load_env()->None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    load_dotenv(verbose=True)
    _ENV_LOADED = True