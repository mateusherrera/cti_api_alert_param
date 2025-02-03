"""
Padronização de códigos de retorno (específicos) para APIs de serviços.

:created by:        Mateus Herrera
:created at:        2025-02-02
"""


class ResponseErrorCode:
    """ Classe para armazenar códigos de retorno dos endpoints de serviços. """

    ERROR_EMPTY_BODY                    = ( 1, 'O corpo da requisição está vazio.'          )
    ERROR_MISSING_FIELDS                = ( 2, 'Parâmetro obrigatório não informado.'       )
    ERROR_GET_REQUEST                   = ( 3, 'Erro ao tentar obter a requisição.'         )
    ERROR_INVALID_DATE                  = ( 4, 'Data Final já passou.'                      )
    ERROR_CREATE_ALERT                  = ( 5, 'Erro ao tentar criar alerta.'               )
    ERROR_ADD_KEYWORD                   = ( 6, 'Erro ao tentar adicionar palavra-chave.'    )
    ERROR_ADD_FORUM                     = ( 7, 'Erro ao tentar adicionar fórum.'            )
    ERROR_ADD_EMAIL                     = ( 8, 'Erro ao tentar adicionar e-mail.'           )
    pass
