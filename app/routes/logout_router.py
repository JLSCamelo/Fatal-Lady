from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter()

@router.get("/logout")
async def logout(request: Request, response: Response):
    """
    Logout universal para:
    - JWT (login interno)
    - OAuth Google
    - OAuth Facebook
    """
    
    # Limpar cookies de JWT
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    # Limpar dados da sessão (usado por OAuth)
    if hasattr(request, "session"):
        request.session.clear()

    return RedirectResponse(url="/login", status_code=303)
