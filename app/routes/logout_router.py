from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.api_route("/logout", methods=["GET", "POST"])
async def logout(request: Request, response: Response):
    """
    Logout universal para:
    - JWT (login interno)
    - OAuth Google
    - OAuth Facebook
    """

    # 🔒 Limpar cookies de JWT
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    # 🔑 Limpar dados da sessão (usado por OAuth)
    if hasattr(request, "session"):
        request.session.clear()

    # 🔁 Redirecionar ou retornar mensagem
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

