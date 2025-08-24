from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request

from open_webui.models.prompts import (
    PromptForm,
    PromptUserResponse,
    PromptModel,
    Prompts,
)
from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.auth import get_admin_user, get_verified_user
from open_webui.utils.access_control import has_access, has_permission
from open_webui.config import ENABLE_ADMIN_WORKSPACE_CONTENT_ACCESS

router = APIRouter()



