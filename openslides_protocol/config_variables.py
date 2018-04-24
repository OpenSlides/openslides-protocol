from openslides.core.config import ConfigVariable


def get_config_variables():
    """
    Generator which yields all config variables of this app.
    It has to be evaluated during app loading (see apps.py).
    """
    yield ConfigVariable(
        name='protocol_motion_reason',
        default_value=True,
        input_type='boolean',
        label='Add motion reason in protocol',
        weight=1300,
        group='Protocol',
        subgroup='Motions')
