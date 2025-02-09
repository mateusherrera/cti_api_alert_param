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

    LIST_ALERTS                 = 'Alertas listados com sucesso.'

    ERROR_LIST_ALERTS           = 'Erro ao tentar listar alertas.'
    ERROR_FOUND_ALERT           = 'Alerta não encontrado.'

    ALERT_INACTIVE              = 'Alerta foi inativado.'
    ALERT_INACTIVE_METHOD       = 'Alerta desativado com sucesso.'

    ALERT_RUN_UPDATED           = 'Próximo dia a rodar alerta atualizado com sucesso.'
    ALERT_KEYWORDS_UPDATED      = 'Palavras-chave do alerta atualizadas com sucesso.'
    ALERT_FORUMS_UPDATED        = 'Fóruns do alerta atualizados com sucesso.'
    ALERT_EMAILS_UPDATED        = 'Emails do alerta atualizados com sucesso.'

    ERROR_ALERT_UPDATE_RUN      = 'Erro ao tentar atualizar próximo dia a rodar alerta.'
    ERROR_ALERT_UPDATE_KEYWORDS = 'Erro ao tentar atualizar palavras-chave do alerta.'
    ERROR_ALERT_UPDATE_FORUMS   = 'Erro ao tentar atualizar fóruns do alerta.'
    ERROR_ALERT_UPDATE_EMAILS   = 'Erro ao tentar atualizar emails do alerta.'
    pass
