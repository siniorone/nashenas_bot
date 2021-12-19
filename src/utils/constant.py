from types import SimpleNamespace
from emoji import emojize

from src.utils.keyboard import create_keyboard

# In this part, useful keys are made.
keys = SimpleNamespace(
    random_connect=emojize(":game_die: Random Connect"),
    setting=emojize(":gear: Setting"),
    exit=emojize(":cross_mark: Discard"),
)
# Commonly used keyboards is designed in this section.
keyboards = SimpleNamespace(
    exit=create_keyboard(keys.exit),
    main=create_keyboard(keys.random_connect, keys.setting),
)
# User states
states = SimpleNamespace(
    random_connect='RANDOM_CONNECT',
    main='MAIN',
    connected='CONNECTED',
)
