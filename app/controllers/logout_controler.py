from fastapi.responses import RedirectResponse


# Logout
def logout_controller(request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="token")
    return response
