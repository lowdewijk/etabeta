from fastapi import HTTPException


class UserError(HTTPException):
  user: str
  message: str

  def __init__(self, user: str, message: str):
    self.user = user
    self.message = message
    super().__init__(status_code=200, detail=self.message, headers={ "x-user-error": "true" })
