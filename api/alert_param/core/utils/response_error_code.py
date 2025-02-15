"""
Padronização de códigos de retorno (específicos) para APIs de serviços.

:created by:        Mateus Herrera
:created at:        2025-02-02
"""


class ResponseErrorCode:
    """ Classe para armazenar códigos de retorno dos endpoints de serviços. """

    ERROR_EMPTY_BODY                    = ( 1, 'O corpo da requisição está vazio.'                      )
    ERROR_MISSING_FIELDS                = ( 2, 'Parâmetro obrigatório não informado.'                   )
    ERROR_GET_REQUEST                   = ( 3, 'Erro ao tentar obter a requisição.'                     )
    ERROR_INVALID_DATE                  = ( 4, 'Data Final já passou.'                                  )
    ERROR_START_DATE                    = ( 5, 'Data Inicial não pode ser maior que a Data Final.'      )
    ERROR_CREATE_ALERT                  = ( 6, 'Erro ao tentar criar alerta.'                           )
    ERROR_ADD_KEYWORD                   = ( 7, 'Erro ao tentar adicionar palavra-chave.'                )
    ERROR_ADD_FORUM                     = ( 8, 'Erro ao tentar adicionar fórum.'                        )
    ERROR_ADD_EMAIL                     = ( 9, 'Erro ao tentar adicionar e-mail.'                       )

    ERROR_LIST_ALERTS                   = (10, 'Erro ao tentar listar alertas.'                         )
    ERROR_LIST_ALERTS_BY_USER           = (11, 'Erro ao tentar listar alertas por usuário.'             )
    ERROR_LIST_ACTIVE_ALERTS_BY_USER    = (12, 'Erro ao tentar listar alertas ativos por usuário.'      )
    ERROR_LIST_RUN_TODAY                = (13, 'Erro ao tentar listar alertas que deve rodar hoje.'     )

    ERROR_ALERT_UPDATE_RUN              = (14, 'Erro ao tentar atualizar próximo dia a rodar alerta.'   )
    ERROR_DEACTIVATE_ALERT              = (15, 'Erro ao tentar desativar alerta. Não encontrado'        )

    ERROR_UPDATE_KEYWORDS               = (16, 'Erro ao tentar atualizar palavras-chave.'               )
    ERROR_UPDATE_FORUMS                 = (17, 'Erro ao tentar atualizar fóruns.'                       )
    ERROR_UPDATE_EMAILS                 = (18, 'Erro ao tentar atualizar e-mails.'                      )

    ERROR_CREATE_POST_ALERTED           = (19, 'Erro ao tentar criar post alertado.'                    )
    ERROR_LIST_POSTS_ALERTED            = (20, 'Erro ao tentar listar posts alertados.'                 )
    ERROR_LIST_POSTS_ALERTED_BY_ALERT   = (21, 'Erro ao tentar listar posts alertados por alerta.'      )
    pass
