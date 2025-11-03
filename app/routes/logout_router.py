from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.api_route("/logout", methods=["GET", "POST"])
async def logout(request: Request, response: Response):
    # ... (Comentários omitidos)

    # 🔒 Limpar cookies de JWT com o PATH de exclusão para garantir que o navegador encontre e apague o cookie.
    response.delete_cookie(key="token", path="/") # <-- ADICIONE O PATH="/" AQUI

    # Os outros cookies podem ser mantidos por precaução ou removidos se não forem usados:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    # ... (Restante do código)

    # 🔁 Redirecionar para o index principal.
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)