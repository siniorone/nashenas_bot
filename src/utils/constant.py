from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

# In this part, useful keys are made.
keys = SimpleNamespace(
    random_connect = ":busts_in_silhouette: Random Connect",
    setting = ":gear: Setting",
)

# Commonly used keyboards is designed in this section.
keyboards = SimpleNamespace(
    main = create_keyboard(keys.random_connect, keys.setting),
)