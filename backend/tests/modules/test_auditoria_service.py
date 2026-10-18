from uuid import uuid4

import pytest

from app.core.exceptions import RegraNegocioViolada
from app.modules.auditoria.models import AcaoAuditoria
from app.modules.auditoria.service import AuditoriaService


class SessaoFalsa:
    def __init__(self):
        self.adicionados = []

    def add(self, obj):
        self.adicionados.append(obj)

    async def flush(self):
        pass


async def test_rn_10_1_indeferimento_exige_justificativa():
    service = AuditoriaService(SessaoFalsa())
    with pytest.raises(RegraNegocioViolada):
        await service.registrar(
            AcaoAuditoria.INSCRICAO_INDEFERIDA,
            entidade="inscricao",
            entidade_id=uuid4(),
            responsavel_id=uuid4(),
            justificativa="   ",
        )


async def test_registra_log_com_responsavel():
    sessao = SessaoFalsa()
    responsavel = uuid4()
    log = await AuditoriaService(sessao).registrar(
        AcaoAuditoria.CERTIFICADO_EMITIDO,
        entidade="certificado",
        entidade_id="ABC123",
        responsavel_id=responsavel,
    )
    assert sessao.adicionados == [log]
    assert log.responsavel_id == responsavel
    assert log.dados == {}
