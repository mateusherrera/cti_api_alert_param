"""
Padronização de menssagens de retorno para APIs de serviços.

:created by:        Mateus Herrera
:created at:        2025-02-02
"""


class ResponseMessages:
    """ Classe para armazenar mensagens de retorno dos endpoints de serviços. """

    SUCCESS_CREATE_ALERT        = 'Alerta criado com sucesso.'

    ERROR_EMPTY_BODY            = 'O corpo da requisição está vazio.'
    ERROR_MISSING_FIELDS        = 'Parâmetro obrigatório não informado.'
    ERROR_GET_REQUEST           = 'Erro ao tentar obter a requisição.'
    ERROR_INVALID_DATE          = 'Data inválida.'
    ERROR_CREATE_ALERT          = 'Erro ao tentar criar alerta.'
    pass
