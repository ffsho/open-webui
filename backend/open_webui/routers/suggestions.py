from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from open_webui.models.suggestions import (
    PromptSuggestionForm,
    PromptSuggestionModel,
    PromptsSuggestions,
)
from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.auth import get_admin_user, get_verified_user

router = APIRouter()

############################
# GetSuggestions
############################


@router.get("/", response_model=List[PromptSuggestionModel])
async def get_suggestions(user=Depends(get_verified_user)):
    suggestions = PromptsSuggestions.get_all_suggestions()
    return suggestions


############################
# GetSuggestionById
############################


@router.get("/{id}", response_model=Optional[PromptSuggestionModel])
async def get_suggestion_by_id(id: str, user=Depends(get_verified_user)):
    suggestion = PromptsSuggestions.get_suggestion_by_id(id)
    if suggestion:
        return suggestion
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# CreateNewSuggestion
############################


@router.post("/create", response_model=Optional[PromptSuggestionModel])
async def create_new_suggestion(
    form_data: PromptSuggestionForm, user=Depends(get_admin_user)
):
    
    existing_suggestion = PromptsSuggestions.get_suggestion_by_title(form_data.title)
    if existing_suggestion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.ALREADY_EXISTS,
        )

    suggestion = PromptsSuggestions.add_suggestion(form_data)
    if suggestion:
        return suggestion
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(),
    )


############################
# UpdateSuggestion
############################


@router.put("/{id}", response_model=Optional[PromptSuggestionModel])
async def update_suggestion(
    id: str, form_data: PromptSuggestionForm, user=Depends(get_admin_user)
):
    suggestion = PromptsSuggestions.get_suggestion_by_id(id)
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    # Check if another suggestion with the same title already exists
    existing_suggestion = PromptsSuggestions.get_suggestion_by_title(form_data.title)
    if existing_suggestion and existing_suggestion.id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.ALREADY_EXISTS,
        )

    updated_suggestion = PromptsSuggestions.update_suggestion(id, form_data)
    if updated_suggestion:
        return updated_suggestion
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES.DEFAULT(),
        )


############################
# DeleteSuggestion
############################


@router.delete("/{id}", response_model=bool)
async def delete_suggestion(id: str, user=Depends(get_admin_user)):
    suggestion = PromptsSuggestions.get_suggestion_by_id(id)
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    result = PromptsSuggestions.delete_suggestion(id)
    return result


############################
# Suggestion Usage Count
############################


@router.get("/{id}/usage", response_model=int)
async def get_suggestion_usage_count(id: str, user=Depends(get_verified_user)):
    suggestion = PromptsSuggestions.get_suggestion_by_id(id)
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    return suggestion.usage_count


@router.post("/{id}/increment-usage", response_model=dict)
async def increment_suggestion_usage_count(id: str, user=Depends(get_verified_user)):
    suggestion = PromptsSuggestions.get_suggestion_by_id(id)
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    success = PromptsSuggestions.increment_usage_count(id)
    if success:
        updated_suggestion = PromptsSuggestions.get_suggestion_by_id(id)
        return {
            "message": "Usage count incremented",
            "new_count": updated_suggestion.usage_count if updated_suggestion else 0
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES.DEFAULT(),
        )


############################
# Initialize Default Suggestions
############################


@router.post("/initialize-defaults", response_model=dict)
async def initialize_default_suggestions(user=Depends(get_admin_user)):
    try:
        PromptsSuggestions.set_default_prompts_suggestions()
        return {"message": "Default suggestions initialized successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize default suggestions: {str(e)}",
        )